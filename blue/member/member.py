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


# from models import User
class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    account_type = db.Column(db.String(20))


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
