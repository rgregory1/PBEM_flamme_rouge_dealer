"""
This module exists to create the program configuration
(including database connection) and provide
a way for all other modules to access this configuration
information
"""

# system modules
import os
import logging

# 3rd party modules
import pathlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_debugtoolbar import DebugToolbarExtension


# create the application instance we'll use everywhere
app = Flask(__name__)


# DEBUG_TB_INTERCEPT_REDIRECTS = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Set the secret key to the debugtoolbar
app.secret_key = "my_secret"

# the toolbar is only enabled in debug mode:
app.debug = True
toolbar = DebugToolbarExtension(app)


# create the login manager instance we'll use everyhere
login_manager = LoginManager(app)
# redirect to login page if trying to get to protected Page
login_manager.login_view = "member.member_login"


# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["SECRET_KEY"] = "not_very_secret"

# Build the Sqlite ULR for SqlAlchemy
basedir = pathlib.Path(__file__).parent.resolve()
basedir_os = os.path.abspath(os.path.dirname(__file__))
sqlite_url = "sqlite:////" + os.path.join(basedir_os, "flamme_rouge.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["USE_SESSION_FOR_NEXT"] = True

# Create the SqlAlchemy db instance we'll use everywhere
db = SQLAlchemy(app)

# create a logger instance that can be used everywhere
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("flamme")
