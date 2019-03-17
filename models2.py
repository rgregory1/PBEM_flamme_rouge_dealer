# all we need from config is db, so grab it here
from config import db

# all we need from flask_login is UserMixin, so grab it here
from flask_login import UserMixin

# imported pretty print to pring objects of the classes below
from pprint import pformat

# from sqlalchemy.ext.declarative import delcarative_base

# Base = delcarative_base()

game_to_user = db.Table(
    "game_to_user",
    db.Column("game_id", db.Integer, db.ForeignKey("Game.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("User.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30))
    account_type = db.Column(db.String(20))
    games = db.relationship("Game", secondary=game_to_user)

    def __str__(self):
        return pformat(vars(self), indent=4, width=1)

    def __repr__(self):
        return self.__str__()


class TurnInfo(UserMixin, db.Model):
    __tablename__ = "TurnInfo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    game_id = db.Column(db.Integer)
    current_round = db.Column(db.Integer)
    turn_data = db.Column(db.Text)

    def __str__(self):
        return pformat(vars(self), indent=4, width=1)

    def __repr__(self):
        return self.__str__()


class Game(UserMixin, db.Model):
    __tablename__ = "Game"
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    participants = db.Column(db.Text)
    name = db.Column(db.String(30))
    active = db.Column(db.Boolean)
    limit = db.Column(db.Integer)
    users = db.relationship("User", secondary=game_to_user)

    def __str__(self):
        return pformat(vars(self), indent=4, width=1)

    def __repr__(self):
        return self.__str__()
