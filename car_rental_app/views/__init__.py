from flask import render_template
from flask import Blueprint

public_blueprint = Blueprint("public", __name__)

from . import cars_view


@public_blueprint.route("/")
def home():
    """
    Render the home page template for public users
    """
    return render_template("index.html")
