"""Cria as constraints e carrega os dados de exemplo.

Uso (na raiz do projeto):
    python scripts/seed.py           # constraints + dados
    python scripts/seed.py --limpar  # apaga TUDO do banco antes de carregar
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import config, db  # noqa: E402


def main() -> None:
    print(f"Conectando em {config.NEO4J_URI} (banco '{config.NEO4J_DATABASE}')...")
    db.driver().verify_connectivity()

    if "--limpar" in sys.argv:
        db.driver().execute_query("MATCH (n) DETACH DELETE n", database_=config.NEO4J_DATABASE)
        print("Banco limpo.")

    for arquivo in ("01_constraints.cypher", "02_seed.cypher"):
        n = db.executar_script(str(RAIZ / "cypher" / arquivo))
        print(f"  {arquivo}: {n} instruções executadas")

    contagem, _, _ = db.driver().execute_query(
        "MATCH (n) RETURN labels(n)[0] AS tipo, count(*) AS total ORDER BY tipo",
        database_=config.NEO4J_DATABASE,
    )
    for linha in contagem:
        print(f"  {linha['tipo']}: {linha['total']}")
    db.fechar()
    print("Pronto.")


if __name__ == "__main__":
    main()
