from flask import render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from marshmallow import ValidationError
from wtforms import PasswordField, StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, NumberRange

from log import logger
from . import public_blueprint
from flask_login import logout_user, login_required, current_user

from .. import bcrypt
from ..models.user import UserSchema, User
from ..service import user_service
from ..service.passport_service import read_passport_by_id


class UserForm(FlaskForm):
    """
    Form to edit user
    """
    name = StringField()
    surname = StringField()
    password = PasswordField()
    submit = SubmitField(label="Save")


class BalanceForm(FlaskForm):
    balance = IntegerField(validators=[DataRequired(), NumberRange(min=50, message="Must enter a number greater than 50")])
    submit = SubmitField(label="Save")


@public_blueprint.route("/profile", methods=["GET"])
@login_required
def profile_page():
    """
    Render the profile page template
    """
    return render_template("profile.html")


@public_blueprint.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    """
    Edit user data
    """
    form = UserForm()
    data_to_validate = dict()
    # validate data from forms
    if form.validate_on_submit():
        for key, value in form.data.items():
            if value and key != "csrf_token" and key != "submit":
                data_to_validate[key] = value
        try:
            UserSchema().load(data_to_validate, partial=True)
        except ValidationError as err:
            flash(f"{err.messages}")
        try:
            if data_to_validate["password"]:
                data_to_validate["password"] = bcrypt.generate_password_hash(data_to_validate["password"])
        except:
            logger.error(f"Failed to hash password!")
        user_service.update_user(current_user.id, data_to_validate)
        flash("You have successfully edited your personal info.", category="success")
        # redirect to the profile page
        return redirect(url_for("public.profile_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    return render_template("edit_profile.html", form=form)


@public_blueprint.route("/profile/delete", methods=["GET", "POST"])
@login_required
def delete_user():
    """
    Delete user from system
    """
    try:
        user_service.delete_user(current_user.id)
        return redirect(url_for("register.html"))
    except:
        logger.error(f"Failed delete user!")
        return render_template("profile.html")


@public_blueprint.route("/balance", methods=["GET", "POST"])
@login_required
def edit_balance():
    """
    Retrieve balance
    """
    form = BalanceForm()
    if form.validate_on_submit():
        user_service.update_user_balance(current_user.id, form.balance.data)
        flash("You have successfully edited your personal info.", category="success")
        # redirect to the profile page
        return redirect(url_for("public.profile_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    return render_template("edit_balance.html", form=form)

