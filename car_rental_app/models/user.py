from flask_login import UserMixin

from car_rental_app import db, login_manager
from marshmallow import Schema, fields, validate


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, default=0)
    passport_id = db.Column(db.Integer, db.ForeignKey("passport.id"))
    password = db.Column(db.String(10), nullable=False)

    user = db.relationship("Order",
                           cascade="all,delete",
                           backref="creator")

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the department in json format
        """
        return {
             "id": self.id,
             "login": self.login,
             "name": self.name,
             "surname": self.surname,
             "balance": self.balance,
             "passport_data": self.passport.to_dict()
        }


class UserSchema(Schema):
    """
    Marshmallow.Schema makes it easy to check for the existence and data types of fields,
    which can be inserted to User table.
    """
    login = fields.Email(required=True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    password = fields.String(validate=validate.Length(min=4), required=True)
    password2 = fields.String(validate=validate.Length(min=4), required=True)


@login_manager.user_loader
def load_user(user_id):
    """
    :param user_id:
    :return: user obj
    """
    return User.query.get(int(user_id))
