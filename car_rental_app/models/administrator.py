from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError


class Administrator(db.Model):

    __tablename__ = "administrator"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
