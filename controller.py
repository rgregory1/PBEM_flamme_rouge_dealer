from config import db
from models import Game, User, game_to_user

# TODO figiure out what the minimum that I need to import to use current_user

def get_games():
    """
    This function provides the /games API REST URL endpoint
    It returns a JSON string of the list of active games

    :return:        JSON string containing list of games
    """
    _games = Game.query \
        .filter(Game.active == True) \
        .all()

    # convert the list of games objects to a list of dictionaries
    # so they can be serialized
    games = [
        {
            "id": game.id,
            "creator": game.creator,
            "participants": game.participants,
            "name": game.name,
            "active": game.active,
            "limit": game.limit,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "account_type": user.account_type,
                }
                for user in game.users
            ]
        }
        for game in _games
    ]
    # response = make_response(jsonify(games), 200)
    # response.headers["Content-Type"] = "application/json"
    # return response
    return games

def get_user_games(this_id):
    """
    This function provides the /games API REST URL endpoint
    It returns a dict of the list of active games of current_user

    :return:        dict containing list of games for the current user
    """
    _games = Game.query.filter(Game.active==True).filter(Game.users.any(User.id == this_id)).all()

    # convert the list of games objects to a list of dictionaries
    # so they can be serialized
    games = [
        {
            "id": game.id,
            "creator": game.creator,
            "participants": game.participants,
            "name": game.name,
            "active": game.active,
            "limit": game.limit,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "account_type": user.account_type,
                }
                for user in game.users
            ]
        }
        for game in _games
    ]
    return games
