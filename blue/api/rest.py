# This module provides the REST API (example) for the application

from flask import Blueprint, jsonify, request, make_response
import controller
from config import logger


api = Blueprint("api", __name__)


@api.route("/games", methods=["GET"])
@api.route("/games/<int:game_id>")
def get_games(game_id=None):
    """
    This function provides the /games/<game_id> API REST URL endpoint
    It returns a JSON string of the list of active games

    :return:        JSON string containing list of games
    """
    # call the controller to get the games that match our requirements
    _games = controller.get_games(game_id=game_id)

    # convert the list of games objects to a list of dictionaries
    # so they can be serialized
    games = [
        {
            "id": game.id,
            "creator": game.creator,
            "name": game.name,
            "active": game.active,
            "limit": game.limit,
            "options": game.options,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "account_type": user.account_type,
                    "icon": user.icon,
                }
                for user in game.users
            ],
        }
        for game in _games
    ]


    response = make_response(jsonify(games), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route("/users", methods=["GET"])
@api.route("/users/<int:user_id>")
def get_users(user_id=None):
    """
    This function provides the /users/<user_id> API REST URL endpoint
    It returns a JSON string of the list of users

    :return:        JSON string containing list of users
    """
    # call the controller to get the users that match our requirements
    _users = controller.get_users(user_id=user_id)

    # convert the list of user objects to a list of dictionaries
    # so they can be serialized
    users = [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "account_type": user.account_type,
            "icon": user.icon,
            "games": [
                {
                    "id": game.id,
                    "creator": game.creator,
                    "name": game.name,
                    "active": game.active,
                    "limit": game.limit,
                    "options": game.options,
                }
                for game in user.games
            ],
        }
        for user in _users
    ]
    response = make_response(jsonify(users), 200)
    response.headers["Content-Type"] = "application/json"
    return response
