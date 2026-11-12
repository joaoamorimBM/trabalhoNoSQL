// Restrições de unicidade (também criam índices automaticamente).
// Pode rodar quantas vezes quiser: IF NOT EXISTS evita erro.

CREATE CONSTRAINT usuario_username IF NOT EXISTS
FOR (u:Usuario) REQUIRE u.username IS UNIQUE;

CREATE CONSTRAINT post_id IF NOT EXISTS
FOR (p:Post) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT interesse_nome IF NOT EXISTS
FOR (i:Interesse) REQUIRE i.nome IS UNIQUE;
