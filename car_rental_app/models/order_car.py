from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime, timezone, timedelta


class OrderCar(db.Model):

    __tablename__ = "order_car"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

