from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError


class Order(db.Model):

    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_date = db.Column(db.DateTime, nullable=False, server_default="09:00")
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
