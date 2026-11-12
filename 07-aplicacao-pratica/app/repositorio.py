"""Todas as consultas Cypher da rede social.

Modelo do grafo
---------------
(:Usuario {username, nome, cidade, bio, criadoEm})
(:Post {id, conteudo, criadoEm, editadoEm})
(:Interesse {nome})

(:Usuario)-[:SEGUE {desde}]->(:Usuario)
(:Usuario)-[:PUBLICOU]->(:Post)
(:Usuario)-[:CURTIU {em}]->(:Post)
(:Usuario)-[:INTERESSADO_EM]->(:Interesse)
"""
from . import db

# ---------------------------------------------------------------- Usuários (CRUD)


def criar_usuario(username: str, nome: str, cidade: str = "", bio: str = "",
                  interesses: list[str] | None = None) -> dict | None:
    """CREATE — cria o nó Usuario e liga aos nós Interesse."""
    linhas = db.escrever(
        """
        CREATE (u:Usuario {username: $username, nome: $nome, cidade: $cidade,
                           bio: $bio, criadoEm: datetime()})
        WITH u
        UNWIND $interesses AS interesse
        MERGE (i:Interesse {nome: interesse})
        MERGE (u)-[:INTERESSADO_EM]->(i)
        RETURN DISTINCT u.username AS username
        """,
        username=username, nome=nome, cidade=cidade, bio=bio,
        interesses=interesses or [],
    )
    return obter_usuario(username) if linhas or not interesses else None


def listar_usuarios() -> list[dict]:
    """READ — lista todos os usuários com contagem de seguidores/seguindo."""
    return db.ler(
        """
        MATCH (u:Usuario)
        RETURN u.username AS username, u.nome AS nome, u.cidade AS cidade,
               COUNT { (u)<-[:SEGUE]-() } AS seguidores,
               COUNT { (u)-[:SEGUE]->() } AS seguindo
        ORDER BY u.nome
        """
    )


def obter_usuario(username: str) -> dict | None:
    """READ — perfil completo: dados, interesses, quem segue e posts."""
    linhas = db.ler(
        """
        MATCH (u:Usuario {username: $username})
        RETURN u.username AS username, u.nome AS nome, u.cidade AS cidade, u.bio AS bio,
               toString(u.criadoEm) AS criadoEm,
               [(u)-[:INTERESSADO_EM]->(i) | i.nome] AS interesses,
               [(u)-[:SEGUE]->(s) | {username: s.username, nome: s.nome}] AS seguindo,
               [(u)<-[:SEGUE]-(s) | {username: s.username, nome: s.nome}] AS seguidores,
               [(u)-[:PUBLICOU]->(p) | {id: p.id, conteudo: p.conteudo,
                    criadoEm: toString(p.criadoEm),
                    curtidas: COUNT { (p)<-[:CURTIU]-() }}] AS posts
        """,
        username=username,
    )
    if not linhas:
        return None
    perfil = linhas[0]
    perfil["posts"].sort(key=lambda p: p["criadoEm"] or "", reverse=True)
    return perfil


def atualizar_usuario(username: str, campos: dict,
                      interesses: list[str] | None = None) -> dict | None:
    """UPDATE — altera propriedades do nó e, se enviado, substitui os interesses."""
    permitidos = {k: v for k, v in campos.items() if k in {"nome", "cidade", "bio"}}
    linhas = db.escrever(
        """
        MATCH (u:Usuario {username: $username})
        SET u += $campos, u.atualizadoEm = datetime()
        RETURN u.username AS username
        """,
        username=username, campos=permitidos,
    )
    if not linhas:
        return None
    if interesses is not None:
        db.escrever(
            """
            MATCH (u:Usuario {username: $username})
            OPTIONAL MATCH (u)-[r:INTERESSADO_EM]->()
            DELETE r
            WITH DISTINCT u
            UNWIND $interesses AS interesse
            MERGE (i:Interesse {nome: interesse})
            MERGE (u)-[:INTERESSADO_EM]->(i)
            """,
            username=username, interesses=interesses,
        )
    return obter_usuario(username)


def excluir_usuario(username: str) -> bool:
    """DELETE — remove o usuário, seus posts e todos os relacionamentos (DETACH DELETE)."""
    linhas = db.escrever(
        """
        MATCH (u:Usuario {username: $username})
        OPTIONAL MATCH (u)-[:PUBLICOU]->(p:Post)
        WITH u, collect(p) AS posts
        FOREACH (p IN posts | DETACH DELETE p)
        DETACH DELETE u
        RETURN size(posts) AS postsRemovidos
        """,
        username=username,
    )
    return bool(linhas)


# ---------------------------------------------------------------- Relacionamento SEGUE


def seguir(seguidor: str, seguido: str) -> bool:
    """CREATE de aresta — MERGE garante que não duplica o relacionamento."""
    return bool(db.escrever(
        """
        MATCH (a:Usuario {username: $seguidor}), (b:Usuario {username: $seguido})
        MERGE (a)-[r:SEGUE]->(b)
        ON CREATE SET r.desde = datetime()
        RETURN type(r) AS rel
        """,
        seguidor=seguidor, seguido=seguido,
    ))


