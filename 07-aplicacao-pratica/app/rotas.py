"""API REST da rede social. Toda resposta JSON traz `cypher`: as consultas executadas."""
import re

from flask import Blueprint, current_app, g, jsonify, request
from neo4j.exceptions import ConstraintError, ServiceUnavailable, AuthError

from . import repositorio as repo

bp = Blueprint("api", __name__)

USERNAME_VALIDO = re.compile(r"^[a-z0-9_.]{3,30}$")


def resposta(dados=None, status: int = 200, erro: str | None = None):
    corpo = {"dados": dados, "cypher": g.get("cypher", [])}
    if erro:
        corpo["erro"] = erro
    return jsonify(corpo), status


def corpo_json() -> dict:
    return request.get_json(silent=True) or {}


@bp.errorhandler(ServiceUnavailable)
@bp.errorhandler(AuthError)
def sem_conexao(e):
    return resposta(status=503, erro=f"Não foi possível conectar ao Neo4j: {e}")


@bp.errorhandler(ConstraintError)
def violou_restricao(_e):
    return resposta(status=409, erro="Já existe um usuário com esse username.")


# ------------------------------------------------------------------ Página


@bp.get("/")
def index():
    return current_app.send_static_file("index.html")


# ------------------------------------------------------------------ Usuários


@bp.get("/api/usuarios")
def listar_usuarios():
    return resposta(repo.listar_usuarios())


@bp.post("/api/usuarios")
def criar_usuario():
    d = corpo_json()
    username = (d.get("username") or "").strip().lower()
    nome = (d.get("nome") or "").strip()
    if not USERNAME_VALIDO.match(username):
        return resposta(status=400, erro="username deve ter 3–30 caracteres: letras minúsculas, números, _ ou .")
    if not nome:
        return resposta(status=400, erro="nome é obrigatório.")
    usuario = repo.criar_usuario(
        username, nome, (d.get("cidade") or "").strip(), (d.get("bio") or "").strip(),
        _lista(d.get("interesses")),
    )
    return resposta(usuario, 201)


@bp.get("/api/usuarios/<username>")
def obter_usuario(username):
    usuario = repo.obter_usuario(username)
    if usuario is None:
        return resposta(status=404, erro="Usuário não encontrado.")
    return resposta(usuario)


@bp.put("/api/usuarios/<username>")
def atualizar_usuario(username):
    d = corpo_json()
    interesses = _lista(d["interesses"]) if "interesses" in d else None
    usuario = repo.atualizar_usuario(username, d, interesses)
    if usuario is None:
        return resposta(status=404, erro="Usuário não encontrado.")
    return resposta(usuario)


@bp.delete("/api/usuarios/<username>")
def excluir_usuario(username):
    if not repo.excluir_usuario(username):
        return resposta(status=404, erro="Usuário não encontrado.")
    return resposta({"excluido": username})


# ------------------------------------------------------------------ Seguir


@bp.post("/api/usuarios/<username>/seguir/<alvo>")
def seguir(username, alvo):
    if username == alvo:
        return resposta(status=400, erro="Um usuário não pode seguir a si mesmo.")
    if not repo.seguir(username, alvo):
        return resposta(status=404, erro="Usuário não encontrado.")
    return resposta({"seguidor": username, "seguido": alvo}, 201)


@bp.delete("/api/usuarios/<username>/seguir/<alvo>")
def deixar_de_seguir(username, alvo):
    if not repo.deixar_de_seguir(username, alvo):
        return resposta(status=404, erro="Relacionamento SEGUE não encontrado.")
    return resposta({"seguidor": username, "deixouDeSeguir": alvo})


# ------------------------------------------------------------------ Posts


@bp.post("/api/usuarios/<username>/posts")
def criar_post(username):
    conteudo = (corpo_json().get("conteudo") or "").strip()
    if not conteudo:
        return resposta(status=400, erro="conteudo é obrigatório.")
    post = repo.criar_post(username, conteudo)
    if post is None:
        return resposta(status=404, erro="Usuário não encontrado.")
    return resposta(post, 201)


@bp.put("/api/posts/<post_id>")
def atualizar_post(post_id):
    conteudo = (corpo_json().get("conteudo") or "").strip()
    if not conteudo:
        return resposta(status=400, erro="conteudo é obrigatório.")
    post = repo.atualizar_post(post_id, conteudo)
    if post is None:
        return resposta(status=404, erro="Post não encontrado.")
    return resposta(post)


@bp.delete("/api/posts/<post_id>")
def excluir_post(post_id):
    if not repo.excluir_post(post_id):
        return resposta(status=404, erro="Post não encontrado.")
    return resposta({"excluido": post_id})


@bp.post("/api/posts/<post_id>/curtir/<username>")
def curtir(post_id, username):
    if not repo.curtir(username, post_id):
        return resposta(status=404, erro="Usuário ou post não encontrado.")
    return resposta({"curtiu": post_id}, 201)


# ------------------------------------------------------------------ Consultas de grafo


@bp.get("/api/usuarios/<username>/feed")
def feed(username):
    return resposta(repo.feed(username))


@bp.get("/api/usuarios/<username>/sugestoes")
def sugestoes(username):
    return resposta(repo.sugestoes(username))


@bp.get("/api/caminho")
def caminho():
    origem, destino = request.args.get("de", ""), request.args.get("para", "")
    if not origem or not destino or origem == destino:
        return resposta(status=400, erro="Informe dois usuários diferentes em ?de=&para=")
    resultado = repo.menor_caminho(origem, destino)
    if resultado is None:
        return resposta(status=404, erro="Não há caminho entre esses usuários (até 6 graus).")
    return resposta(resultado)


@bp.get("/api/grafo")
def grafo():
    return resposta(repo.grafo_completo())


def _lista(valor) -> list[str]:
    if isinstance(valor, str):
        valor = valor.split(",")
    return [v.strip() for v in (valor or []) if isinstance(v, str) and v.strip()]
