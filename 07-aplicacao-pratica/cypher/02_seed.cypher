// Dados de exemplo da rede social.
// Responsável por ampliar o dataset: Vinícius (ver 00-divisao e 06-rede-social).
// Usa MERGE: rodar de novo não duplica nada.
// Atenção: o script scripts/seed.py separa as instruções por ponto e vírgula,
// então não use esse caractere dentro dos textos.

// ---------- Usuários
UNWIND [
  {username: 'ana.souza',   nome: 'Ana Souza',      cidade: 'Fortaleza',  bio: 'Dev backend e fã de café'},
  {username: 'bruno.lima',  nome: 'Bruno Lima',     cidade: 'Fortaleza',  bio: 'Fotógrafo nas horas vagas'},
  {username: 'carla.mendes',nome: 'Carla Mendes',   cidade: 'Recife',     bio: 'Cientista de dados'},
  {username: 'diego.alves', nome: 'Diego Alves',    cidade: 'Natal',      bio: 'Corredor e gamer'},
  {username: 'elisa.rocha', nome: 'Elisa Rocha',    cidade: 'Fortaleza',  bio: 'Designer de produto'},
  {username: 'felipe.costa',nome: 'Felipe Costa',   cidade: 'São Paulo',  bio: 'Músico e professor'},
  {username: 'gabi.nunes',  nome: 'Gabriela Nunes', cidade: 'Recife',     bio: 'Viajante e escritora'},
  {username: 'heitor.reis', nome: 'Heitor Reis',    cidade: 'Teresina',   bio: 'Engenheiro de dados'},
  {username: 'iris.melo',   nome: 'Íris Melo',      cidade: 'Fortaleza',  bio: 'Estudante de computação'},
  {username: 'jonas.pinto', nome: 'Jonas Pinto',    cidade: 'Natal',      bio: 'Chef de cozinha'}
] AS dado
MERGE (u:Usuario {username: dado.username})
ON CREATE SET u.nome = dado.nome, u.cidade = dado.cidade, u.bio = dado.bio, u.criadoEm = datetime();

// ---------- Interesses
UNWIND [
  ['ana.souza',    ['Tecnologia', 'Café', 'Música']],
  ['bruno.lima',   ['Fotografia', 'Viagem']],
  ['carla.mendes', ['Tecnologia', 'Ciência de Dados', 'Viagem']],
  ['diego.alves',  ['Games', 'Corrida', 'Tecnologia']],
  ['elisa.rocha',  ['Design', 'Fotografia', 'Café']],
  ['felipe.costa', ['Música', 'Educação']],
  ['gabi.nunes',   ['Viagem', 'Livros', 'Fotografia']],
  ['heitor.reis',  ['Ciência de Dados', 'Tecnologia', 'Corrida']],
  ['iris.melo',    ['Tecnologia', 'Games', 'Livros']],
  ['jonas.pinto',  ['Culinária', 'Viagem', 'Música']]
] AS par
MATCH (u:Usuario {username: par[0]})
UNWIND par[1] AS nomeInteresse
MERGE (i:Interesse {nome: nomeInteresse})
MERGE (u)-[:INTERESSADO_EM]->(i);

// ---------- Quem segue quem
UNWIND [
  ['ana.souza', 'bruno.lima'],   ['ana.souza', 'carla.mendes'], ['ana.souza', 'elisa.rocha'],
  ['bruno.lima', 'elisa.rocha'], ['bruno.lima', 'gabi.nunes'],  ['bruno.lima', 'ana.souza'],
  ['carla.mendes', 'heitor.reis'], ['carla.mendes', 'ana.souza'], ['carla.mendes', 'gabi.nunes'],
  ['diego.alves', 'iris.melo'],  ['diego.alves', 'heitor.reis'],
  ['elisa.rocha', 'gabi.nunes'], ['elisa.rocha', 'felipe.costa'],
  ['felipe.costa', 'jonas.pinto'],
  ['gabi.nunes', 'jonas.pinto'], ['gabi.nunes', 'bruno.lima'],
  ['heitor.reis', 'diego.alves'], ['heitor.reis', 'iris.melo'],
  ['iris.melo', 'ana.souza'],    ['iris.melo', 'diego.alves'],
  ['jonas.pinto', 'felipe.costa']
] AS par
MATCH (a:Usuario {username: par[0]}), (b:Usuario {username: par[1]})
MERGE (a)-[r:SEGUE]->(b)
ON CREATE SET r.desde = datetime();

// ---------- Posts (id fixo para o seed ser idempotente)
UNWIND [
  {id: 'seed-01', autor: 'ana.souza',    texto: 'Primeiro deploy da semana sem quebrar nada!', dias: 6},
  {id: 'seed-02', autor: 'bruno.lima',   texto: 'Pôr do sol na Praia de Iracema hoje', dias: 5},
  {id: 'seed-03', autor: 'carla.mendes', texto: 'Grafos deixam consultas de recomendação muito mais simples', dias: 4},
  {id: 'seed-04', autor: 'elisa.rocha',  texto: 'Novo protótipo do app saindo do forno', dias: 3},
  {id: 'seed-05', autor: 'gabi.nunes',   texto: 'Dica de livro: viagens pelo sertão nordestino', dias: 3},
  {id: 'seed-06', autor: 'heitor.reis',  texto: 'Pipeline de dados rodando em 3 minutos em vez de 40', dias: 2},
  {id: 'seed-07', autor: 'diego.alves',  texto: 'Fiz 10 km hoje cedo, alguém topa correr sábado?', dias: 2},
  {id: 'seed-08', autor: 'jonas.pinto',  texto: 'Receita de baião de dois da casa no próximo post', dias: 1},
  {id: 'seed-09', autor: 'felipe.costa', texto: 'Show acústico sexta no centro, apareçam', dias: 1},
  {id: 'seed-10', autor: 'iris.melo',    texto: 'Estudando Cypher para o trabalho de NoSQL', dias: 0}
] AS dado
MATCH (u:Usuario {username: dado.autor})
MERGE (p:Post {id: dado.id})
ON CREATE SET p.conteudo = dado.texto, p.criadoEm = datetime() - duration({days: dado.dias})
MERGE (u)-[:PUBLICOU]->(p);

// ---------- Curtidas
UNWIND [
  ['ana.souza', 'seed-03'], ['ana.souza', 'seed-04'], ['bruno.lima', 'seed-01'],
  ['carla.mendes', 'seed-06'], ['diego.alves', 'seed-10'], ['elisa.rocha', 'seed-02'],
  ['gabi.nunes', 'seed-02'], ['gabi.nunes', 'seed-08'], ['heitor.reis', 'seed-03'],
  ['iris.melo', 'seed-07'], ['jonas.pinto', 'seed-09'], ['felipe.costa', 'seed-08']
] AS par
MATCH (u:Usuario {username: par[0]}), (p:Post {id: par[1]})
MERGE (u)-[c:CURTIU]->(p)
ON CREATE SET c.em = datetime();
