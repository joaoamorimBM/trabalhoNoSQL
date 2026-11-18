# Tópico 2B — Cluster, hardware, nuvem e custo

> **Responsável:** Isaac · **Tempo de fala:** ~3 min
> Pesquisa conferida em 18/11/2026, direto na documentação oficial da Neo4j, AWS e Azure (e agregadores de preço quando a página oficial não abre).
> **Preços de nuvem mudam com frequência** — todos os valores abaixo valem para a data da consulta.

**Glossário rápido (para explicar à turma, se perguntarem):**

| Termo | Em uma frase |
|---|---|
| Cluster | Vários servidores trabalhando como um só banco, com cópias dos dados |
| Raft / consenso | Algoritmo que faz as cópias concordarem com a mesma ordem de transações, mesmo com falhas |
| Quórum | A maioria dos primários; sem ela, não há escrita |
| Líder / seguidor | Primário que recebe as escritas / primários que votam e confirmam |
| Secundário | Cópia extra só para leitura; não vota |
| *Transaction log* | Registro em ordem de todas as transações; é o que é replicado |
| Tabela de roteamento | Lista, enviada ao driver, de quem é o líder e quem atende leituras |
| Bookmark | Marcador da última transação vista; garante ler o que você mesmo gravou |
| Heap | Memória de trabalho do Java, onde as consultas executam |
| Page cache | Parte da RAM onde o Neo4j mantém o grafo para não ler do disco |
| SLA | Garantia de disponibilidade em contrato (ex.: 99,95% do tempo) |
| Zona de disponibilidade | Data center separado dentro da mesma região da nuvem |

## Slide 1 — Como um cluster Neo4j é montado

- **Só na Enterprise:** Neo4j em cada servidor → cada um recebe o endereço dos outros → `CREATE DATABASE` com a topologia
- **Primários** usam o consenso **Raft**: um **líder** recebe as escritas; os **seguidores** votam e confirmam
- Escrita confirmada quando a **maioria (quórum)** a registra no log
- **M = 2F + 1:** 3 primários aguentam 1 falha, 5 aguentam 2 (máx. 11) · sem maioria → **somente leitura**
- **Secundários:** não votam; puxam o *transaction log* de forma assíncrona e **escalam leituras** (máx. 20)

**Fala:** "O cluster existe só na Enterprise; a Community roda num servidor só. Cada servidor recebe o endereço dos outros, e o banco é criado dizendo quantas cópias primárias e secundárias terá. Os primários usam o Raft, um algoritmo de consenso: as cópias concordam com a mesma sequência de transações enquanto a maioria, o quórum, estiver de pé. Um primário é eleito líder e recebe as escritas; os seguidores votam e confirmam. A escrita só vale quando a maioria a registra. Daí a regra M = 2F + 1, em que M é o número de primários e F quantas falhas o banco aguenta: três primários aguentam a queda de um. Sem maioria, o banco fica somente leitura. Os secundários não votam: só distribuem as leituras."

**Imagem/diagrama:** imagens/cluster-neo4j.svg (diagrama próprio: aplicação → driver `neo4j://` → banco `social` com 3 primários em Raft + 2 secundários, 5 servidores)

**Detalhe da montagem (para responder perguntas):**
```properties
# neo4j.conf de cada servidor (muda só o endereço) — sintaxe da documentação atual (2026.10)
server.default_listen_address=0.0.0.0
server.default_advertised_address=server01.example.com
dbms.cluster.endpoints=server01.example.com:6000,server02.example.com:6000,server03.example.com:6000
initial.dbms.default_primaries_count=3
```
```properties
# Mesma coisa no Neo4j 5.26 LTS (a versão da nossa demo), com o discovery v2
server.default_listen_address=0.0.0.0
server.default_advertised_address=server01.example.com
dbms.cluster.discovery.v2.endpoints=server01.example.com:6000,server02.example.com:6000,server03.example.com:6000
dbms.cluster.discovery.version=V2_ONLY
initial.dbms.default_primaries_count=3
```
```cypher
SHOW SERVERS;                       // confere os membros e o estado (Free, Enabled...)
CREATE DATABASE social TOPOLOGY 3 PRIMARIES 2 SECONDARIES;
SHOW DATABASES;                     // mostra em que servidor cada cópia está e quem é o writer
```
```cypher
// Acrescentar um 6º servidor como secundário e aumentar a topologia
ENABLE SERVER '<serverId copiado do SHOW SERVERS>' OPTIONS {modeConstraint: 'SECONDARY'};
ALTER DATABASE social SET TOPOLOGY 3 PRIMARIES 3 SECONDARIES;
```
- `server.default_listen_address=0.0.0.0` faz o Neo4j escutar em todas as interfaces de rede. Sem isso, os membros não se enxergam.
- `modeConstraint` (`PRIMARY`, `SECONDARY` ou `NONE`) restringe em que modo um servidor pode hospedar bancos. O papel de cada cópia é definido por banco, na topologia.
- **Portas padrão:**
  - **Entre os servidores:**
    - 6000: descoberta do cluster.
    - 7000: tráfego do Raft.
    - 7688: roteamento no servidor, se estiver ativo.
  - **Para os clientes:**
    - 7687: Bolt, usada pelos drivers.
    - 7474/7473: HTTP/HTTPS do Browser.
  - **Backup:** 6362, que por padrão escuta só em localhost. Para um backup remoto, abrir só para a máquina de backup.
