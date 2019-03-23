import os
from config import db
from models import User, TurnInfo, Game, game_to_user
import json

# Data to initialize database with
USERS = [
    {
        "username": "Doug",
        "password": "password",
        "email": "notsure@gmail.com",
        "account_type": "organizer",
        "icon": "usa.png",
        "games": ["Test Game One"],
    },
    {
        "username": "Brockman",
        "password": "password",
        "email": "rgregory@fnwsu.org",
        "account_type": "member",
        "icon": "united-kingdom.png",
        "games": ["Test Game One", "Test Game Two"],
    },
    {
        "username": "rusti",
        "password": "password",
        "email": "mrgregory1@gmail.com",
        "account_type": "admin",
        "icon": "usa.png",
        "games": ["Test Game Two"],
    },
]

GAMES = [
    {"creator": 3, "active": True, "limit": 3, "name": "Test Game One", "allow_new": True},
    {"creator": 2, "active": True, "limit": 5, "name": "Test Game Two", "allow_new": True},
]

# Delete database file if it exists currently
if os.path.exists("flamme_rouge.db"):
    os.remove("flamme_rouge.db")

# String-ify a dictionary to save in options
pre_options = {"is_meteo": True, "breakaway_option": True}
options = json.dumps(pre_options)

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in USERS:
    p = User(
        username=person.get("username"),
        password=person.get("password"),
        email=person.get("email"),
        account_type=person.get("account_type"),
        icon=person.get("icon"),
    )
    db.session.add(p)
db.session.commit()


for game in GAMES:
    this_game = Game(
        creator=game.get("creator"),
        name=game.get("name"),
        active=game.get("active"),
        limit=game.get("limit"),
        allow_new=game.get("allow_new"),
        options=options,
    )

    # This is sort of artificial, I added what games the users are part of
    # in the dictionary for USERS above as a list of games. I'm using
    # that list to add those users to the appropriate games here
    # I'm just doing this for an experiment to populate the database.
    # In the real application users would add themselves to games using
    # your application.
    # So you'll want to delete this section when you get the "add user to game"
    # part of your application done

    # iterate over the list of users
    for user in USERS:

        # iterate over the list of games the user is in
        for game in user.get("games"):

            # does the name of the game the user is in match our current db game?
            if game == this_game.name:

                # retrieve the user from the database
                this_user = User.query.filter(
                    User.username == user.get("username")
                ).one_or_none()

                # did we get a user?
                if this_user is not None:

                    # add the user to the game
                    this_game.users.append(this_user)

    db.session.add(this_game)

db.session.commit()
