from datetime import datetime
from myapp import db
from flask_login import LoginManager, UserMixin, login_user, login_required


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    account_type = db.Column(db.String(20))
