from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime, timezone, timedelta


class Order(db.Model):

    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, default=datetime.now(timezone(timedelta(hours=2))))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"))
    order_car = db.relationship("OrderCar", backref="order")

    def save(self):
        db.session.add(self)
        db.session.commit()

