# Aplicação prática — Rede social no Neo4j (CRUD)

> **Responsável:** João Pedro · **Tempo de fala:** ~3 min (fecha a apresentação)

## Slide 1 — Modelagem do grafo

- Nós: `Usuario`, `Post`, `Interesse`
- Relacionamentos: `SEGUE`, `PUBLICOU`, `CURTIU`, `INTERESSADO_EM`
- Propriedades nos nós **e** nas arestas (ex.: `SEGUE {desde}`)
- Unicidade: `username`, `id` do post, `nome` do interesse

**Fala:** Nossa rede social virou um grafo de propriedades. Cada pessoa é um nó Usuario, e quem segue quem
é uma aresta SEGUE com a data. Posts e interesses também são nós, então curtir ou se interessar por algo
é só criar uma aresta. Não existe tabela de junção: o relacionamento é guardado diretamente.

**Imagem/diagrama:** diagrama de `modelagem.md` (Usuario → SEGUE → Usuario, Usuario → PUBLICOU → Post,
Usuario → CURTIU → Post, Usuario → INTERESSADO_EM → Interesse)

**Fontes:**
- https://neo4j.com/docs/getting-started/graph-database/ (acessado em 12/11/2026)

## Slide 2 — A aplicação

- Python + Flask + driver oficial do Neo4j
- Banco: Neo4j Community 5.26 local (o mesmo app roda no AuraDB, na nuvem, só trocando o `.env`)
- Tela mostra o grafo e o **Cypher executado** em cada ação
- Plano B: o mesmo CRUD em Cypher no Neo4j Browser

**Fala:** A aplicação é um app web simples ligado ao Neo4j. Cada clique executa uma consulta
Cypher, e a própria tela mostra a consulta que rodou, para vocês verem exatamente o que acontece no banco.

**Imagem/diagrama:** print da tela do app

**Fontes:**
- https://neo4j.com/docs/python-manual/current/ (acessado em 12/11/2026)

## Slide 3 — CRUD em Cypher (resumo, fica na tela durante a demo)

- **Create:** `CREATE (u:Usuario {...})` · `MERGE (a)-[:SEGUE]->(b)`
- **Read:** amigos de amigos `(eu)-[:SEGUE]->()-[:SEGUE]->(sug)` · `shortestPath(...)`
- **Update:** `SET u.cidade = 'Recife'`
- **Delete:** `DELETE r` (só a aresta) · `DETACH DELETE u` (nó + arestas)

**Fala:** Agora vamos ao vivo: criar um usuário, fazer ele seguir alguém e publicar, consultar as sugestões
de quem seguir, alterar os dados dele e, por fim, excluir. Reparem que a sugestão de amigos, que no
relacional precisaria de vários JOINs na mesma tabela, aqui é só um padrão de dois saltos.

**Fontes:**
- https://neo4j.com/docs/cypher-manual/current/ (acessado em 12/11/2026)

## Demo ao vivo

Seguir o roteiro em [`06-rede-social/roteiro-demo.md`](../06-rede-social/roteiro-demo.md).
