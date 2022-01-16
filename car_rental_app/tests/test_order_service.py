import unittest
from datetime import date
from car_rental_app.tests.base import BaseTestCase

from car_rental_app import db
from car_rental_app.models.user import User
from car_rental_app.models.car import Car
from car_rental_app.models.passport import Passport
from car_rental_app.models.order import Order
from car_rental_app.service import user_service, car_service, order_service

test_car = {
    "name": "Land Cruiser",
    "model": "DF6732",
    "year": 2017,
    "price_per_day": 75,
    "people_count": 5,
}
test_passport = {
    "series": "KC",
    "number": 22899239,
    "published_by": 4920,
    "date_of_birth": date.fromisoformat("2001-12-04"),
}
test_user = {
    "login": "test_user@gmail.com",
    "name": "Ivan",
    "surname": "Ivanov",
    "password": "12345super",
}
test_order = {
    "start_date": date.fromisoformat("2022-01-04"),
    "end_date": date.fromisoformat("2022-01-14"),
    "price": 550,
}
test_order2 = {
    "start_date": date.fromisoformat("2022-02-04"),
    "end_date": date.fromisoformat("2022-02-14"),
    "price": 800,
}


class TestOrderService(BaseTestCase):
    def test_create_order(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        user = User(passport=passport, **test_user)
        db.session.add(user)
        car = Car(**test_car)
        db.session.add(car)
        db.session.commit()
        order_service.create_order(1, 1,  **test_order)
        order_service.create_order(1, 1, **test_order2)
        self.assertEqual(2, Order.query.count())

    def test_read_all_orders(self):
        self.test_create_order()
        self.assertEqual(2, len(order_service.read_all_orders()))

    def test_read_orders_by_user(self):
        self.test_create_order()
        orders = order_service.read_all_orders_by_user_id(1)
        self.assertEqual(2, len(orders))

    def test_read_order_by_id(self):
        self.test_create_order()
        order_from_db = order_service.read_order_by_id(1)
        self.assertEqual(1, order_from_db.id)

    def test_update_order(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        user = User(passport=passport, **test_user)
        db.session.add(user)
        car = Car(**test_car)
        db.session.add(car)
        db.session.commit()
        order = order_service.create_order(1, 1, **test_order)
        old_data = order.to_dict()
        data_to_update = {"start_date": date.fromisoformat("2022-01-06")}
        order_service.update_order(1, data_to_update)
        self.assertNotEqual(old_data["start_date"], Order.query.get(1).start_date)

    def test_delete_order(self):
        self.test_create_order()
        order_service.delete_order(1)
        order_service.delete_order(2)
        self.assertEqual(0, Order.query.count())


if __name__ == "__main__":
    unittest.main()
