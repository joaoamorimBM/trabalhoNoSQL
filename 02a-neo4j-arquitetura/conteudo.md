# Tópico 2A — Neo4j: características e arquitetura

> **Responsável:** Hamilton · **Tempo de fala:** ~1,5 min
> Pesquisa conferida em 18/11/2026. Não há benchmark próprio; edições e limites mudam por versão.

## Slide 1 — Origem e posição de mercado

- Protótipo em 2000, na Suécia · primeira implantação 24×7 em 2003
- **2007:** empresa formada e Neo4j aberto sob **GPL** como o primeiro banco de grafos open source
- **2010:** versão 1.0 · **2011:** sede para o Vale do Silício · **2017:** empresa passa a se chamar **Neo4j, Inc.**
- Nome = "Neo" (novo) + "4j" (*for Java*) · implementado em **Java**, acessível por drivers (Python, JS, Java, Go, .NET) e pelo protocolo **Bolt**

**Fala:**
"O Neo4j nasceu de um problema prático: os fundadores tocavam um sistema de gestão de conteúdo e perdiam tempo modelando dados muito conectados em tabelas. O protótipo é de 2000, a primeira implantação em produção 24 por 7 é de 2003, e em 2007 a empresa foi formalizada na Suécia e o Neo4j foi aberto sob GPL. Veio a versão 1.0 em 2010 e, em 2011, a sede foi para o Vale do Silício. O nome vem de 'neo', novo, com o '4j' de 'for Java', porque é implementado em Java — mas a aplicação acessa por drivers, inclusive o driver de Python que o João Pedro usa na demo."

**Imagem/diagrama:** (a criar) `imagens/linha-do-tempo.svg` — 2000 → 2003 → 2007 → 2010 → 2011 → 2017.

**Fontes:**
- Neo4j, *Company — quick history*: https://neo4j.com/company (acessado em 18/11/2026)
- Wikipédia, *Neo4j* (origem do nome e fundadores): https://en.wikipedia.org/wiki/Neo4j (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Introduction* (drivers e protocolo Bolt): https://neo4j.com/docs/operations-manual/current/introduction/ (acessado em 18/11/2026)

## Slide 2 — Características e edições

- **ACID:** atomicidade, consistência, isolamento e durabilidade · isolamento padrão *read-committed* · *locks* de escrita por nó e por relacionamento
- **Cypher:** consultas por padrões no estilo ASCII art (`(a)-[:SEGUE]->(b)`) · origem do **openCypher** (2015)
- **GQL:** ISO/IEC 39075:2024, padrão ISO para grafos de propriedades (publicado em abril/2024); o Cypher evolui para ser compatível com GQL
- **Esquema opcional:** índices e *constraints* entram quando trazem benefício
- **Community (GPLv3, instância única) × Enterprise (cluster, backup online, RBAC/LDAP) × Infinigraph (sharding)** · **Aura** = serviço gerenciado

**Fala:**
"Como banco transacional, o Neo4j é ACID: se uma parte da transação falha, nada é aplicado, e o commit garante durabilidade. O isolamento padrão é read-committed, com locks de escrita no nível de nó e de relacionamento. A linguagem é o Cypher, que descreve o padrão do grafo com uma sintaxe quase desenhada — parênteses para nós, colchetes para relacionamentos. O Cypher foi aberto como openCypher em 2015 e serviu de base para o GQL, que virou norma ISO em abril de 2024. Sobre licença: a Community é open source sob GPLv3 e roda em instância única; a Enterprise é comercial e traz cluster, backup online e controle de acesso; e o Aura é a versão gerenciada na nuvem, que o Isaac vai detalhar."

**Imagem/diagrama:** (a criar) `imagens/cypher-exemplo.svg` — o mesmo padrão em desenho e em Cypher.

**Fontes:**
- Neo4j, *Database internals and transactional behavior* (ACID, isolamento, locks): https://neo4j.com/docs/operations-manual/current/database-internals/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Introduction* (edições e licenças): https://neo4j.com/docs/operations-manual/current/introduction/ (acessado em 18/11/2026)
- Neo4j, *Cypher overview*: https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/ (acessado em 18/11/2026)
- ISO, *ISO/IEC 39075:2024 — GQL*: https://www.iso.org/standard/76120.html (acessado em 18/11/2026)
- Neo4j, *GQL conformance*: https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance (acessado em 18/11/2026)

## Slide 3 — Arquitetura interna

- **Armazenamento nativo de grafo:** arquivos separados para nós, relacionamentos e propriedades, com registros de tamanho fixo encadeados por ponteiros → base do *index-free adjacency*
- **Page cache:** mantém páginas desses arquivos em RAM; aquece sob demanda e é dimensionado por configuração (`server.memory.pagecache.size`)
- **Transaction log (write-ahead):** grava antes de aplicar, garante durabilidade e permite recuperação após queda; *checkpoints* descarregam o cache e permitem podar o log
- **Índices:** estruturas à parte (B-tree, texto completo, vetorial) para **achar o ponto de partida**; a travessia em si não usa índice

**Fala:**
"Por dentro, o Neo4j guarda o grafo de forma nativa: existem arquivos próprios para nós, para relacionamentos e para propriedades, com registros de tamanho fixo ligados por ponteiros. É essa organização que sustenta o index-free adjacency que eu citei no começo. O page cache mantém páginas desses arquivos na memória e é o principal parâmetro de desempenho — daí a regra de dar RAM suficiente para o conjunto de dados ativo. Para durabilidade existe o transaction log, um log write-ahead: ele é gravado antes da aplicação, serve para recuperar o banco depois de uma queda e é aparado nos checkpoints. Por fim, os índices existem para encontrar o nó inicial de uma consulta; o caminho entre os nós é percorrido por ponteiros, não por índice. Com isso eu fecho e passo para o Isaac, que fala de cluster, hardware e nuvem."

**Imagem/diagrama:** (a criar) `imagens/arquitetura-interna.svg` — store files (node/relationship/property) → page cache → consulta Cypher, com transaction log ao lado.

**Fontes:**
- Neo4j, *Database internals — store formats*: https://neo4j.com/docs/operations-manual/current/database-internals/store-formats/ (acessado em 18/11/2026)
- Neo4j, *Database internals — transaction logs*: https://neo4j.com/docs/operations-manual/current/database-internals/transaction-logs/ (acessado em 18/11/2026)
- Neo4j, *Disks, RAM and other tips* (page cache e checkpoints): https://neo4j.com/docs/operations-manual/current/performance/disks-ram-and-other-tips/ (acessado em 18/11/2026)
- Neo4j, *Cypher Manual — Indexes*: https://neo4j.com/docs/cypher-manual/current/indexes/ (acessado em 18/11/2026)
