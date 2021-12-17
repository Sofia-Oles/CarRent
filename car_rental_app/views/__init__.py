from flask import render_template
from flask import Blueprint, url_for

users = Blueprint("users", __name__)

from . import cars_view


@users.route("/")
def home():
    """
    Render the home page template
    """
    return render_template("index.html")



