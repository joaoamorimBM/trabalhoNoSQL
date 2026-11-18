# Tópico 1 — Paradigma orientado a grafo

> **Responsável:** Hamilton · **Tempo de fala:** ~1,5 min (abre a apresentação)
> Pesquisa conferida em 18/11/2026. Explicações são conceituais; não há benchmark próprio.

## Slide 1 — Abertura + o que é um banco orientado a grafo

- Equipe: João Pedro, Hamilton, Isaac, Luiz e Vinícius — Projeto 3: NoSQL, paradigma de grafo, Neo4j, rede social
- **Nó** = entidade · **rótulo** = tipo do nó · **relacionamento** = aresta com direção e tipo · **propriedades** = chave-valor em nós e arestas
- O grafo guarda dado **e** conexão no mesmo modelo — a conexão deixa de ser "deduzida" por chave estrangeira

**Fala:**
"Boa noite. Somos João Pedro, Hamilton, Isaac, Luiz e Vinícius, e o nosso paradigma sorteado foi o orientado a grafo, com o Neo4j e uma rede social. Eu sou o Hamilton e começo explicando o paradigma. Um banco de grafos trabalha com três peças: nós, que são as entidades, como um usuário; relacionamentos, que ligam dois nós e sempre têm direção e um tipo, como SEGUE; e propriedades, que são pares chave-valor tanto nos nós quanto nos relacionamentos. Além disso, nós recebem rótulos, como Usuario ou Post, que funcionam como o 'tipo' da entidade. A diferença central é que a conexão é armazenada junto com o dado, e não recalculada a cada consulta."

**Imagem/diagrama:** (a criar) `imagens/grafo-basico.svg` — Ana —SEGUE→ Bruno —SEGUE→ Carla, com rótulos e uma propriedade em cada nó.

**Fontes:**
- Neo4j, *Graph database concepts*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ (acessado em 18/11/2026)
- Neo4j, *What is a graph database?*: https://neo4j.com/docs/getting-started/graph-database/ (acessado em 18/11/2026)

## Slide 2 — Grafo × relacional e o segredo da travessia

- **Relacional:** conexões via chave estrangeira e tabela de junção → cada salto custa mais um JOIN
- **Grafo:** relacionamento é cidadão de primeira classe (tem identidade, direção, tipo e propriedades)
- ***Index-free adjacency*:** cada nó aponta direto para seus relacionamentos → travessia em custo constante por salto, sem consultar índice global
- **Property Graph × RDF/triple store:** grafo de propriedades tem arestas com identidade e atributos; RDF é baseado em triplas sujeito–predicado–objeto

**Fala:**
"No modelo relacional, para ligar usuários e seguidores você precisa de uma tabela de junção, e cada nível a mais na consulta vira mais um JOIN. No grafo, o relacionamento é um objeto do banco, com identidade, direção, tipo e até propriedades — por isso dizemos que ele é cidadão de primeira classe. O que torna a travessia barata é o index-free adjacency: o registro do nó aponta diretamente para os relacionamentos dele, então andar de um nó para o vizinho não exige consultar um índice global. Vale distinguir dois modelos: o property graph, usado pelo Neo4j, em que arestas têm identidade e propriedades, e o RDF ou triple store, em que tudo é tripla sujeito–predicado–objeto."

**Imagem/diagrama:** (a criar) `imagens/grafo-vs-relacional.svg` — à esquerda tabelas usuarios/seguidores com JOIN; à direita o mesmo dado como nós e setas.

**Fontes:**
- Neo4j Graph Academy, *Index-free adjacency*: https://neo4j.com/graphacademy/training-overview-40/02-overview40-neo4j-graph-platform (acessado em 18/11/2026)
- Neo4j, *Transition from NoSQL to graph database*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/graphdb-vs-nosql/ (acessado em 18/11/2026)
- W3C, *RDF 1.1 Concepts and Abstract Syntax*: https://www.w3.org/TR/rdf11-concepts/ (acessado em 18/11/2026)
- Neo4j, *The co-evolution of computer hardware & graph databases* (custo por salto): https://neo4j.com/blog/cypher-and-gql/computer-hardware-native-graph-databases/ (acessado em 18/11/2026)

## Slide 3 — Onde grafos brilham

- **Redes sociais:** amigos de amigos, sugestão de quem seguir, graus de separação
- **Recomendação:** "quem comprou isso também comprou", similaridade por interesses
- **Detecção de fraude:** cadeias de contas, telefones e transações
- **Grafos de conhecimento** e **rotas/logística:** entidades interligadas e caminhos mínimos
- Critério prático: a pergunta envolve **vários saltos de conexão** — é aí que o grafo se paga

**Fala:**
"Esse paradigma aparece onde a pergunta é sobre caminhos. Em rede social, 'amigos de amigos' e 'quem eu deveria seguir'. Em recomendação, ligar clientes, produtos e interesses. Em fraude, seguir a cadeia entre contas, telefones e transações. E também em grafos de conhecimento e em rotas e logística, onde o problema é achar o melhor caminho. O critério prático é simples: se a resposta depende de percorrer vários saltos de relacionamento, o grafo tende a ser a escolha natural — e é exatamente o caso da rede social que a gente vai mostrar. A partir daqui o Isaac continua com o Neo4j por dentro."

**Imagem/diagrama:** (a criar) `imagens/casos-de-uso.svg` — cinco ícones/legendas com uma mini-rede em cada.

**Fontes:**
- Neo4j, *Use cases*: https://neo4j.com/use-cases/ (acessado em 18/11/2026)
- Neo4j, *Graph database concepts* (travessias e caminhos): https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ (acessado em 18/11/2026)
