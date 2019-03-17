import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user
import controller

from pprint import pprint


# we need user from models, so we grab it here
from models import User, TurnInfo, Game

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
    # only for testing purposes
    session["PBEM"] = True

    # changed this to use the version that passes a user id
    users = controller.get_users(current_user.id)

    # did we get a list of users?
    if users:
        user = users[0]

    member_games_info = []
    # Ok i got nothing else, lets put this Here
    _users_trial = controller.get_users_dict(current_user.id)
    users_trial = _users_trial[0]
    # print("\nhere is the user dict\n")
    # pprint(users_trial)

    for game in users_trial["games"]:
        this_game_info = {}
        this_game_info["game_id"] = game["id"]
        this_game_info["name"] = game["name"]
        this_turn_data = controller.get_latest_turn(game["id"], current_user.id)
        # print("----------------------------------")
        # print("----------------------------------")
        # print("this is the turn data")
        # print("\n")
        # print(this_turn_data)
        if this_turn_data:
            this_game_info["current_round"] = this_turn_data.current_round
        else:
            this_game_info["current_round"] = None
        # print("----------------------------------")
        # print("this is the game info")
        # print("\n")
        # pprint(this_game_info)
        member_games_info.append(this_game_info)
    print("----------------------------------")
    print("----------------------------------")
    print("this is the member games info")
    print("\n")
    pprint(member_games_info)
    return render_template(
        "member/member_page.html", user=user, member_games_info=member_games_info
    )


# preserved member page so I don't blow the whole thing
# @member.route("/member_page")
# @login_required
# def member_page():
#     # only for testing purposes
#     session["PBEM"] = True
#     current_turn_info = (
#         TurnInfo.query.filter_by(user_id=current_user.id)
#         .order_by(TurnInfo.id.desc())
#         .first()
#     )
#
#
#     # changed this to use the version that passes a user id
#     users = controller.get_users(current_user.id)
#
#     # did we get a list of users?
#     if users:
#         user = users[0]
#
#     # log the list of games to stdout
#     logger.debug("Here is the user list returned for this user")
#     logger.debug(user)
#
#
#     return render_template(
#         "member/member_page.html",
#         current_turn_info=current_turn_info,
#         user=user
#     )


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
    turn_data = TurnInfo(
        user_id=current_user.id,
        game_id=1,
        current_round=session["round"],
        turn_data=frozen_data,
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
    race_name = request.form["race_name"]
    race_limit = request.form["race_limit"]
    new_race = Game(
        creator=current_user.id, name=race_name, active=True, limit=race_limit
    )
    db.session.add(new_race)
    db.session.commit()
    return redirect(url_for("member.member_page"))
