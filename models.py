
# all we need from config is db, so grab it here
from config import db

# all we need from flask_login is UserMixin, so grab it here
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    account_type = db.Column(db.String(20))
