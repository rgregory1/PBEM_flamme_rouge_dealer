import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, current_user, logout_user
import controller

from pprint import pprint


# we need user from models, so we grab it here
from models import User, TurnInfo, Game, game_to_user

# all we need is login_manager, so grab it from comnfig here
from config import login_manager, db, logger


member = Blueprint("member", __name__, template_folder="member")


@login_manager.user_loader
def load_user(user_id):
    # I like this style just because it's more explicit
    return User.query.filter(User.id == int(user_id)).first()


@member.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()

        if not user:
            return "user does not exixt"

        login_user(user, remember=True)

        if "next" in session:
            next = session["next"]

            if next is not None:
                return redirect(next)

        return redirect(url_for("member.member_page"))
    session["next"] = request.args.get("next")
    return render_template("member/login.html")


@member.route("/member_page")
@login_required
def member_page():
    # remove session keys, keep the flashed messages though
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']
    # create blank list to fill with game info
    member_games_info = []

    # get dict of user info including games registered for
    _users = controller.get_users_dict(current_user.id)
    users = _users[0]

    for game in users["games"]:
        # create empty dict for each game
        this_game_info = {}
        # id and game name
        this_game_info["game_id"] = game["id"]
        this_game_info["name"] = game["name"]
        # use game id to see if data for game is stored in TurnInfo table if it's there,
        # return the last turns number
        this_turn_data = controller.get_latest_turn(game["id"], current_user.id)

        # assign
        if this_turn_data:
            this_game_info["current_round"] = this_turn_data.current_round
            this_game_info["turn_id"] = this_turn_data.id
        else:
            this_game_info["current_round"] = None

        member_games_info.append(this_game_info)

    return render_template(
        "member/member_page.html", member_games_info=member_games_info
    )


# This is a mirror of your 'member_page_doug' and you can see
# this work by navigating to /member_page_doug.
@member.route("/member_page_doug")
@login_required
def member_page_doug():
    # only for testing purposes
    session["PBEM"] = True

    # I removed the query that was here as you can just
    # use the function you have that returns the user_id
    # from the session.

    # use the currently logged in user id value to get the user
    users = controller.get_users(current_user.id)

    # did we get a list of users?
    if users:

        # get the single user we expect from that list
        user = users[0]

    # log the user to stdout
    logger.debug(f"Here is the user data returned for this user.id = {current_user.id}")
    logger.debug(user)

    # iterate over the user's games
    for game in user.games:

        # get the turns associated with the user's games
        turns = controller.get_turns(user.id, game.id)

        # append the list of turns to this user game
        game.turns = turns

    return render_template(
        "member/member_page_doug.html",
        user=user
    )


@member.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@member.route("/save_turn")
@login_required
def save_turn():
    # freeze the state to come back to the beginning of the round
    freeze_state = dict(session)
    frozen_data = json.dumps(freeze_state)
    summary_data = json.dumps(session["chosen_cards"])
    turn_data = TurnInfo(
        user_id=current_user.id,
        game_id=session["game_id"],
        current_round=session["round"],
        turn_data=frozen_data,
        summary_data=summary_data,
    )
    db.session.add(turn_data)
    db.session.commit()
    return redirect(url_for("member.member_page"))


@member.route("/play_next_turn/<turn_id>", methods=["POST", "GET"])
@login_required
def play_next_round(turn_id):
    raw_turn_data = TurnInfo.query.filter_by(id=turn_id).first()
    this_turn_data = json.loads(raw_turn_data.turn_data)
    session.clear()
    for key in this_turn_data:
        session[key] = this_turn_data[key]
    return render_template("hidden_cards.html")


@member.route("/create_game_form")
@login_required
def create_game_form():

    return render_template("member/create_game_form.html")


@member.route("/create_game", methods=["POST", "GET"])
@login_required
def create_game():
    options = {"is_meteo": False, "breakaway_option": False}
    if "is_meteo" in request.form:
        options["is_meteo"] = True

    # begin dealing with breakaway options
    if "breakaway_option" in request.form:
        # setup the breakaway variables
        options["breakaway_option"] = True
    frozen_options = json.dumps(options)
    race_name = request.form["race_name"]
    race_limit = request.form["race_limit"]
    new_race = Game(
        creator=current_user.id,
        name=race_name,
        active=True,
        limit=race_limit,
        options=frozen_options,
    )
    db.session.add(new_race)
    db.session.commit()
    return redirect(url_for("member.member_page"))


@member.route("/join_game", methods=["POST", "Get"])
@login_required
def join_game():
    game_number = request.form["join_game"]

    # test if string is not empty and contains numbers
    if game_number is not "" and game_number.isdigit():
        # test if game is in database
        game_on = (
            db.session.query(Game.id).filter_by(id=game_number).scalar() is not None
        )
        if game_on:
            # if game is in database, add user to game
            try:
                joiner = game_to_user.insert().values(
                    game_id=game_number, user_id=current_user.id
                )
                # joiner = game_to_user(game_id=game_number, user_id=current_user.id)
                db.session.execute(joiner)
                db.session.commit()
            except:
                flash("Already registered")
            return redirect(url_for("member.member_page"))
        else:
            flash("No such game")
    else:
        flash("Invalid Entry")
    return redirect(url_for("member.member_page"))


@member.route("/initial_PBEM_turn/<game_id>", methods=["POST", "GET"])
@login_required
def initial_PBEM_turn(game_id):
    session.clear()
    session["game_id"] = game_id
    session["PBEM"] = True
    game_data = Game.query.filter_by(id=game_id).first()
    # print("\n---------------------\n")
    # print(frozen_options)
    options = json.loads(game_data.options)
    session["is_meteo"] = options["is_meteo"]
    session["breakaway_option"] = options["breakaway_option"]
    return render_template("member/PBEM_home.html")


# @member.route("/setup", methods=["POST", "GET"])
# @login_required
# def setup():
#     # collect form info
#     team_color = request.form["team_color"]
#
#     initialize_session()
#     load_player_deck(team_color)
#     check_for_ai_teams()
#
#     # general options checked
#     if "exhaustion_reminder" in request.form:
#         session["is_exhaustion_reminder"] = request.form["exhaustion_reminder"]
#
#     if "view_played" in request.form:
#         session["view_played"] = request.form["view_played"]
#
#     # begin dealing with breakaway options
#     if "breakaway_option" in request.form:
#         # setup the breakaway variables
#         session["breakaway_option"] = request.form["breakaway_option"]
#         session.modified = True
#         return render_template("breakaway/breakaway_deck_choice.html")
#     session.modified = True
#     return redirect(url_for("choose_deck"))
