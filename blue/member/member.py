from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_login import login_user, login_required, current_user, logout_user


# we need user from models, so we grab it here
from models import User


# all we need is login_manager, so grab it from comnfig here
from config import login_manager


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
    return render_template("member/member_page.html")


@member.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
