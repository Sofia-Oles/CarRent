from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError


class Car(db.Model):

    __tablename__ = "car"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Integer, nullable=False)
    people_count = db.Column(db.Integer, nullable=False)
    car = db.relationship("Order",
                          cascade="all,delete",
                          backref="car")
