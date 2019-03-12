from models import Game, User

def get_games(user_id=None):
    """
    This function returns the list of game objects (SqlAlchemy objects)
    from the database

    :user_id:       filter the list of games based on user_id, if present
    :return:        JSON string containing list of games
    """
    # start building the query to get all active games
    query = Game.query \
        .filter(Game.active)

    # should we also filter based on the user_id?
    if user_id is not None:
        query = query \
            .filter(Game.users.any(User.id == user_id))

    # get all the games that match our requirements
    games = query.all()

    # return the list of SqlAlchemy game objects
    return games
