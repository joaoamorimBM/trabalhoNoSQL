# Roteiro da demo ao vivo (~3 min)

> **Responsável:** Vinícius (roteiro) · **Executa:** João Pedro
>
> Os resultados esperados abaixo foram calculados a partir do `02_seed.cypher` atual.
> Se o seed mudar, confira de novo no ensaio.

## Antes de começar (no dia, antes da aula)

1. Neo4j ligado (`bin\neo4j.bat console`) e app rodando (`python run.py` → <http://localhost:5000>).
2. **Recarregar o banco do zero:** `python scripts/seed.py --limpar`
   (apaga o `prof.demo` que sobrou de ensaios; sem isso o CREATE do passo 2 dá erro 409).
3. Conferir a saída do seed: `Interesse: 18 · Post: 60 · Usuario: 30`.
4. Deixar abertos: aba do app, aba do Neo4j Browser (<http://localhost:7474>) com o
   `cypher/03_crud_demo.cypher` carregado (plano B) e o zoom do navegador em 125% para a turma enxergar.
5. Ter o `.env` do AuraDB Free à mão (contingência se o PC falhar).

## Passo a passo (app web)

O painel **"Cypher executado"** (à direita) mostra a consulta de cada clique: apontar para ele em todos os passos.

| # | Operação | O que fazer na tela | Resultado esperado | Fala (João Pedro) |
|---|---|---|---|---|
| 0 | Transição | (Vinícius) "Agora o João Pedro mostra isso funcionando." | — | — |
| 1 | — | Mostrar o grafo já carregado. Clicar em **Íris Melo** na lista. Em "Graus de separação", escolher **Íris Melo → Fernanda Lopes** e clicar **Buscar**. | Perfil da Íris com 4 interesses. Sugestões: **Carla Mendes** em 1º (segue: Ana, Marina · curte: IA, Tecnologia). Caminho: **5 graus** (o caminho exato pode variar quando há empate). | "Essa é a nossa rede: 30 pessoas, posts, curtidas e interesses, tudo em nós e arestas. A Íris, estudante em Fortaleza, está a 5 graus da Fernanda, professora em São Luís." |
| 2 | **CREATE** (nó) | Em "Criar usuário": username `prof.demo` · nome `Professor Demo` · cidade `Fortaleza` · bio `Criado ao vivo na apresentação` · interesses `Tecnologia, Livros` → **Criar**. | Toast "Usuário Professor Demo criado." Perfil aberto, 0 seguidores. No painel: `CREATE (u:Usuario ...)` + `MERGE ... INTERESSADO_EM`. | "Criei um nó Usuario e liguei ele a dois nós Interesse que já existiam. O MERGE reaproveita o interesse em vez de duplicar." |
| 3 | **CREATE** (aresta) | Em "Seguindo", escolher **Ana Souza** no seletor → **Seguir**. Depois, em "Publicar": `Olá, turma de NoSQL!` → **Publicar**. | Ana aparece em "Seguindo". Post novo em "Meus posts". | "Seguir alguém é só criar uma aresta SEGUE com a data. O post é outro nó, ligado por PUBLICOU." |
| 4 | **READ** | Olhar **Sugestões de quem seguir**. Clicar na aba **Feed**. Em "Graus de separação": **Professor Demo → Jonas Pinto** → **Buscar**. | Sugestões, nesta ordem: **Marina Castro** (segue: Ana · curte: Livros, Tecnologia), Carla Mendes, Thiago Barros, Bruno Lima, Elisa Rocha. Feed com 2 posts da Ana ("Café coado rende mais código..." e "Primeiro deploy da semana..."). Caminho: **3 graus: Professor Demo → Ana Souza → Patrícia Gomes → Jonas Pinto**. | "Com uma aresta só, o grafo já sugere a Marina, professora de banco de dados: amiga da Ana e com os mesmos interesses. Isso é amigos de amigos, dois saltos. E o menor caminho até o Jonas, em Natal, sai com um shortestPath." |
| 5 | **CREATE** (curtida, opcional se o tempo apertar) | Na aba Feed, clicar **♥ Curtir** no post da Ana. | Contador de curtidas do post sobe em 1. | "Curtir também é uma aresta, CURTIU, com a hora." |
| 6 | **UPDATE** | Em "Editar": cidade `Recife`, bio `Bio atualizada ao vivo` → **Salvar alterações**. | Cabeçalho mostra "Recife". Painel: `SET u += $campos, u.atualizadoEm = datetime()`. | "Atualizar é um SET nas propriedades do nó. Não tem ALTER TABLE: se eu quiser um campo novo, é só gravar." |
| 7 | **DELETE** (aresta) | Em "Seguindo", clicar no **×** do chip da Ana. | Ana sai de "Seguindo". Sugestões ficam vazias ("Sem sugestões — siga alguém primeiro."). Painel: `DELETE r`. | "Aqui apaguei só o relacionamento. Os dois usuários continuam existindo." |
| 8 | **DELETE** (nó) | Clicar **Excluir usuário (DELETE)** e confirmar. | Toast "Usuário excluído (DETACH DELETE)". Professor Demo some da lista e do grafo. | "DETACH DELETE apaga o nó junto com todas as arestas dele. O post que ele publicou também foi removido." |

**Tempo-alvo:** passos 1–2 (~45 s), 3–5 (~1 min), 6–8 (~1 min). Se estiver atrasado, pular o passo 5.

## Plano B — Neo4j Browser (`07-aplicacao-pratica/cypher/03_crud_demo.cypher`)

Se o app falhar, rodar os mesmos passos **um bloco por vez** (selecionar o bloco e Ctrl+Enter).
Use o modo **Graph** nos blocos de READ.

| Bloco | Operação | Resultado esperado |
|---|---|---|
| CREATE — novo usuário | `CREATE (u:Usuario {username: 'prof.demo', ...})` + interesses | 1 nó criado e 2 relacionamentos (os interesses já existiam, o MERGE reaproveita) |
| CREATE — seguir + post | `MERGE (u)-[:SEGUE]->(ana)` e `CREATE (u)-[:PUBLICOU]->(:Post ...)` | 1 relação SEGUE · 1 nó Post + 1 relação PUBLICOU |
| READ — vizinhança | `MATCH (u {username:'prof.demo'})-[r]-(vizinho)` | 4 vizinhos: Ana, Tecnologia, Livros e o post |
| READ — sugestões | amigos de amigos + interesses | 6 linhas: Marina Castro (Livros, Tecnologia), Carla Mendes, Thiago Barros, Bruno Lima, Elisa Rocha e Patrícia Gomes (no Browser não há LIMIT 5) |
| READ — graus | `shortestPath` até `jonas.pinto` | `graus = 3` (Professor Demo → Ana → Patrícia → Jonas) |
| UPDATE | `SET u.cidade = 'Recife', ...` | Nó com cidade Recife |
| DELETE — aresta | `DELETE r` | 1 relacionamento removido |
| DELETE — usuário | `DETACH DELETE p, u` | Remove o usuário, o post e as arestas restantes |
| Conferir | `count(u)` | `restantes = 0` |

## Se algo der errado

| Problema | O que fazer |
|---|---|
| "Já existe um usuário com esse username" no passo 2 | Sobrou o `prof.demo` do ensaio: usar `prof.demo2` e seguir em frente (ou rodar `seed.py --limpar` antes, como no checklist). |
| Grafo não aparece ("sem internet?") | A biblioteca de visualização vem da internet. Seguir a demo pelas listas e pelo painel de Cypher, e mostrar o grafo no Neo4j Browser. |
| App não conecta no Neo4j (erro 503) | Conferir se a janela do `neo4j.bat console` está aberta. Se o PC falhar, trocar o `.env` para o AuraDB Free e reiniciar o `run.py`. |
| Nada funciona | Plano B no Neo4j Browser (tabela acima). |

## Teste do plano B com o João Pedro (fazer no ensaio)

- [ ] `python scripts/seed.py --limpar` roda sem erro e mostra 18 / 60 / 30
- [ ] Passos 1 a 8 no app conferem com a coluna "Resultado esperado"
- [ ] Todos os blocos do `03_crud_demo.cypher` rodam no Neo4j Browser
- [ ] Demo inteira cronometrada em até 3 minutos
- [ ] Instância AuraDB Free criada, seed carregado e retomada na véspera
