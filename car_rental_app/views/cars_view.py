from flask import render_template, url_for, redirect, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired

from . import public_blueprint
from ..service import car_service


class CarForm(FlaskForm):
    """
    Form for admin to create new car
    """
    name = StringField(validators=[Length(min=5, max=50), DataRequired()])
    model = StringField(validators=[Length(min=1, max=50), DataRequired()])
    year = IntegerField(validators=[DataRequired()])
    price_per_day = IntegerField(validators=[DataRequired()])
    people_count = IntegerField(validators=[DataRequired()])
    submit = SubmitField(label="Add car!")


@public_blueprint.route("/cars", methods=["GET", "POST"])
def show_cars():
    """
    Render the cars page template
    """
    cars = car_service.read_all_cars()
    return render_template("cars.html", cars=cars)


@public_blueprint.route("/car/add", methods=["GET", "POST"])
@login_required
def car_page():
    """
    Add a car to the database through the car form
    """
    form = CarForm()
    if form.validate_on_submit():
        new_car = car_service.create_car(name=form.name.data,
                                         model=form.model.data,
                                         year=form.year.data,
                                         price_per_day=form.price_per_day.data,
                                         people_count=form.people_count.data)
        if new_car:
            flash(f"Car was created successfully!", category="success")
            # redirect to the cars page
            return redirect(url_for("public.show_cars"))
        else:
            flash(f"Check your car data!", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    # load template
    return render_template("car.html", form=form)