- **Memória no `neo4j.conf` (para a VM de 16 GiB):**
  - `server.memory.heap.initial_size=4g`
  - `server.memory.heap.max_size=4g`
  - `server.memory.pagecache.size=8g`
- Os servidores 4 e 5 usam a mesma lista de endpoints para encontrar o cluster. Os servidores presentes na primeira inicialização são habilitados automaticamente. Os que entram depois precisam de `ENABLE SERVER` **antes** do `CREATE DATABASE ... 2 SECONDARIES`.
- Cada cópia do banco fica num servidor: a documentação diz que três primários exigem "três servidores para hospedar cada cópia". Então 3 primários + 2 secundários = 5 servidores.

**Fontes:**
- Neo4j, *Operations Manual — Clustering: Introduction*: https://neo4j.com/docs/operations-manual/current/clustering/introduction/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Deploy a basic cluster*: https://neo4j.com/docs/operations-manual/current/clustering/setup/deploy/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual 5 — Deploy a basic cluster* (sintaxe da 5.26): https://neo4j.com/docs/operations-manual/5/clustering/setup/deploy/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Clustering glossary* (commit por quórum dos primários): https://neo4j.com/docs/operations-manual/current/clustering/glossary/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Managing servers* (`ENABLE SERVER`, `modeConstraint`, estados): https://neo4j.com/docs/operations-manual/current/clustering/servers/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Managing databases in a cluster* (`ALTER DATABASE ... SET TOPOLOGY`): https://neo4j.com/docs/operations-manual/current/clustering/databases/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Ports*: https://neo4j.com/docs/operations-manual/current/configuration/ports/ (acessado em 18/11/2026)

## Slide 2 — O papel de cada nó e o roteamento pelo driver

- **Um líder por banco** = única porta de escrita → o cluster **escala leituras, não escritas**
- Driver com `neo4j://` usa a **tabela de roteamento**: escrita → líder · leitura → seguidores e secundários
- Seguidores e secundários podem estar **atrasados** → os **bookmarks** garantem ler o que acabou de gravar
- `bolt://` = conexão direta, sem roteamento · no AuraDB o endereço é `neo4j+s://` (criptografado)

**Fala:** "Um detalhe importante: cada banco tem um único líder, então o cluster multiplica a capacidade de leitura, não a de escrita. Quem distribui as consultas é o próprio driver: com o endereço neo4j://, ele pede ao cluster uma tabela de roteamento, manda as escritas para o líder e espalha as leituras pelos seguidores e secundários. Como eles podem estar um pouco atrasados, o driver repassa bookmarks, e quem posta algo vê o próprio post. A nossa demo já separa leitura e escrita desse jeito."

**Imagem/diagrama:** o mesmo imagens/cluster-neo4j.svg do slide 1. Na fala, apontar a seta vermelha (escrita → líder) e as azuis (leitura → seguidores e secundários).

