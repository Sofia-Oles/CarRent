import unittest
from car_rental_app.tests.base import BaseTestCase

from car_rental_app import db
from car_rental_app.models.car import Car
from car_rental_app.service import car_service


class TestCarService(BaseTestCase):

    def test_create_car(self):
        car_service.create_car(name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        self.assertEqual(1, Car.query.count())

    def test_read_all_cars(self):
        car1 = Car(name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        car2 = Car(name="Smart", model="DF6792", year=2015, price_per_day=75, people_count=2)
        db.session.add(car1)
        db.session.add(car2)
        db.session.commit()
        self.assertEqual(2, car_service.read_all_cars())


if __name__ == "__main__":
    unittest.main()
