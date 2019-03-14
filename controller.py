from models import Game, User

def get_games(game_id=None):
    """
    This function returns the list of game objects (SqlAlchemy objects)
    from the database

    :game_id:       filter the list of games based on game_id, if present
    :return:        list of games, or single game
    """
    # start building the query to get all active games
    query = Game.query \
        .filter(Game.active)

    # should we also filter based on the user_id?
    if game_id is not None:
        query = query \
            .filter(Game.id == game_id)

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
        query = query \
            .filter(User.id == user_id)

    users = query.all()
    return users

