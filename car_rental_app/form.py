from flask import flash
from flask_wtf import FlaskForm
import datetime
from marshmallow import ValidationError
from wtforms import PasswordField, StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, NumberRange, Optional


class RegisterForm(FlaskForm):
    """
    Form for users to create new account
    """
    series = StringField(validators=[Length(min=1, max=2), DataRequired()])
    number = IntegerField(validators=[DataRequired()])
    published_by = IntegerField(validators=[DataRequired()])
    date_of_birth = DateField(validators=[InputRequired()])

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


class PassportForm(FlaskForm):
    """
    Form for users to edit passport
    """
    series = StringField(validators=[Length(min=1, max=2), Optional()])
    number = IntegerField(validators=[Optional()])
    published_by = IntegerField(validators=[Optional()])
    date_of_birth = DateField(validators=[Optional()])
    submit = SubmitField(label="Save")


class OrderForm(FlaskForm):
    start_date = DateField(validators=[InputRequired()])
    end_date = DateField(validators=[InputRequired()])
    submit = SubmitField(label="Pay!")

    @staticmethod
    def validate_date(form):
        if form.start_date.data < datetime.date.today() or form.end_date.data < datetime.date.today():
            flash(f"Start and End dates cannot be in the past!", category="danger")
            return None
        elif form.start_date.data > form.end_date.data:
            flash(f"The start date cannot be greater than end date", category="danger")
            return None
        return True


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


class CarEditForm(FlaskForm):
    """
    Form for admin to create new car
    """
    name = StringField(validators=[Length(min=5, max=50), Optional()])
    model = StringField(validators=[Length(min=1, max=50), Optional()])
    year = IntegerField(validators=[Optional()])
    price_per_day = IntegerField(validators=[Optional()])
    people_count = IntegerField(validators=[Optional()])
    submit = SubmitField(label="Save!")
