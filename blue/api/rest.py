# This module provides the REST API (example) for the application

from flask import (
    Blueprint,
    jsonify,
    request,
    make_response
)
from models import Game
import controller


api = Blueprint("api", __name__)


@api.route("/games", methods=["GET"])
def get_games():
    """
    This function provides the /games API REST URL endpoint
    It returns a JSON string of the list of active games

    :return:        JSON string containing list of games
    """
    user_id = None

    # is 'user_id' in the query string?
    if "user_id" in request.args:
        user_id = int(request.args.get("user_id", None))

    # call the controller to get the games that match our requirements
    _games = controller.get_games(user_id=user_id)

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
    response = make_response(jsonify(games), 200)
    response.headers["Content-Type"] = "application/json"
    return response
