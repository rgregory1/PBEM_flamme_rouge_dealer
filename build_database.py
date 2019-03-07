import os
from config import db
from models import User, TurnInfo, Game

# Data to initialize database with
USERS = [
    {
        "username": "Doug",
        "password": "password",
        "email": "notsure@gmail.com",
        "account_type": "organizer",
    },
    {
        "username": "Brockman",
        "password": "password",
        "email": "rgregory@fnwsu.org",
        "account_type": "member",
    },
    {
        "username": "rusti",
        "password": "password",
        "email": "mrgregory1@gmail.com",
        "account_type": "admin",
    },
]

GAMES = [
    {
        "id": 101,
        "creator": 3,
        "participants": "'[3,1]'",
        "active": True,
        "limit": 3,
        "name": "Test Game",
    }
]

# Delete database file if it exists currently
if os.path.exists("flamme_rouge.db"):
    os.remove("flamme_rouge.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in USERS:
    p = User(
        username=person.get("username"),
        password=person.get("password"),
        email=person.get("email"),
        account_type=person.get("account_type"),
    )
    db.session.add(p)

for game in GAMES:
    this_game = Game(
        id=game.get("id"),
        creator=game.get("creator"),
        participants=game.get("participants"),
        name=game.get("name"),
        active=game.get("active"),
        limit=game.get("limit"),
    )
    db.session.add(this_game)

db.session.commit()
