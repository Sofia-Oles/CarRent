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
        self.assertEqual(2, len(car_service.read_all_cars()))

    def test_read_car(self):
        car1 = Car(name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        db.session.add(car1)
        db.session.commit()
        car = car_service.read_car_by_id(1)
        self.assertEqual(car1.id, car.id)

    def test_update_car(self):
        car = Car(name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        db.session.add(car)
        db.session.commit()
        old_data = car.to_dict()
        data_to_update = {"name": "UPDATED", "year": 2016}
        car_service.update_car(1, data_to_update)
        self.assertNotEqual(old_data["name"], Car.query.get(1).name)
        self.assertNotEqual(old_data["year"], Car.query.get(1).year)

    def test_delete_car(self):
        car = Car(name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        db.session.add(car)
        db.session.commit()
        car_service.delete_car(1)
        self.assertEqual(0, Car.query.count())


if __name__ == "__main__":
    unittest.main()
