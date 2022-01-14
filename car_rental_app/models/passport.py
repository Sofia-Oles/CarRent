from car_rental_app import db
from marshmallow import Schema, fields, validate


class Passport(db.Model):

    __tablename__ = "passport"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series = db.Column(db.String(2), default=None)
    number = db.Column(db.Integer, unique=True, nullable=False)
    published_by = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    user = db.relationship(
        "User", uselist=False, cascade="all,delete", backref="passport"
    )

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the passport in json format
        """
        return {
            "id": self.id,
            "series": self.series,
            "number": self.number,
            "published_by": self.published_by,
            "date_of_birth": self.date_of_birth,
        }


class PassportSchema(Schema):
    """
    Marshmallow.Schema makes it easy to check for the existence and data types of fields,
    which can be inserted to Passport table.
    """

    series = fields.String(validate=validate.Length(equal=2), required=True)
    number = fields.Integer(required=True)
    published_by = fields.Integer(required=True)
    date_of_birth = fields.Date(required=True)
