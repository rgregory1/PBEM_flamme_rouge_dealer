from flask import (
    Blueprint,
)


from flask_login import login_user, login_required

# we need user from models, so we grab it here
from models import User


# all we need is login_manager, so grab it from comnfig here
from config import login_manager


member = Blueprint("member", __name__, template_folder="member")


@login_manager.user_loader
def load_user(user_id):
    # I like this style just because it's more explicit
    return User.query.filter(User.id == int(user_id)).first()


@member.route("/login")
def member_login():
    user = User.query.filter_by(username="rusti").first()
    login_user(user)
    return """
    <html>
    <head>
        <title>Logged in page</title>
    </head>
    <body>
        <h1>you are logged in</h1>
    </body>
    </html>
    """


@member.route("/member_page")
@login_required
def member_page():
    return """
    <html>
    <head>
        <title>Member Page</title>
    </head>
    <body>
        <h1>you are in a protected page</h1>
    </body>
    </html>
    """