**Se o professor perguntar (não vai no slide):**
- *"Com 5 primários, quantos precisam ter a escrita antes do commit? E se a rede partir em 3 e 2?"* A maioria, ou seja, 3 (o líder + 2). O lado com 3 elege líder e continua aceitando escritas; o lado com 2 fica somente leitura. Com 3 primários, basta o líder + 1.
- *"Qual a diferença entre seguidor e secundário? Um secundário pode virar líder?"* Não. "Só primários podem ser o writer de um banco." Seguidores são primários: votam e entram no quórum. Secundários só recebem cópias assíncronas e não votam.
- *"O líder cai no meio de um commit. A escrita se perde?"* O que já foi registrado pela maioria não se perde.
  - **Retry:** o driver repete sozinho, quando a falha é transitória, as consultas feitas com `execute_query` e as transações gerenciadas (`execute_read` / `execute_write`). A nova tentativa vai para o novo líder. Transações explícitas e `session.run()` não são repetidas.
  - **Na nossa demo:** ela usa `execute_query`, com no máximo 5 s de novas tentativas (`max_transaction_retry_time=5` em `app/db.py`). Em cluster, 5 s seria pouco: por padrão, o cluster leva de 20 a 23 s para detectar a queda do líder (`dbms.cluster.raft.leader_failure_detection_window`), e só depois há eleição. Em produção aumentaríamos esse limite para passar desse tempo. Os 5 s servem para a demo não travar num servidor único.
  - **Cuidado:** o cliente pode receber erro mesmo que a escrita tenha sido confirmada (o líder caiu depois do quórum e antes de responder). Aí a nova tentativa repetiria a escrita. Por isso a documentação diz que "as funções de transação precisam ser idempotentes".
  - **Como fazer certo:** `MERGE (p:Post {id: $id})`, com o id gerado **na aplicação, antes** da transação (por exemplo, `uuid.uuid4()` no Python), com uma **constraint de unicidade** em `Post.id` (a demo já tem: `post_id` em `cypher/01_constraints.cypher`). Assim a nova tentativa encontra o post já gravado em vez de criar outro. Se o id fosse gerado dentro do Cypher, cada tentativa teria um id novo e o `MERGE` não ajudaria.
- *"A demo de vocês é idempotente?"* Resposta honesta:
  - **Post:** não totalmente.
    - A constraint em `Post.id` já existe. O que falta é gerar o id no Python e usar `MERGE`.
    - Como o id vem de `randomUUID()` dentro do Cypher, cada tentativa gera um id novo, e a constraint não impede a duplicação.
    - Num cluster, uma falha do líder bem no commit poderia duplicar o post. No nosso servidor único isso praticamente não ocorre.
  - **Usuário:** o `username` tem constraint de unicidade, então um retry não duplica. Mas ele receberia `ConstraintError`, e a tela mostraria o erro 409 "Já existe um usuário com esse username" mesmo com o cadastro gravado. O dado fica certo e a resposta fica errada.
  - **Exemplo positivo:** seguir e curtir já usam `MERGE` na relação, então são idempotentes.
  - **Ponto forte:** o `execute_query` manda tudo para o líder por padrão. A demo marca `RoutingControl.READ` nas leituras, e por isso um cluster distribuiria as leituras sem mudar o código.
- *"Em termos de CAP, onde fica o cluster?"*
  - **Escritas:** priorizam consistência (CP). Só são confirmadas com quórum e, sem maioria, o banco recusa escritas.
  - **Leituras fora do líder:** seguidores e secundários podem estar atrasados, então a consistência é eventual. Os bookmarks garantem consistência causal. Durante uma partição, o lado minoritário continua respondendo leituras, possivelmente antigas.
  - **Em PACELC:** escrita PC/EC, porque paga a latência do quórum mesmo sem falha. Leitura EL.
- *"Se a leitura vai para um seguidor que já deu ack, ela é garantidamente atual? O cluster é linearizável?"* Não. O ack só significa que a transação está no log do seguidor, que pode ainda não tê-la aplicado. Nenhuma leitura é prometida como linearizável. A garantia documentada é a consistência causal, via bookmarks. Mesmo no líder pode haver uma janela curta, durante a troca de liderança, em que a leitura está atrasada (não verificamos se o Neo4j usa algum mecanismo que impeça isso).
- *"Como o bookmark funciona por baixo?"* O bookmark marca a última transação que o cliente viu. O servidor que recebe a próxima consulta espera até ter aplicado aquela transação (ou dá timeout) antes de responder.
- *"Por que uma escrita confirmada não se perde quando o líder cai? O que impede dois líderes?"*
  - Duas maiorias sempre têm pelo menos um servidor em comum (interseção de quóruns).
  - Na eleição, um servidor só vota num candidato cujo log esteja pelo menos tão atualizado quanto o seu. Então quem vence já tem todas as escritas confirmadas.
  - Um líder antigo isolado não consegue confirmar nada sem maioria. Por isso não há dois líderes confirmando escritas ao mesmo tempo (*split brain*).
  - (Esse é o funcionamento padrão do Raft.)
