from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_login import login_user, login_required, current_user, logout_user

from functools import wraps

# we need user from models, so we grab it here
from models import User


# all we need is login_manager, so grab it from comnfig here
from config import login_manager, db


admin = Blueprint("admin", __name__, template_folder="admin")


@login_manager.user_loader
def load_user(user_id):
    # I like this style just because it's more explicit
    return User.query.filter(User.id == int(user_id)).first()


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        account_type = current_user.account_type
        if account_type != "admin":
            return redirect(url_for("member.member_page"))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/admin")
@login_required
@admin_login_required
def admin_home():
    users = User.query.all()

    return render_template("admin/admin.html", users=users)


@admin.route("/create_user", methods=["POST", "GET"])
@login_required
@admin_login_required
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    account_type = request.form["account_type"]
    new_user = User(
        username=username, password=password, email=email, account_type=account_type
    )
    db.session.add(new_user)
    db.session.commit()
    users = User.query.all()

    return redirect(url_for("admin.admin_home"))


@admin.route("/create_user_form")
@login_required
@admin_login_required
def create_user_form():

    return render_template("admin/create_user_form.html")
