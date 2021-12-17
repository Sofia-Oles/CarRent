from flask import render_template, url_for
from . import users


@users.route("/all")
def show_cars():
    """
    Render the cars page template
    """
    return render_template("clients/cars.html")

