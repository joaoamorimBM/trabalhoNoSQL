# CLAUDE.md — instruções para assistentes de IA neste repositório

Este arquivo orienta qualquer IA (Claude, ChatGPT, Copilot, Gemini...) que for ajudar alguém da equipe.
Se a sua IA não lê este arquivo sozinha, **cole o conteúdo dele no início da conversa**.

## O projeto

Trabalho em equipe da disciplina de **Bancos de Dados NoSQL** (Projeto 3, vale 40% da nota).
- **Paradigma sorteado:** orientado a grafo · **SGBD:** Neo4j · **Sistema escolhido:** Rede Social
- Entrega = **apresentação de 15 minutos** para a turma + **CRUD ao vivo** no banco.
- Notas: apresentação do banco e características **6,0** · aplicação prática (CRUD) **4,0**.
- A apresentação deve ter o **nome de todos os componentes**. Não há prorrogação de prazo.
- Divisão completa: `00-divisao/Divisao_Trabalho_NoSQL_Grafo.pdf`.

## Equipe e pastas (cada pessoa só mexe na própria pasta)

| Pasta | Conteúdo | Responsável |
|---|---|---|
| `01-paradigma/` | Tópico 1 — paradigma orientado a grafo (+ abertura) | Hamilton |
| `02a-neo4j-arquitetura/` | Tópico 2A — características e arquitetura do Neo4j | Hamilton |
| `02b-cluster-hardware-nuvem/` | Tópico 2B — cluster, nós, hardware, nuvem e custo | Isaac |
| `03-aplicacoes-reais/` | Tópico 3 — empresas que usam Neo4j | Luiz |
| `04-05-vantagens-desvantagens/` | Tópicos 4 e 5 + slide de referências | Luiz |
| `06-rede-social/` | Tópico 6 — por que grafo numa rede social + `roteiro-demo.md` | Vinícius |
| `07-aplicacao-pratica/` | Código da aplicação (Flask + Neo4j), modelagem, plano B | João Pedro |
| `08-slides/` | Deck final, montado no fim a partir dos `conteudo.md` | Todos |

Ordem da apresentação: 01 → 02a → 02b → 03 → 04-05 → 06 → 07 (demo). Cerca de 3 min por pessoa.

## Regras para a IA

1. **Escreva em português do Brasil.**
2. **Edite só a pasta de quem está pedindo ajuda.** Pergunte o nome da pessoa se não souber.
   Exceção: o Vinícius também edita `07-aplicacao-pratica/cypher/02_seed.cypher` (dados de exemplo).
3. **Não invente fatos, números, preços nem casos de empresas.** Todo dado no `conteudo.md` precisa de
   fonte real (link + data de acesso). Se não tiver certeza, diga que precisa ser verificado.
   Preços de nuvem mudam: sempre indicar a data da consulta.
4. **Não faça slides (.pptx) por conta própria.** O conteúdo vai no `conteudo.md` da pasta, seguindo o
   modelo que já está lá (Slide N → tópicos curtos, Fala, Imagem/diagrama, Fontes). O deck único é
   gerado no fim, com o mesmo visual para todos.
5. Slides com **tópicos curtos** (até ~5 por slide); a explicação vai em "Fala". Cada pessoa tem
   ~3 minutos, então 2 a 4 slides por tópico.
6. Imagens e diagramas ficam em `imagens/` dentro da pasta do tópico.
7. **Nunca** coloque senhas no repositório. O `.env` é local e está no `.gitignore`.
8. Mantenha o foco no paradigma de **grafo** e no **Neo4j** — é o que a avaliação cobra.

## Fluxo de Git

```bash
git checkout main && git pull
git checkout -b nome/topico          # ex.: luiz/vantagens
# editar só a própria pasta
git add . && git commit -m "Tópico X: descrição curta"
git push -u origin nome/topico       # depois abrir Pull Request no GitHub
```

O João Pedro revisa e faz o merge no `main`. Não fazer push direto no `main`.

## Aplicação (07-aplicacao-pratica)

- Python 3 + Flask + driver oficial `neo4j`. Interface em `app/static/` (HTML/CSS/JS puro + vis-network).
- **Todas as consultas Cypher ficam em `app/repositorio.py`.** As rotas (`app/rotas.py`) só validam a
  entrada e chamam o repositório. `app/db.py` registra o Cypher executado para a tela mostrar.
- Modelo do grafo (`modelagem.md`): nós `Usuario`, `Post`, `Interesse`; relações `SEGUE`, `PUBLICOU`,
  `CURTIU`, `INTERESSADO_EM`. Nomes de variáveis, funções e rótulos em português.
- Rodar (dentro de `07-aplicacao-pratica/`, com um Neo4j ligado e o `.env` preenchido):
  `python scripts/seed.py` (carrega dados) e depois `python run.py` → <http://localhost:5000>.
- Plano B da demo: `cypher/03_crud_demo.cypher`, bloco a bloco no Neo4j Browser.
- Em `cypher/02_seed.cypher` não use ponto e vírgula dentro dos textos (o script separa as instruções
  por esse caractere) e use `MERGE` para o seed poder rodar várias vezes.
- Banco da apresentação: Neo4j **local** no computador do João Pedro; **AuraDB Free** é o plano de
  contingência (mesmo código, só troca o `.env`).
