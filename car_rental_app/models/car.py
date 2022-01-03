from car_rental_app import db
from marshmallow import Schema, fields, validate


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

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the car in json format
        """
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "year": self.year,
            "price_per_day": self.price_per_day,
            "people_count": self.people_count
        }


class CarSchema(Schema):
    """
    Marshmallow.Schema makes it easy to check for the existence and data types of fields,
    which can be inserted to Car table.
    """
    name = fields.String(validate=validate.Length(min=5, max=50), required=True)
    model = fields.String(validate=validate.Length(min=1, max=50), required=True)
    year = fields.Integer(required=True)
    price_per_day = fields.Integer(required=True)
    people_count = fields.Integer(required=True)
