"""Conexão com o Neo4j.

Um único driver é compartilhado pela aplicação (o driver gerencia o pool de conexões).
Toda consulta executada fica registrada em `flask.g.cypher` para a interface mostrar
o Cypher que rodou — útil na apresentação ao vivo.
"""
import atexit
from typing import Any

from flask import g, has_app_context
from neo4j import GraphDatabase, RoutingControl

from . import config

_driver = None


def driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            config.NEO4J_URI,
            auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
            connection_timeout=8,          # falha rápido se o banco estiver fora do ar
            max_transaction_retry_time=5,  # não fica 30 s tentando de novo na demo
        )
    return _driver


def registrar_encerramento() -> None:
    atexit.register(fechar)


def fechar() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def _registrar(query: str, params: dict) -> None:
    if has_app_context():
        g.setdefault("cypher", []).append({"query": _limpar(query), "params": params})


def _limpar(query: str) -> str:
    linhas = [linha.rstrip() for linha in query.strip("\n").splitlines()]
    recuo = min((len(l) - len(l.lstrip()) for l in linhas if l.strip()), default=0)
    return "\n".join(l[recuo:] for l in linhas)


def escrever(query: str, **params: Any) -> list[dict]:
    """Executa uma consulta de escrita (CREATE/MERGE/SET/DELETE)."""
    _registrar(query, params)
    records, _, _ = driver().execute_query(
        query, params, database_=config.NEO4J_DATABASE, routing_=RoutingControl.WRITE
    )
    return [r.data() for r in records]


def ler(query: str, **params: Any) -> list[dict]:
    """Executa uma consulta somente leitura (MATCH ... RETURN)."""
    _registrar(query, params)
    records, _, _ = driver().execute_query(
        query, params, database_=config.NEO4J_DATABASE, routing_=RoutingControl.READ
    )
    return [r.data() for r in records]


def executar_script(caminho: str) -> int:
    """Executa um arquivo .cypher (instruções separadas por ';'). Retorna quantas rodaram."""
    with open(caminho, encoding="utf-8") as f:
        sem_comentarios = "\n".join(
            l for l in f.read().splitlines() if not l.strip().startswith("//")
        )
    instrucoes = [s.strip() for s in sem_comentarios.split(";") if s.strip()]
    for instrucao in instrucoes:
        driver().execute_query(instrucao, database_=config.NEO4J_DATABASE)
    return len(instrucoes)
