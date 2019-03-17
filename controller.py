from models import Game, User, TurnInfo


def get_games(game_id=None):
    """
    This function returns the list of game objects (SqlAlchemy objects)
    from the database

    :game_id:       filter the list of games based on game_id, if present
    :return:        list of games, or single game
    """
    # start building the query to get all active games
    query = Game.query.filter(Game.active)

    # should we also filter based on the user_id?
    if game_id is not None:
        query = query.filter(Game.id == game_id)

    games = query.all()
    return games


def get_users(user_id=None):
    """
    This function returns the list of users, if no user_id is supplied,
    and a single user if the user_id is supplied.

    :param user_id:     user id to filter on if present
    :return:            list of users
    """
    # start building the query to get all users
    query = User.query

    # should we filter down to a single user?
    if user_id is not None:
        query = query.filter(User.id == user_id)

    users = query.all()
    return users


def get_users_dict(user_id=None):
    _users_dict = get_users(user_id)

    # convert the list of user objects to a list of dictionaries
    # so they can be serialized
    users_dict = [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "account_type": user.account_type,
            "games": [
                {
                    "id": game.id,
                    "creator": game.creator,
                    "participants": game.participants,
                    "name": game.name,
                    "active": game.active,
                    "limit": game.limit,
                }
                for game in user.games
            ],
        }
        for user in _users_dict
    ]

    return users_dict


def get_latest_turn(game_id, user_id):
    print(game_id)
    print(user_id)
    latest_turn_info = (
        TurnInfo.query.filter_by(game_id=game_id)
        .filter_by(user_id=user_id)
        .order_by(TurnInfo.id.desc())
        .first()
    )
    return latest_turn_info
