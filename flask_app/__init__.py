# export FLASK_APP=__init__.py in command line

# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_talisman import Talisman
import os
from flask_mongoengine import MongoEngine
from .client import PokeClient
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

mail = Mail()

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

poke_client = PokeClient()

from .pokemons.routes import pokemons
from .users.routes import users

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)

    #csp = {
    #    'default-src': '\'self\'',
    #    'script-src': 'stackpath.bootstrapcdn.com',
    #    'style-src': ['code.jquery.com', 'cdn.jsdelivr.net', 'stackpath.bootstrapcdn.com']
    #}

    #Talisman(app, content_security_policy=csp)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_DEFAULT_SENDER": os.environ['EMAIL_USER'],
        "MAIL_USERNAME": os.environ['EMAIL_USER'],
        "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    }

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    app.config.update(mail_settings)

    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(pokemons)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
