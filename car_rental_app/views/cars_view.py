from flask import render_template, url_for, request, jsonify, redirect
from flask_restful.inputs import date
from flask import Blueprint

from car_rental_app.models.passport import Passport
from car_rental_app.service import passport_service

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

#
# @public_blueprint.route("/a", methods=['POST', 'GET'])
# def tr():
#     """
#     Render the cars page template
#     """
#     data = request.get_json()
#     id = data.get('id')
#     passport = Passport.query.get_or_404(id)
#     print(passport)
#     return jsonify(passport)
