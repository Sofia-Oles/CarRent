from car_rental_app import db


class Order(db.Model):

    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_date = db.Column(db.DateTime, nullable=False, server_default="09:00")
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the car in json format
        """
        return {
            "id": self.id,
            "user_login": self.creator.login,
            "car_name": self.car.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": self.price
        }
