
import json

# all we need from config is db, so grab it here
from config import db

# all we need from flask_login is UserMixin, so grab it here
from flask_login import UserMixin

# imported pretty print to print objects of the classes below
from pprint import pformat


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
    icon = db.Column(db.String(30))

    def __str__(self):
        return pformat(vars(self), indent=4, width=80)

    def __repr__(self):
        return self.__str__()


class TurnInfo(UserMixin, db.Model):
    __tablename__ = "TurnInfo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    current_round = db.Column(db.Integer)
    turn_data = db.Column(db.Text)
    summary_data = db.Column(db.Text)
    total_exhaustion = db.Column(db.Integer)

    # I added these properties to the class that
    # automatically convert the JSON string to a dictionary
    # when you access the property. So for example you would get a
    # turn_info instance and you could do this:
    # turn_info.turn_data_json["<some key in the data">]
    @property
    def turn_data_json(self):
        return json.loads(self.turn_data)

    @property
    def summary_data_json(self):
        return json.loads(self.summary_data)

    def __str__(self):
        return pformat(vars(self), indent=4, width=1)

    def __repr__(self):
        return self.__str__()


class Game(UserMixin, db.Model):
    __tablename__ = "Game"
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    name = db.Column(db.String(30))
    active = db.Column(db.Boolean)
    limit = db.Column(db.Integer)
    allow_new = db.Column(db.Boolean)
    users = db.relationship("User", secondary=game_to_user)
    options = db.Column(db.Text)

    @property
    def options_json(self):
        return json.loads(self.options)

    def __str__(self):
        return pformat(vars(self), indent=4, width=1)

    def __repr__(self):
        return self.__str__()
