# Aplicação prática — Rede Social em grafo (Neo4j)

**Responsável:** João Pedro · **Vale:** 4,0 pontos (CRUD ao vivo)

App web (Python + Flask + driver oficial do Neo4j) com o CRUD da rede social, visualização do grafo e um
painel que mostra **o Cypher executado em cada ação**.

| Operação | O que acontece no grafo |
|---|---|
| **Create** | cria nó `Usuario` (+ `Interesse`), `Post` com aresta `PUBLICOU`, arestas `SEGUE` e `CURTIU` |
| **Read** | perfil, feed, **sugestão de quem seguir** (amigos de amigos + interesses em comum), **graus de separação** (`shortestPath`) |
| **Update** | `SET` nas propriedades do usuário / conteúdo do post, troca de interesses |
| **Delete** | remove só a aresta (deixar de seguir), remove post, remove usuário com `DETACH DELETE` |

Modelo do grafo: [`modelagem.md`](modelagem.md) · Conteúdo dos slides desta parte: [`conteudo.md`](conteudo.md)

## Como rodar

Todos os comandos abaixo são executados **dentro desta pasta** (`07-aplicacao-pratica`).

### 1. Ter um Neo4j rodando (escolha uma opção)

> **Recomendação para a apresentação:** a demo roda no **computador do João Pedro**, com o Neo4j
> **local** (opção A). Já foi testado assim: CRUD completo + plano B funcionando.
> O **AuraDB Free** (opção B) fica como **plano de contingência**: se o PC do João Pedro der problema
> no dia, qualquer pessoa da equipe roda a aplicação apontando para o banco na nuvem, sem instalar
> Neo4j. Vale criar a instância alguns dias antes, rodar o `seed.py` nela e deixar as credenciais
> com o João Pedro. Atenção: instâncias Free pausam depois de alguns dias sem uso — entre no console
> e retome a instância na véspera da apresentação.

- **A) Neo4j local (zip, sem instalar nada além do Java 17/21):**
  1. Baixe o *Neo4j Community 5.26* (Windows, zip) em <https://neo4j.com/deployment-center/> e
     descompacte fora do repositório (ex.: `D:\Trabalhos\neo4j`).
  2. Defina a senha (só antes da primeira inicialização):
     `bin\neo4j-admin.bat dbms set-initial-password SUA-SENHA`
  3. Inicie e deixe a janela aberta: `bin\neo4j.bat console`
     (Neo4j Browser em <http://localhost:7474>).
- **B) AuraDB Free (nuvem):** crie uma instância grátis em <https://console.neo4j.io>,
  baixe o arquivo de credenciais e copie URI, usuário e senha para o `.env`.
- **C) Docker:** `docker compose up -d` (Neo4j Browser em <http://localhost:7474>).
- **D) Neo4j Desktop:** crie um DBMS local (versão 5.x) e inicie.

### 2. Configurar e instalar

```bash
cd 07-aplicacao-pratica
copy .env.example .env          # Linux/macOS: cp .env.example .env
# edite o .env com URI, usuário e senha do seu Neo4j

python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Carregar constraints e dados de exemplo

```bash
python scripts/seed.py            # cria constraints + dados (pode rodar várias vezes)
python scripts/seed.py --limpar   # apaga tudo e recarrega
```

### 4. Subir a aplicação

```bash
python run.py
```

Abra <http://localhost:5000>.

## Plano B da demo

Se a aplicação falhar na hora, [`cypher/03_crud_demo.cypher`](cypher/03_crud_demo.cypher) tem o mesmo
CRUD para rodar bloco a bloco no **Neo4j Browser**.

## Estrutura

```
app/
  __init__.py      # cria o app Flask
  config.py        # lê o .env
  db.py            # driver Neo4j + registro do Cypher executado
  repositorio.py   # TODAS as consultas Cypher (CRUD + consultas de grafo)
  rotas.py         # API REST
  static/          # interface web (HTML/CSS/JS + vis-network)
cypher/
  01_constraints.cypher
  02_seed.cypher       # dados de exemplo (Vinícius amplia)
  03_crud_demo.cypher  # plano B no Neo4j Browser
scripts/seed.py        # carrega 01 e 02 no banco
```

## API

| Método | Rota | Ação |
|---|---|---|
| GET | `/api/usuarios` | listar usuários |
| POST | `/api/usuarios` | criar usuário `{username, nome, cidade, bio, interesses}` |
| GET | `/api/usuarios/<u>` | perfil completo |
| PUT | `/api/usuarios/<u>` | atualizar `{nome, cidade, bio, interesses}` |
| DELETE | `/api/usuarios/<u>` | excluir usuário (DETACH DELETE) |
| POST / DELETE | `/api/usuarios/<u>/seguir/<alvo>` | seguir / deixar de seguir |
| POST | `/api/usuarios/<u>/posts` | publicar `{conteudo}` |
| PUT / DELETE | `/api/posts/<id>` | editar / excluir post |
| POST | `/api/posts/<id>/curtir/<u>` | curtir |
| GET | `/api/usuarios/<u>/feed` | feed |
| GET | `/api/usuarios/<u>/sugestoes` | quem seguir |
| GET | `/api/caminho?de=<u>&para=<v>` | graus de separação |
| GET | `/api/grafo` | nós e arestas para visualização |
