"""
This module represents endpoints: /register, /login and /logout
"""
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

from .. import bcrypt
from . import public_blueprint

from ..models.passport import Passport
from ..models.user import User
from ..service import user_service, passport_service


class RegisterForm(FlaskForm):
    """
    Form for users to create new account
    """
    series = StringField(validators=[Length(min=1, max=2), DataRequired()])
    number = IntegerField(validators=[DataRequired()])
    published_by = IntegerField(validators=[DataRequired()])
    birth_date = DateField(validators=[InputRequired()])

    email = StringField(validators=[DataRequired(), Email()])
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[Length(min=4), DataRequired()])
    confirm_password = PasswordField(validators=[
        EqualTo("password"),
        DataRequired()
    ])
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    """
    Form for users to log in
    """
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField(label="Login")


@public_blueprint.route("/register", methods=["GET", "POST"])
def register_page():
    """
    Handle requests to the /register endpoint
    Add a passport and a user to the database through the registration form
    """
    form = RegisterForm()
    if form.validate_on_submit():
        passport = Passport.query.filter_by(number=form.number.data).first()
        if passport:
            flash("Passport with this number already exist!")
            return render_template("register.html", form=form)
        user = User.query.filter_by(login=form.email.data).first()
        if user:
            flash("User with this login already exist!Try to sign in.")
            return render_template("register.html", form=form)

        new_passport = passport_service.create_passport(series=form.series.data,
                                                        number=form.number.data,
                                                        published_by=form.published_by.data,
                                                        date_of_birth=form.birth_date.data)
        if new_passport:
            new_user = user_service.create_user(
                login=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                passport=new_passport,
                password=bcrypt.generate_password_hash(form.password.data))

            login_user(new_user)
            flash(f'Account created successfully! You are now logged in '
                  f'as {new_user.login}', category="success")

            # redirect to the cars page
            return redirect(url_for("public.show_cars"))
        flash(f"Check your passport data!", category="danger")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    # load template
    return render_template("register.html", form=form)


@public_blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    """
    Handle requests to the /login endpoint
    Check if user is in database through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Success! You are logged in as: {user.login}", category="success")

                # redirect to the cars page after login
                return redirect(url_for("public.show_cars"))
            flash("Wrong password! Please try again!", category="danger")
        else:
            flash("This login doesn`t exist!", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    # load login template
    return render_template("login.html", form=form)


@public_blueprint.route("/logout")
@login_required
def logout_page():
    """
    Handle requests to the /logout route
    Allow users to logout.
    """
    logout_user()
    flash("You have been logged out!", category="info")
    # redirect to the login page
    return redirect(url_for("public.login_page"))
