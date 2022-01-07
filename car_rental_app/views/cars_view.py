from flask import render_template, url_for, redirect

from . import public_blueprint
from ..service import car_service


@public_blueprint.route("/cars", methods=["GET", "POST"])
def show_cars():
    """
    Render the cars page template
    """
    cars = car_service.read_all_cars()
    return render_template("cars.html", cars=cars)


@public_blueprint.route("/cars/add", methods=["GET", "POST"])
def add_car():
    """
    Form to add or edit car
    """
    return redirect(url_for("public.show_cars"))  # blueprint_name.func_name