- *"O commit por maioria resiste se todas as máquinas perderem energia juntas?"* Depende de os servidores gravarem no disco antes de confirmar, e não verificamos esse detalhe na documentação. A resposta honesta é "precisa ser verificado".
- *"Com 4 primários, quantas falhas o cluster tolera?"* Uma, a mesma coisa que com 3, mas com quórum de 3: a escrita fica mais lenta sem ganho de disponibilidade. Por isso se usa número ímpar. E M = 2F + 1 vale para falhas por parada (*crash*), não para servidores maliciosos (falhas bizantinas).
- *"O líder é do cluster inteiro?"* Não: cada banco tem seu próprio grupo Raft e seu próprio líder. Bancos diferentes podem ter líderes em servidores diferentes.
- *"Por que não particionar o grafo por chave, como o Cassandra ou o MongoDB?"* Dividir o grafo em partes **de tamanho parecido** cortando o mínimo de relações (particionamento balanceado) é um problema NP-difícil. Numa rede social, as relações cruzam qualquer divisão (amigos em outra região). Cada travessia entre partições vira uma chamada de rede e perde a vantagem de ir de um nó ao vizinho direto, sem índice. Por isso o Neo4j replica o grafo inteiro em cada cópia.
- *"Como escalar escritas numa rede social com milhões de posts?"* Dentro de um banco, toda escrita passa pelo líder. As opções oficiais são:
  - **Bancos compostos (Enterprise):** dividir os dados em bancos com o mesmo modelo (por exemplo, por região), cada um com seu líder em servidores diferentes, e consultar tudo com uma única query Cypher. Restrição: uma transação pode ler de vários bancos, mas só escreve em um. Não existe no Aura nem na Community.
  - **Property sharding (Infinigraph, desde a 2025.12):** espalha as propriedades em vários *shards*, mas **não divide a estrutura do grafo**: o *graph shard* guarda todos os nós e relações, sem as propriedades. Exige assinatura à parte, e as transações continuam coordenadas por um grupo Raft.
- *"A aplicação precisa tratar os bookmarks?"* Não: o driver faz isso sozinho dentro de uma sessão, e o `execute_query` encadeia as chamadas do mesmo driver. Entre sessões diferentes, sem passar o bookmark (`session.last_bookmarks()`), o usuário pode sim ler um dado atrasado.
- *"Por que a demo usa `neo4j://` num servidor só?"* Funciona: a tabela de roteamento tem um único membro, que é ao mesmo tempo escritor e leitor. E o mesmo código serve para cluster ou Aura sem mudança, só trocando a URI (no Aura, `neo4j+s://`). A demo já marca cada consulta como leitura ou escrita (`RoutingControl.READ` / `WRITE` em `app/db.py`).
- *"Por que não usar 2 primários?"* Com 2, a maioria é 2: se um cair, não há maioria e o banco fica somente leitura. Por isso o mínimo para tolerar uma falha é 3.
- *"Por que 11 primários no máximo?"* A documentação fixa o máximo em 11 e desaconselha chegar perto disso, porque cada escrita precisa da maioria dos primários: mais primários deixam a escrita mais lenta. Ela diz que 3 bastam para a maioria dos casos.
- *"As leituras podem ir para o líder?"* Na configuração padrão, não: todos os servidores menos o líder aparecem como leitores na tabela de roteamento.
- *"A demo de vocês roda em cluster?"* Não: roda num Neo4j local (servidor único) e o plano B é o AuraDB Free. O cluster é o que se usaria em produção.

**Fontes:**
- Neo4j, *Operations Manual — Clustering: Introduction*: https://neo4j.com/docs/operations-manual/current/clustering/introduction/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Leadership, routing and load balancing*: https://neo4j.com/docs/operations-manual/current/clustering/setup/routing/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Managing servers* (`modeConstraint`): https://neo4j.com/docs/operations-manual/current/clustering/servers/ (acessado em 18/11/2026)
- Neo4j, *Python Driver Manual — Advanced connection information* (`neo4j+s` é o padrão do Aura): https://neo4j.com/docs/python-manual/current/connect-advanced/ (acessado em 18/11/2026)
- Neo4j, *Python Driver Manual — Coordinate parallel transactions (bookmarks)*: https://neo4j.com/docs/python-manual/current/bookmarks/ (acessado em 18/11/2026)
- Neo4j, *Python Driver Manual — Run your own transactions* (retry automático, idempotência): https://neo4j.com/docs/python-manual/current/transactions/ (acessado em 18/11/2026)
- Neo4j, *Python Driver Manual — Query the database* (retry no `execute_query`): https://neo4j.com/docs/python-manual/current/query-simple/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Composite databases: Concepts*: https://neo4j.com/docs/operations-manual/current/scalability/composite-databases/concepts/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Property sharding overview*: https://neo4j.com/docs/operations-manual/current/scalability/sharded-property-databases/overview/ (acessado em 18/11/2026)

