from car_rental_app import db, ma
from marshmallow import Schema, fields, validate, ValidationError


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, default=0)
    passport_id = db.Column(db.Integer,
                            db.ForeignKey("passport.id"))
    password = db.Column(db.String(10), nullable=False)

    user = db.relationship("Order",
                           backref="creator")

    def replenish_balance(self, balance):
        self.balance = balance

    def save(self):
        db.session.add(self)
        db.session.commit()


# class UserSchema(Schema):
#     login = fields.String(required=True)
#     password = fields.String(validate=validate.Length(min=4), required=True)
#     # password2 = fields.String(validate=validate.Length(min=8), required=True)
