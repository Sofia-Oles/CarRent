"""
Module contains all views blueprints.
Blueprints:
    public_blueprint
    admin_blueprint
"""
from flask import render_template
from flask import Blueprint

public_blueprint = Blueprint("public", __name__)
admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

from . import auth_view
from . import cars_view
from . import user_view
from . import order_view
from . import auth_view


@public_blueprint.route("/")
def home():
    """
    Render the page template for users
    """
    return render_template("index.html")
