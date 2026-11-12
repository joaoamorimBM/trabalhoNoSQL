// =====================================================================
// CRUD da demonstração — PLANO B (rodar no Neo4j Browser, um bloco por vez)
// Mesmas operações que a aplicação web faz.
// =====================================================================

// ---------- C: CREATE — novo usuário com interesses
CREATE (u:Usuario {username: 'prof.demo', nome: 'Professor Demo', cidade: 'Fortaleza',
                   bio: 'Criado ao vivo na apresentação', criadoEm: datetime()})
WITH u
UNWIND ['Tecnologia', 'Livros'] AS interesse
MERGE (i:Interesse {nome: interesse})
MERGE (u)-[:INTERESSADO_EM]->(i);

// C: CREATE — relacionamentos (seguir) e um post
MATCH (u:Usuario {username: 'prof.demo'}), (a:Usuario {username: 'ana.souza'})
MERGE (u)-[:SEGUE {desde: datetime()}]->(a);

MATCH (u:Usuario {username: 'prof.demo'})
CREATE (u)-[:PUBLICOU]->(:Post {id: randomUUID(), conteudo: 'Olá, turma de NoSQL!', criadoEm: datetime()});

// ---------- R: READ — perfil + vizinhança no grafo (ver em modo Graph)
MATCH (u:Usuario {username: 'prof.demo'})-[r]-(vizinho)
RETURN u, r, vizinho;

// R: READ — sugestão de quem seguir (amigos de amigos + interesses em comum)
MATCH (eu:Usuario {username: 'prof.demo'})-[:SEGUE]->(amigo)-[:SEGUE]->(sug:Usuario)
WHERE sug <> eu AND NOT EXISTS { (eu)-[:SEGUE]->(sug) }
WITH eu, sug, collect(DISTINCT amigo.nome) AS amigosEmComum
OPTIONAL MATCH (eu)-[:INTERESSADO_EM]->(i)<-[:INTERESSADO_EM]-(sug)
RETURN sug.nome AS sugestao, amigosEmComum, collect(DISTINCT i.nome) AS interessesEmComum
ORDER BY size(amigosEmComum) * 2 + size(interessesEmComum) DESC;

// R: READ — graus de separação
MATCH (a:Usuario {username: 'prof.demo'}), (b:Usuario {username: 'jonas.pinto'})
MATCH caminho = shortestPath((a)-[:SEGUE*..6]-(b))
RETURN caminho, length(caminho) AS graus;

// ---------- U: UPDATE — alterar propriedades do nó
MATCH (u:Usuario {username: 'prof.demo'})
SET u.cidade = 'Recife', u.bio = 'Bio atualizada ao vivo', u.atualizadoEm = datetime()
RETURN u;

// ---------- D: DELETE — remover só o relacionamento
MATCH (:Usuario {username: 'prof.demo'})-[r:SEGUE]->(:Usuario {username: 'ana.souza'})
DELETE r;

// D: DELETE — remover o usuário, os posts dele e todas as arestas
MATCH (u:Usuario {username: 'prof.demo'})
OPTIONAL MATCH (u)-[:PUBLICOU]->(p:Post)
DETACH DELETE p, u;

// Conferir que sumiu
MATCH (u:Usuario {username: 'prof.demo'}) RETURN count(u) AS restantes;
