from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError


class Passport(db.Model):

    __tablename__ = "passport"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series = db.Column(db.String(2), default=None)
    number = db.Column(db.Integer, unique=True, nullable=False)
    published_by = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    user = db.relationship("User",
                           uselist=False,
                           cascade="all,delete",
                           backref="passport")
