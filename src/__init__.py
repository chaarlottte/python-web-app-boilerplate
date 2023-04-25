from flask import Flask, session, request, url_for, redirect
from .models import db, User
from .routes import accounts
from .manager.user_manager import UserManager

def create_app():
    app = Flask(__name__)
    app.secret_key = b"4be19e997f721ea841d8ab0d4215c13421c2eb78d2cc353b49c3e87c1611e40d"
    app.config.update({ "SQLALCHEMY_DATABASE_URI": "sqlite:///database.db" })
    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)
    UserManager(app)
    app.register_blueprint(accounts, url_prefix="")