## Slide 3 — Hardware e configuração média

| | Servidor (nuvem) | Servidor (local) | Desenvolvimento |
|---|---|---|---|
| CPU | mín. 2 vCPU · recom. 16+ | x86-64 ou ARM64 | mín. Core i3 · recom. Core i7 |
| RAM | mín. 2 GB (depende da carga) | mín. 8 GB | mín. 2 GB · recom. 16 GB |
| Disco | mín. 10 GB · NVMe recom. | SSD > 5.000 IOPS · NVMe recom. | mín. 10 GB · SSD/NVMe recom. |

- RAM ≈ SO + **heap** + **page cache** (≈ dados × 1,2)
- **Configuração média (estimativa nossa):** 4 vCPU, 16 GiB (~8 page cache, ~4 heap), SSD NVMe

**Fala:** "O mínimo para rodar o Neo4j é baixo: 2 vCPUs e 2 GB de RAM em nuvem, mas a documentação recomenda 16 vCPUs ou mais e disco NVMe. O ponto principal é a memória: o heap, que é a memória de trabalho do Java, onde as consultas executam, e o page cache, onde o grafo fica carregado. O ideal é o page cache caber o grafo inteiro com uns 20% de folga, para as travessias acontecerem na RAM, sem ir ao disco. Para uma rede social de porte médio, estimamos 4 vCPUs e 16 GB."

**Imagem/diagrama:** (opcional) barra horizontal mostrando os 16 GiB divididos em SO | heap | page cache

**Observações (para responder perguntas):**
- **Detalhes que saíram do slide:**
  - SO: Linux (Ubuntu, Debian, RHEL...) ou Windows Server.
  - Java 21/25 para o Neo4j 2025.10+; Java 17/21 para o 5.26 LTS, que é a versão da demo.
  - A fórmula completa é RAM ≈ SO (~1 GB) + heap + page cache, com page cache ≈ (dados + índices nativos) × 1,2.
  - Swap desligado.
- A configuração média é uma **estimativa nossa**, derivada da regra de memória da documentação, para um banco de até ~6–7 GiB de dados e índices (page cache de ~8 GiB com 20% de folga).
  - Conta da memória: 8 (page cache) + 4 (heap) + 1 (SO) = 13 de 16 GiB. Sobram ~3 GiB para a JVM fora do heap (metaspace, pilhas de threads, buffers de rede) e para os índices Lucene e vetoriais. A memória das transações sai do próprio heap de 4 GiB: é o padrão recomendado, e o limite é `dbms.memory.transaction.total.max`.
  - *"E se o page cache for menor que o grafo?"* Partes do grafo ficam fora da RAM. As travessias passam a ler do disco (falhas de página) e dependem do IOPS. Por isso a documentação pede SSD acima de 5.000 IOPS em servidor local e recomenda NVMe conectado à máquina em nuvem. Caber o grafo inteiro é o ideal, não uma exigência: se o **conjunto de trabalho** (usuários ativos, posts recentes) couber na RAM, quase não há leitura de disco.
  - **Ligação com o paradigma:** ir de um nó ao vizinho sem índice só é rápido se os registros de nós e relações estiverem na RAM. Por isso o page cache deve caber o grafo.
  - Conferir com `neo4j-admin server memory-recommendation --memory=16g`.
- *"A documentação recomenda 16+ vCPU em nuvem. Por que 4?"* O mínimo é 2 vCPU, e a recomendação depende da carga. Para um banco pequeno com poucas consultas simultâneas, 4 vCPU bastam para começar. Se a carga crescer, a VM pode ser trocada por uma maior.
- *"O disco gp3 da AWS (3.000 IOPS de base) atende os > 5.000 IOPS?"* Não na configuração base. Na AWS dá para provisionar mais IOPS pagando à parte (US$ 0,005 por IOPS-mês acima de 3.000), e a documentação recomenda NVMe local em nuvem.
- *"E se o banco tiver 30 GB?"* Page cache ≈ 30 × 1,2 = 36 GB, mais heap e SO. A máquina de 16 GiB não serve: seria preciso algo na faixa de 64 GiB de RAM (estimativa).
- O fator 1,2 é o exemplo da documentação (20% de folga para crescimento). O índice vetorial fica na memória do SO, fora do page cache. Para os índices Lucene (texto), a documentação manda conferir se cabem na memória que sobra depois do page cache e do heap.
- Java: a tabela de compatibilidade da documentação lista Java 21 e 25 para o Neo4j 2025.10 em diante. A nossa demo usa o **Neo4j Community 5.26 LTS** (ver `07-aplicacao-pratica/README.md`), que roda com **Java 17 ou 21**, pela mesma tabela.

