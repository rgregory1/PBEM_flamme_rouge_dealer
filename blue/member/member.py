from flask import (
    Flask,
    Blueprint,
    session,
    render_template,
    url_for,
    redirect,
    request,
    flash,
)

import pathlib
from functions import *
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from models import User


member = Blueprint("member", __name__, template_folder="member")


@member.route("/login")
def member_login():
    user = User.query.filter_by(username="rusti").first()
    login_user(user)
    return "<h1>you are logged in</h1>"


@member.route("/member_page")
@login_required
def member_page():
    return "</h1>you are in a protected page</h1>"
