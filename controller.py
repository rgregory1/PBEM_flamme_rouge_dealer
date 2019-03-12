from config import db
from models import Game

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

def get_user_games():
    """
    This function provides the /games API REST URL endpoint
    It returns a JSON string of the list of active games

    :return:        JSON string containing list of games
    """
    _games = Game.query.filter(Game.active == True, Game.users.user.id == current_user.id).all()

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