**Fontes:**
- Neo4j, *Operations Manual — System requirements*: https://neo4j.com/docs/operations-manual/current/installation/requirements/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Memory configuration*: https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/ (acessado em 18/11/2026)

## Slide 4 — Nuvem e custo: AuraDB × VM própria

- **AuraDB** (gerenciado) em **AWS, Google Cloud ou Azure** · também pelos marketplaces de cada nuvem
- **Free:** US$ 0, 200 mil nós / 400 mil relações, sem SLA · **Professional:** US$ 0,09/GB/h · **Business Critical:** US$ 0,20/GB/h, SLA 99,95%
- **VM própria:** imagens nos marketplaces ou templates (CloudFormation, Terraform, ARM)

| Opção (16 GB de RAM, 730 h/mês · VM = só a máquina, disco à parte) | Custo/mês |
|---|---|
| AuraDB Professional (uma zona) | ≈ **US$ 1.051** |
| AuraDB Business Critical (multizona) | ≈ **US$ 2.336** |
| VM AWS m6i.xlarge, 4 vCPU (Community, grátis) | ≈ **US$ 140** |
| VM Google Cloud n2-standard-4, 4 vCPU (Community) | ≈ **US$ 142** de tabela (≈ US$ 113 com desconto automático) |
| VM Azure D4s v5, 4 vCPU (Community) | ≈ **US$ 140** |
| Cluster do diagrama: 5 × AWS + disco (Enterprise) | ≈ US$ 721 **+ licença** (sob consulta) |

*Comparação feita pela RAM: não verificamos quantas vCPU o Aura entrega com 16 GB. Preços de tabela, sem descontos de reserva.*

**Fala:** "Na nuvem há dois caminhos. O primeiro é o AuraDB, o Neo4j como serviço, contratado direto ou pelo marketplace da nuvem. A Neo4j cuida de backup e atualização, e o plano Business Critical garante em contrato, o SLA, 99,95% de disponibilidade, com cópias em várias zonas, que são data centers separados. O plano gratuito é o nosso plano B da demo. O segundo caminho é uma máquina virtual com a Community, que é gratuita: com 4 vCPUs e 16 GB, sai por uns 140 dólares por mês de tabela, contra mil no AuraDB Professional. Mas não é igual por igual: a VM não tem backup nem alta disponibilidade, e o cluster do diagrama sai por uns 720 dólares mais a licença Enterprise."

**Imagem/diagrama:** a própria tabela de custo

**Como a conta foi feita (para responder perguntas):**
- **AuraDB:** preço/GB/hora × GB × 730 h. 0,09 × 16 × 730 = 1.051,20; 0,20 × 16 × 730 = 2.336,00. Os preços são "a partir de" e podem variar por região e provedor. Os mínimos são 1 GB no Professional (≈ US$ 66) e 2 GB no Business Critical (≈ US$ 292).
- **VMs (Linux, sob demanda, só a máquina):**
  - AWS m6i.xlarge (4 vCPU, 16 GiB) a US$ 0,192/h × 730 = 140,16, em US East (N. Virginia). Esse preço consta no arquivo de preços oficial que a página do EC2 carrega.
  - Google Cloud n2-standard-4 (4 vCPU, 16 GB) a US$ 0,1942/h × 730 = 141,77. É o preço de tabela em us-central1. O Google aplica **automaticamente** o desconto por uso contínuo, de até 20% nas N2 quando a máquina fica ligada o mês todo: 141,77 × 0,8 ≈ 113.
  - Azure D4s v5 (4 vCPU, 16 GiB) a US$ 0,192/h × 730 = 140,16, na região East US (API oficial de preços do Azure).
- **Disco:** à parte nas linhas de VM (o AuraDB já inclui armazenamento). Na AWS, 50 GiB gp3 × US$ 0,08/GiB-mês = 4,00 (US East), valor incluído só na linha do cluster. O disco no Google Cloud e no Azure não foi pesquisado.
- **Cluster do diagrama (3 primários + 2 secundários):** 5 × (140,16 + 4,00) = 720,80, mais a licença Enterprise, que é sob consulta. O mínimo para tolerar uma falha, com 3 primários e sem secundários, seria 3 × 144,16 = 432,48. Sem contar tráfego de rede, backup e o tempo de quem administra.
- **Edição:** as VMs isoladas usam a **Community** (gratuita, servidor único, sem cluster). O cluster exige a **Enterprise**, que é licenciada.
- **Comparação justa:**
  - O cluster de VMs (alta disponibilidade feita por nós) se compara com o **Business Critical**, não com o Professional.
  - Para isso, as VMs precisam ficar em **zonas de disponibilidade diferentes**. O tráfego entre zonas é cobrado à parte e não entrou na conta.
  - Nos 16 GiB da VM ainda é preciso dividir a RAM entre SO, heap e page cache.
