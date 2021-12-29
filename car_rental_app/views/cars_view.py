import datetime as dt
from flask import render_template, url_for, request, jsonify
from flask_restful.inputs import date
from flask import Blueprint
from datetime import datetime

public_blueprint = Blueprint("public", __name__)


@public_blueprint.route("/")
def home():
    """
    Render the home page template for public users
    """
    return render_template("index.html")


@public_blueprint.route("/all")
def show_cars():
    """
    Render the cars page template
    """
    return render_template("cars.html")
