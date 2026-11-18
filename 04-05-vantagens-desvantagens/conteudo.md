# Tópicos 4 e 5 — Vantagens, desvantagens e comparação entre modelos

> Responsável: Luiz · Tempo de fala: aproximadamente 2 minutos  
> Pesquisa conferida em 18/11/2026. Comparações são **qualitativas e dependem da consulta, dos índices, do volume de dados e da configuração**; não representam benchmark universal.

## Slide 1 — Principais vantagens do Neo4j

- **Relacionamentos nativos:** travessias entre nós e conexões são parte central do modelo.
- **Cypher:** consultas de padrões de grafo de forma expressiva.
- **Modelo flexível:** permite acrescentar tipos de nós e relações conforme evolui a aplicação.
- **Transações ACID:** consistência nas operações transacionais.
- **Ecossistema:** visualização e recursos adicionais de análise de grafos.

**Fala:**  
"A principal vantagem do Neo4j aparece quando a pergunta envolve várias conexões: por exemplo, quem segue pessoas com interesses semelhantes? No grafo, relacionamentos são representados diretamente e podem ser percorridos por consultas Cypher. O modelo também é flexível para incluir novas relações e o Neo4j oferece transações ACID. Para a rede social da equipe, isso facilita recursos como sugestões de pessoas para seguir e caminhos de conexão."

**Imagem/diagrama:** grafo ilustrativo `Ana → SEGUE → Bruno → SEGUE → Carla` versus três tabelas conectadas por chaves. Legenda: "representações conceituais, não teste de velocidade".

**Fontes:**
- Neo4j, *What is a graph database?*: https://neo4j.com/docs/getting-started/graph-database/ (acessado em 18/11/2026).
- Neo4j, *Graph database concepts*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ (acessado em 18/11/2026).
- Neo4j, *Transition from NoSQL to graph database*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/graphdb-vs-nosql/ (acessado em 18/11/2026).

## Slide 2 — Limitações e quando evitar

- Exige aprender **modelagem em grafos e Cypher**.
- Pode não ser a opção mais simples para **cadastros tabulares e relatórios agregados**.
- **Memória e infraestrutura** precisam ser dimensionadas para a carga de trabalho.
- Recursos corporativos e topologias avançadas podem envolver **licenciamento/custos**.
- **Distribuição de escrita e particionamento:** dependem da edição e da arquitetura escolhidas.

**Fala:**  
"O Neo4j não é a melhor escolha para todos os sistemas. Se o problema é basicamente uma planilha de cadastros ou relatórios com somas e agrupamentos, um banco relacional pode ser mais simples. Também existe a curva de aprendizado da modelagem em grafo, além de cuidados com memória, operação e licenciamento. Na escalabilidade, é preciso distinguir as edições: não é correto dizer que o Neo4j simplesmente não tem sharding, já que há ofertas recentes com esse recurso."

**Imagem/diagrama:** quadro "Vale considerar Neo4j" (muitas conexões) e "Avaliar alternativas" (dados essencialmente tabulares/analíticos).

**Fontes:**
- Neo4j, *Operations Manual — Introduction* (edições e escalabilidade): https://neo4j.com/docs/operations-manual/current/introduction/ (acessado em 18/11/2026).
- Neo4j, *Database administration* (detalhes de sharding conforme edição): https://neo4j.com/docs/operations-manual/current/database-administration/ (acessado em 18/11/2026).
- Neo4j, *Graph database concepts*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ (acessado em 18/11/2026).

## Slide 3 — Grafo × relacional × documentos: qual escolher?