- **GB × GiB:** o Aura cobra por GB de memória e as VMs são vendidas em GiB (16 GiB ≈ 17,2 GB). Para esta comparação a diferença é desprezível. A comparação é feita **pela RAM**; não verificamos quantas vCPU o Aura entrega com 16 GB.
- **Marketplaces do AuraDB:** a cobrança vai na conta do provedor; os planos variam por nuvem (AWS e Azure: Professional; Google Cloud: Professional e Business Critical). Créditos de marketplace não pagam o Aura.
- **Limite do Free:** a documentação oficial (*Quotas and limits*) traz 200 mil nós, 400 mil relações, 1 GB de armazenamento, 1 banco, sem SLA e sem alta disponibilidade. A página comercial do AuraDB Free ainda mostra números antigos (50 mil / 175 mil); a documentação é a referência. Da página do AuraDB Free vêm "sem cartão" e "pausa após 3 dias sem uso". "Uma instância Free por conta" vem do guia de criação de instância do Aura.
- **Sobre as fontes de preço:**
  - AWS e Azure foram conferidos em fontes oficiais: o arquivo de preços da página do EC2 e a API de preços do Azure.
  - O Google Cloud veio de um agregador (gcloud-compute.com), porque a tabela oficial não abriu automaticamente. Vale abrir https://cloud.google.com/compute/vm-instance-pricing antes de apresentar.

**Fontes:**
- Neo4j, *Pricing*: https://neo4j.com/pricing/ (acessado em 18/11/2026)
- Neo4j, *Aura — Quotas and limits*: https://neo4j.com/docs/aura/quotas-and-limits/ (acessado em 18/11/2026)
- Neo4j, *AuraDB Free*: https://neo4j.com/free-graph-database/ (acessado em 18/11/2026)
- Neo4j, *Aura — Creating an instance* (uma instância Free por conta): https://neo4j.com/docs/aura/classic/auradb/getting-started/create-database/ (acessado em 18/11/2026)
- Neo4j, *Aura with cloud provider marketplaces*: https://neo4j.com/docs/aura/cloud-providers/ (acessado em 18/11/2026)
- Neo4j, *Operations Manual — Cloud deployments*: https://neo4j.com/docs/operations-manual/current/cloud-deployments/ (acessado em 18/11/2026)
- AWS, *Amazon EC2 On-Demand Pricing* (página oficial): https://aws.amazon.com/ec2/pricing/on-demand/ (acessado em 18/11/2026)
- Vantage, *m6i.xlarge pricing* (dados da AWS, us-east-1): https://instances.vantage.sh/aws/ec2/m6i.xlarge (acessado em 18/11/2026)
- gcloud-compute.com, *n2-standard-4* (dados do Google Cloud, us-central1): https://gcloud-compute.com/n2-standard-4.html (acessado em 18/11/2026)
- Google Cloud, *Sustained use discounts* (automático, até 20% nas N2): https://docs.cloud.google.com/compute/docs/sustained-use-discounts (acessado em 18/11/2026)
- Microsoft, *Azure Retail Prices API* (Standard_D4s_v5, eastus): https://prices.azure.com/api/retail/prices (acessado em 18/11/2026)
- AWS, *Amazon EBS pricing* (página oficial de preços do disco): https://aws.amazon.com/ebs/pricing/ (acessado em 18/11/2026)
- AWS, *Comparing Amazon EBS volume types gp2 and gp3* (valor do gp3 em US East): https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-storage-compare-volume-types.html (acessado em 18/11/2026)

## Referências do tópico 2B (para o slide final de referências)

