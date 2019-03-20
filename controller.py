from models import Game, User, TurnInfo
from sqlalchemy import desc


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


def get_turns(user_id=None, game_id=None):
    """
    This function returns the list of turns that match
    the user and game id.

    :param user_id:     user id to filter on if present
    :param game_id:     game id to filter on if present
    :return:            list of turns

    ** NOTE ** I added this because I couldn't think of some
    cool way to relate turn_info to both users and games. So
    I set this up as a separate query to get the turns
    that match the user AND the game. I did the order_by
    to make sure if any turns are found, the turn at
    index 0 would be the current (latest) round.
    """
    # start building the query to get all the turns
    query = TurnInfo.query

    # should we filter by user and game?
    if user_id is not None and game_id is not None:
        query = query \
            .filter(TurnInfo.user_id == user_id) \
            .filter(TurnInfo.game_id == game_id) \
            .order_by(TurnInfo.current_round.desc())

    # run the query
    turns = query.all()
    return turns

def get_this_turns(game_id):
    query = TurnInfo.query

    # filter by game number?
    if user_id is not None and game_id is not None:
        query = query \
            .filter(TurnInfo.game_id == game_id) \
            .order_by(TurnInfo.current_round.desc())

    # run the query
    turns = query.all()
    return turns

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
                    "name": game.name,
                    "active": game.active,
                    "limit": game.limit,
                    "options": game.options,
                }
                for game in user.games
            ],
        }
        for user in _users_dict
    ]

    return users_dict


def get_games_users_dict(game_id=None):

   # convert the get_games call to a dict

    # call the controller to get the games that match our requirements
    _games = get_games(game_id=game_id)

    # convert the list of games objects to a list of dictionaries
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
                }
                for user in game.users
            ],
        }
        for game in _games
    ]

    return games



def get_latest_turn(game_id, user_id):
    # print(game_id)
    # print(user_id)
    latest_turn_info = (
        TurnInfo.query.filter_by(game_id=game_id)
        .filter_by(user_id=user_id)
        .order_by(TurnInfo.id.desc())
        .first()
    )
    return latest_turn_info

def test_for_same_turn(game_id):
        # begin query to find all players last turn
        # return dict of game info
        current_game_users = get_games_users_dict(game_id)

        # save the list of user dicts
        user_list = current_game_users[0]['users']

        # initiate list to store max turn numbers
        max_turn_list = []

        for user in user_list:
            # iterate over each user to find max turn for this game
            max_turn = get_latest_turn(game_id, user['id'])
            # if user hasn't played a turn, none is returned, change that to zero
            if max_turn == None:
                max_turn_number = 0
            else:
                max_turn_number = max_turn.current_round
            # append this users turn to list
            max_turn_list.append(max_turn_number)

        # test to see if all users have same turn number
        if(len(set(max_turn_list))==1):
            same_turn = True
        else:
            same_turn = False

        return same_turn