| Critério | Grafo: Neo4j | Relacional: PostgreSQL | Documentos: MongoDB |
|---|---|---|---|
| Organização típica | Nós, relacionamentos e propriedades | Tabelas, linhas e chaves | Documentos semelhantes a JSON |
| Maior afinidade | Consultas sobre cadeias e padrões de relações | Dados estruturados, regras e consultas SQL | Registros semiestruturados e agregados por documento |
| Exemplo de uso | Sugestão de pessoas e graus de separação | Pedidos, pagamentos e contabilidade | Catálogo com atributos variados |
| Atenção | Exige boa modelagem e dimensionamento de grafos | Conexões complexas podem exigir várias junções ou consultas recursivas | Relações entre muitos documentos podem demandar outras estratégias de modelagem |

**Fala:**  
"A escolha depende da pergunta que o sistema precisa responder. O PostgreSQL é uma opção forte para transações e dados estruturados; o MongoDB é adequado para documentos com estrutura variável. Já o Neo4j se destaca quando os relacionamentos são o centro do problema. Nenhuma dessas tecnologias vence em todo cenário: para a rede social do trabalho, o grafo é uma escolha coerente porque seguir, curtir e recomendar são relações explícitas."

**Imagem/diagrama:** usar a própria tabela, resumida para leitura. Não atribuir ganho numérico de velocidade sem teste reproduzível.

**Fontes:**
- Neo4j, *Transition from NoSQL to graph database*: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/graphdb-vs-nosql/ (acessado em 18/11/2026).
- PostgreSQL, *About*: https://www.postgresql.org/about/ (acessado em 18/11/2026).
- MongoDB, *Document data model*: https://www.mongodb.com/docs/manual/core/data-modeling-introduction/ (acessado em 18/11/2026).

## Fechamento da parte do Luiz

"Assim, o Neo4j é uma boa ferramenta quando as conexões entre dados trazem valor para as consultas. Os casos reais demonstram aplicações variadas, mas as vantagens devem ser avaliadas junto às limitações técnicas e financeiras. Para nossa rede social, os relacionamentos entre usuários, posts e interesses justificam a escolha do modelo orientado a grafos."

## Referências consolidadas da pesquisa do Luiz

> **Atenção para o grupo:** esta lista consolida as fontes **desta parte**. As referências dos tópicos de Hamilton, Isaac, Vinícius e João Pedro devem ser adicionadas ao slide final pelos respectivos responsáveis.

1. NEO4J. *eBay customer story*. Disponível em: https://neo4j.com/customer-stories/ebay/. Acesso em: 18 nov. 2026.
2. NEO4J. *How Walmart uses Neo4j for retail competitive advantage*. Disponível em: https://neo4j.com/blog/graph-database/walmart-neo4j-competitive-advantage/. Acesso em: 18 nov. 2026.
3. NEO4J. *Real-time recommendations*. Disponível em: https://neo4j.com/use-cases/real-time-recommendations/. Acesso em: 18 nov. 2026.
4. NEO4J. *Graphs in government: A NASA knowledge graph*. Disponível em: https://neo4j.com/blog/knowledge-graph/graphs-in-government-nasa-knowledge-graph/. Acesso em: 18 nov. 2026.
5. NEO4J. *What is a graph database?* Disponível em: https://neo4j.com/docs/getting-started/graph-database/. Acesso em: 18 nov. 2026.
6. NEO4J. *Graph database concepts*. Disponível em: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/. Acesso em: 18 nov. 2026.
7. NEO4J. *Transition from NoSQL to graph database*. Disponível em: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/graphdb-vs-nosql/. Acesso em: 18 nov. 2026.
8. NEO4J. *Operations Manual — Introduction*. Disponível em: https://neo4j.com/docs/operations-manual/current/introduction/. Acesso em: 18 nov. 2026.
9. NEO4J. *Database administration*. Disponível em: https://neo4j.com/docs/operations-manual/current/database-administration/. Acesso em: 18 nov. 2026.
10. POSTGRESQL. *About*. Disponível em: https://www.postgresql.org/about/. Acesso em: 18 nov. 2026.
11. MONGODB. *Document data model*. Disponível em: https://www.mongodb.com/docs/manual/core/data-modeling-introduction/. Acesso em: 18 nov. 2026.
