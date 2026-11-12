from flask import Flask

from . import db
from .rotas import bp


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.json.ensure_ascii = False
    app.register_blueprint(bp)
    db.registrar_encerramento()
    return app
