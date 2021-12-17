from flask import render_template, url_for
from . import public_blueprint


@public_blueprint.route("/all")
def show_cars():
    """
    Render the cars page template
    """
    return render_template("clients/cars.html")