1. NEO4J. *Operations Manual — Clustering: Introduction*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/introduction/. Acesso em: 18 nov. 2026.
2. NEO4J. *Operations Manual — Deploy a basic cluster*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/setup/deploy/. Acesso em: 18 nov. 2026.
3. NEO4J. *Operations Manual 5 — Deploy a basic cluster*. Disponível em: https://neo4j.com/docs/operations-manual/5/clustering/setup/deploy/. Acesso em: 18 nov. 2026.
4. NEO4J. *Operations Manual — Managing servers*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/servers/. Acesso em: 18 nov. 2026.
5. NEO4J. *Operations Manual — Clustering glossary*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/glossary/. Acesso em: 18 nov. 2026.
6. NEO4J. *Operations Manual — Leadership, routing and load balancing*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/setup/routing/. Acesso em: 18 nov. 2026.
7. NEO4J. *Python Driver Manual — Coordinate parallel transactions*. Disponível em: https://neo4j.com/docs/python-manual/current/bookmarks/. Acesso em: 18 nov. 2026.
8. NEO4J. *Python Driver Manual — Run your own transactions*. Disponível em: https://neo4j.com/docs/python-manual/current/transactions/. Acesso em: 18 nov. 2026.
9. NEO4J. *Operations Manual — Composite databases: Concepts*. Disponível em: https://neo4j.com/docs/operations-manual/current/scalability/composite-databases/concepts/. Acesso em: 18 nov. 2026.
10. NEO4J. *Operations Manual — Property sharding overview*. Disponível em: https://neo4j.com/docs/operations-manual/current/scalability/sharded-property-databases/overview/. Acesso em: 18 nov. 2026.
11. NEO4J. *Operations Manual — System requirements*. Disponível em: https://neo4j.com/docs/operations-manual/current/installation/requirements/. Acesso em: 18 nov. 2026.
12. NEO4J. *Operations Manual — Memory configuration*. Disponível em: https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/. Acesso em: 18 nov. 2026.
13. NEO4J. *Operations Manual — Cloud deployments*. Disponível em: https://neo4j.com/docs/operations-manual/current/cloud-deployments/. Acesso em: 18 nov. 2026.
14. NEO4J. *Pricing*. Disponível em: https://neo4j.com/pricing/. Acesso em: 18 nov. 2026.
15. NEO4J. *Aura — Quotas and limits*. Disponível em: https://neo4j.com/docs/aura/quotas-and-limits/. Acesso em: 18 nov. 2026.
16. NEO4J. *AuraDB Free*. Disponível em: https://neo4j.com/free-graph-database/. Acesso em: 18 nov. 2026.
17. NEO4J. *Aura — Creating an instance*. Disponível em: https://neo4j.com/docs/aura/classic/auradb/getting-started/create-database/. Acesso em: 18 nov. 2026.
18. NEO4J. *Aura with cloud provider marketplaces*. Disponível em: https://neo4j.com/docs/aura/cloud-providers/. Acesso em: 18 nov. 2026.
19. AMAZON WEB SERVICES. *Amazon EC2 On-Demand Pricing*. Disponível em: https://aws.amazon.com/ec2/pricing/on-demand/. Acesso em: 18 nov. 2026.
20. VANTAGE. *m6i.xlarge — Amazon EC2 instance pricing*. Disponível em: https://instances.vantage.sh/aws/ec2/m6i.xlarge. Acesso em: 18 nov. 2026.
21. GCLOUD-COMPUTE.COM. *n2-standard-4*. Disponível em: https://gcloud-compute.com/n2-standard-4.html. Acesso em: 18 nov. 2026.
22. MICROSOFT. *Azure Retail Prices API*. Disponível em: https://prices.azure.com/api/retail/prices. Acesso em: 18 nov. 2026.
23. AMAZON WEB SERVICES. *Comparing Amazon EBS volume types gp2 and gp3*. Disponível em: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-storage-compare-volume-types.html. Acesso em: 18 nov. 2026.
24. AMAZON WEB SERVICES. *Amazon EBS pricing*. Disponível em: https://aws.amazon.com/ebs/pricing/. Acesso em: 18 nov. 2026.
25. NEO4J. *Python Driver Manual — Advanced connection information*. Disponível em: https://neo4j.com/docs/python-manual/current/connect-advanced/. Acesso em: 18 nov. 2026.
26. GOOGLE CLOUD. *Sustained use discounts*. Disponível em: https://docs.cloud.google.com/compute/docs/sustained-use-discounts. Acesso em: 18 nov. 2026.
27. NEO4J. *Operations Manual — Managing databases in a cluster*. Disponível em: https://neo4j.com/docs/operations-manual/current/clustering/databases/. Acesso em: 18 nov. 2026.
28. NEO4J. *Operations Manual — Ports*. Disponível em: https://neo4j.com/docs/operations-manual/current/configuration/ports/. Acesso em: 18 nov. 2026.
29. NEO4J. *Python Driver Manual — Query the database*. Disponível em: https://neo4j.com/docs/python-manual/current/query-simple/. Acesso em: 18 nov. 2026.
