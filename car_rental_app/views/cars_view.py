from flask import render_template, url_for, request, jsonify, redirect
from flask_restful.inputs import date
from flask import Blueprint

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

