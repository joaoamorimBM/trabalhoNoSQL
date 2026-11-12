# Projeto 3 — Bancos de Dados NoSQL · Orientado a Grafo (Neo4j)

**Paradigma:** orientado a grafo · **SGBD:** Neo4j · **Sistema:** Rede Social
**Equipe:** João Pedro · Hamilton · Isaac · Luiz · Vinícius

Divisão completa do trabalho: [`00-divisao/Divisao_Trabalho_NoSQL_Grafo.pdf`](00-divisao/Divisao_Trabalho_NoSQL_Grafo.pdf)

## Organização: uma pasta por tópico

| Pasta | Tópico | Responsável |
|---|---|---|
| [`00-divisao/`](00-divisao/) | PDF com a divisão do trabalho | — |
| [`01-paradigma/`](01-paradigma/) | 1 — Paradigma orientado a grafo (+ abertura) | Hamilton |
| [`02a-neo4j-arquitetura/`](02a-neo4j-arquitetura/) | 2A — Neo4j: características e arquitetura | Hamilton |
| [`02b-cluster-hardware-nuvem/`](02b-cluster-hardware-nuvem/) | 2B — Cluster, hardware, nuvem e custo | Isaac |
| [`03-aplicacoes-reais/`](03-aplicacoes-reais/) | 3 — Aplicações reais | Luiz |
| [`04-05-vantagens-desvantagens/`](04-05-vantagens-desvantagens/) | 4 e 5 — Vantagens e desvantagens (+ referências) | Luiz |
| [`06-rede-social/`](06-rede-social/) | 6 — Rede social com Neo4j (+ dados e roteiro da demo) | Vinícius |
| [`07-aplicacao-pratica/`](07-aplicacao-pratica/) | Aplicação prática: código do CRUD + modelagem | João Pedro |
| [`08-slides/`](08-slides/) | Deck final montado a partir de todas as pastas | Todos |

Cada pasta tem um `README.md` (o que cobrir) e um `conteudo.md` (modelo para escrever slide por slide).
Ordem da apresentação (15 min): 01 → 02a → 02b → 03 → 04-05 → 06 → 07 (demo ao vivo).

**Vai usar IA para ajudar?** Peça para ela ler o [`CLAUDE.md`](CLAUDE.md) primeiro (Claude Code e
Copilot leem sozinhos; no ChatGPT/Gemini, cole o conteúdo do arquivo no início da conversa).

**Demo:** roda no computador do João Pedro com Neo4j local; o AuraDB Free (nuvem) é o plano de
contingência. Detalhes em [`07-aplicacao-pratica/README.md`](07-aplicacao-pratica/README.md).

## Como cada um contribui

Faça isso **uma vez**:

```bash
git clone <URL-DO-REPOSITORIO>
cd <nome-do-repositorio>
```

Toda vez que for trabalhar:

```bash
git checkout main
git pull                                   # pega o que os outros já enviaram
git checkout -b seu-nome/topico            # ex.: hamilton/topico-1
# ... edite APENAS os arquivos da sua pasta ...
git add .
git commit -m "Tópico 1: conceitos de grafo"
git push -u origin seu-nome/topico
```

Depois, no GitHub, clique em **Compare & pull request** → **Create pull request**.
O João Pedro revisa e faz o merge no `main`.

Regras:
- Mexa só na sua pasta; assim ninguém tem conflito com ninguém.
- Não suba senhas: o `.env` já está no `.gitignore`.
- Toda informação no `conteudo.md` precisa de fonte.
