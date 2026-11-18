# Tópico 3 — Aplicações reais do Neo4j

> Responsável: Luiz · Tempo de fala: aproximadamente 1 minuto  
> Pesquisa conferida em 18/11/2026. Os exemplos abaixo são **casos de uso documentados historicamente**; não afirmamos que todos continuam usando Neo4j na arquitetura atual.

## Slide 1 — Neo4j no mercado: comércio e recomendações

- **eBay:** assistente de compras conversacional apoiado por grafo de conhecimento.
- **Walmart Brasil:** recomendações personalizadas no comércio eletrônico.
- Ideia comum: explorar conexões entre pessoas, produtos e contexto.

**Fala:**  
"O Neo4j não é só uma tecnologia estudada em sala. Um caso documentado é o do eBay, que utilizou um grafo para apoiar um assistente de compras conversacional, entendendo melhor o contexto das buscas. Outro exemplo histórico é o Walmart Brasil, que usou relações entre consumidores e produtos para gerar recomendações personalizadas. Nos dois casos, o valor está em percorrer conexões entre informações, em vez de analisar cada registro isoladamente."

**Imagem/diagrama:** duas colunas com os nomes eBay e Walmart Brasil; ao centro, desenho conceitual `Pessoa → INTERESSA_SE → Produto → POSSUI → Categoria`. Esse desenho é **ilustrativo**, não um modelo oficial dos bancos das empresas.

**Fontes:**
- Neo4j, *eBay customer story*: https://neo4j.com/customer-stories/ebay/ (acessado em 18/11/2026).
- Neo4j, *How Walmart uses Neo4j for retail competitive advantage*: https://neo4j.com/blog/graph-database/walmart-neo4j-competitive-advantage/ (acessado em 18/11/2026).
- Neo4j, *Walmart case study* (PDF): https://go.neo4j.com/rs/710-RRC-335/images/neo4j-casestudy-walmart.pdf (acessado em 18/11/2026).

## Slide 2 — Neo4j para conteúdo e conhecimento

- **Medium:** grafo social e recomendações de conteúdo personalizado.
- **NASA:** organização e descoberta de conexões em conhecimentos de projetos.
- Usos diferentes, mesma necessidade: consultar relações complexas.

**Fala:**  
"O uso de grafos vai além das lojas virtuais. O Medium apresentou o uso de Neo4j para construir um grafo social e apoiar recomendações de conteúdo. Na NASA, casos publicados descrevem grafos de conhecimento para conectar informações e lições de projetos anteriores. Isso mostra a versatilidade da abordagem: recomendações, redes de pessoas e gestão do conhecimento podem se beneficiar de um banco orientado a relacionamentos."

**Imagem/diagrama:** grafo ilustrativo ligando `Autor → Escreveu → Artigo → Trata_de → Tema`, ao lado de outro ligando `Projeto → Gerou → Lição → Relacionada_a → Tecnologia`. Não atribuir esses rótulos ao banco real dessas organizações.

**Fontes:**
- Neo4j, *Real-time recommendations: customer spotlight Medium.com*: https://neo4j.com/use-cases/real-time-recommendations/ (acessado em 18/11/2026).
- Neo4j, *Graphs in government: A NASA knowledge graph*: https://neo4j.com/blog/knowledge-graph/graphs-in-government-nasa-knowledge-graph/ (acessado em 18/11/2026).
- Neo4j, *Graphing a lesson learned database for NASA*: https://neo4j.com/blog/graph-visualization/nasa-lesson-learned-database-using-neo4j-linkurious/ (acessado em 18/11/2026).

## Observações para o responsável pelos slides

- Destacar preferencialmente eBay, Walmart Brasil e Medium; NASA pode ser um exemplo adicional.
- Não afirmar percentuais de ganho de desempenho ou retorno financeiro sem identificar uma medição e suas condições.
- Não confundir casos históricos publicados pelo fabricante com confirmação de adoção **atual**.
- Para manter a fala total em três minutos, este tópico deve consumir cerca de um minuto.

## Referências deste tópico

1. NEO4J. *eBay customer story*. https://neo4j.com/customer-stories/ebay/. Acesso em: 18 nov. 2026.
2. NEO4J. *How Walmart uses Neo4j for retail competitive advantage*. https://neo4j.com/blog/graph-database/walmart-neo4j-competitive-advantage/. Acesso em: 18 nov. 2026.
3. NEO4J. *Real-time recommendations*. https://neo4j.com/use-cases/real-time-recommendations/. Acesso em: 18 nov. 2026.
4. NEO4J. *Graphs in government: A NASA knowledge graph*. https://neo4j.com/blog/knowledge-graph/graphs-in-government-nasa-knowledge-graph/. Acesso em: 18 nov. 2026.
