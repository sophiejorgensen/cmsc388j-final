# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_mongoengine import MongoEngine
from flask_mail import Message
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import io, base64

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, poke_client, mail
from .forms import (
    SearchForm,
    PokeReviewForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
)
from .models import User, Review, load_user
from .utils import current_time

#main = Blueprint("main", __name__)

db = MongoEngine(app)