def deixar_de_seguir(seguidor: str, seguido: str) -> bool:
    """DELETE de aresta — remove apenas o relacionamento, os nós continuam."""
    linhas = db.escrever(
        """
        MATCH (:Usuario {username: $seguidor})-[r:SEGUE]->(:Usuario {username: $seguido})
        DELETE r
        RETURN count(r) AS removidos
        """,
        seguidor=seguidor, seguido=seguido,
    )
    return bool(linhas and linhas[0]["removidos"])


# ---------------------------------------------------------------- Posts (CRUD)


def criar_post(username: str, conteudo: str) -> dict | None:
    linhas = db.escrever(
        """
        MATCH (u:Usuario {username: $username})
        CREATE (u)-[:PUBLICOU]->(p:Post {id: randomUUID(), conteudo: $conteudo,
                                         criadoEm: datetime()})
        RETURN p.id AS id, p.conteudo AS conteudo, toString(p.criadoEm) AS criadoEm
        """,
        username=username, conteudo=conteudo,
    )
    return linhas[0] if linhas else None


def atualizar_post(post_id: str, conteudo: str) -> dict | None:
    linhas = db.escrever(
        """
        MATCH (p:Post {id: $id})
        SET p.conteudo = $conteudo, p.editadoEm = datetime()
        RETURN p.id AS id, p.conteudo AS conteudo, toString(p.editadoEm) AS editadoEm
        """,
        id=post_id, conteudo=conteudo,
    )
    return linhas[0] if linhas else None


def excluir_post(post_id: str) -> bool:
    linhas = db.escrever(
        """
        MATCH (p:Post {id: $id})
        DETACH DELETE p
        RETURN count(*) AS removidos
        """,
        id=post_id,
    )
    return bool(linhas and linhas[0]["removidos"])


def curtir(username: str, post_id: str) -> bool:
    return bool(db.escrever(
        """
        MATCH (u:Usuario {username: $username}), (p:Post {id: $id})
        MERGE (u)-[c:CURTIU]->(p)
        ON CREATE SET c.em = datetime()
        RETURN type(c) AS rel
        """,
        username=username, id=post_id,
    ))


# ---------------------------------------------------------------- Consultas de grafo


def feed(username: str, limite: int = 20) -> list[dict]:
    """Posts de quem o usuário segue, mais recentes primeiro."""
    return db.ler(
        """
        MATCH (:Usuario {username: $username})-[:SEGUE]->(autor:Usuario)-[:PUBLICOU]->(p:Post)
        RETURN p.id AS id, p.conteudo AS conteudo, toString(p.criadoEm) AS criadoEm,
               autor.username AS autor, autor.nome AS autorNome,
               COUNT { (p)<-[:CURTIU]-() } AS curtidas
        ORDER BY p.criadoEm DESC
        LIMIT $limite
        """,
        username=username, limite=limite,
    )


def sugestoes(username: str, limite: int = 5) -> list[dict]:
    """"Quem seguir": amigos de amigos (2 saltos) pontuados por conexões e interesses em comum.

    Em SQL isso exigiria vários self-JOINs na tabela de seguidores; no grafo é só
    percorrer o padrão (eu)-[:SEGUE]->(amigo)-[:SEGUE]->(sugestao).
    """
    return db.ler(
        """
        MATCH (eu:Usuario {username: $username})-[:SEGUE]->(amigo:Usuario)-[:SEGUE]->(sug:Usuario)
        WHERE sug <> eu AND NOT EXISTS { (eu)-[:SEGUE]->(sug) }
        WITH eu, sug, collect(DISTINCT amigo.nome) AS amigosEmComum
        OPTIONAL MATCH (eu)-[:INTERESSADO_EM]->(i:Interesse)<-[:INTERESSADO_EM]-(sug)
        WITH sug, amigosEmComum, collect(DISTINCT i.nome) AS interessesEmComum
        RETURN sug.username AS username, sug.nome AS nome, amigosEmComum, interessesEmComum,
               size(amigosEmComum) * 2 + size(interessesEmComum) AS pontuacao
        ORDER BY pontuacao DESC, nome
        LIMIT $limite
        """,
        username=username, limite=limite,
    )


def menor_caminho(origem: str, destino: str) -> dict | None:
    """Graus de separação entre duas pessoas (ignora a direção do SEGUE)."""
    linhas = db.ler(
        """
        MATCH (a:Usuario {username: $origem}), (b:Usuario {username: $destino})
        MATCH caminho = shortestPath((a)-[:SEGUE*..6]-(b))
        RETURN [n IN nodes(caminho) | n.nome] AS pessoas, length(caminho) AS graus
        """,
        origem=origem, destino=destino,
    )
    return linhas[0] if linhas else None


def grafo_completo() -> dict:
    """Nós e arestas para a visualização na interface."""
    nos = db.ler(
        """
        MATCH (n) WHERE n:Usuario OR n:Post OR n:Interesse
        RETURN elementId(n) AS id, labels(n)[0] AS tipo,
               coalesce(n.nome, left(n.conteudo, 25) + '…') AS rotulo
        LIMIT 400
        """
    )
    arestas = db.ler(
        """
        MATCH (a)-[r]->(b)
        RETURN elementId(a) AS de, elementId(b) AS para, type(r) AS tipo
        LIMIT 1000
        """
    )
    return {"nos": nos, "arestas": arestas}
