import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user


# we need user from models, so we grab it here
from models import User, TurnInfo


# all we need is login_manager, so grab it from comnfig here
from config import login_manager, db


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
    current_turn_info = (
        TurnInfo.query.filter_by(user_id=current_user.id)
        .order_by(TurnInfo.id.desc())
        .first()
    )
    return render_template(
        "member/member_page.html", current_turn_info=current_turn_info
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
    turn_data = TurnInfo(
        user_id=current_user.id,
        game_id=101,
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
