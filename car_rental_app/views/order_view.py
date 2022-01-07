"""
This module represents endpoints: /register, /login and /logout
"""
import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, ValidationError

from log import logger
from .. import bcrypt
from . import public_blueprint

from ..models.passport import Passport
from ..models.user import User
from ..service import user_service, passport_service, car_service, order_service


class OrderForm(FlaskForm):
    start_date = DateField(validators=[InputRequired()])
    end_date = DateField(validators=[InputRequired()])
    submit = SubmitField(label="Order!")

    @staticmethod
    def validate_date(form):
        if form.start_date.data < datetime.date.today() or form.end_date.data < datetime.date.today():
            flash(f"Start and End dates cannot be in the past!", category="danger")
            return None
        elif form.start_date.data > form.end_date.data:
            flash(f"The start date cannot be greater than end date", category="danger")
            return None
        return True


@public_blueprint.route("/order/<car_id>", methods=["GET", "POST"])
@login_required
def order_page(car_id):
    car = car_service.read_car_by_id(car_id)
    form = OrderForm()
    if form.validate_on_submit() and form.validate_date(form):
        start_date = form.start_date.data
        end_date = form.end_date.data
        # check if dates is available
        orders = order_service.retrieve_busy_dates(car_id, start_date, end_date)
        # enough balance
        user = user_service.read_user_by_id(current_user.id)
        if user.balance <= ((end_date - start_date).days * car.price_per_day):
            flash("Balance too low! You can retrieve it", category="danger")
            # redirect to your retrieving page
            return redirect(url_for("public.edit_balance"))
        if not orders:
            order_service.create_order(user_id=current_user.id,
                                       car_id=car_id,
                                       start_date=start_date,
                                       end_date=end_date,
                                       price=(end_date - start_date).days * car.price_per_day)
            flash("The order was created!", category="success")
            # redirect to your orders page
            return redirect(url_for("public.show_cars"))
        flash(f"These dates are busy. Choose another dates!", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating order: {err_msg}", category="danger")
    return render_template("order.html", car=car, form=form)
