import unittest
from datetime import date

from car_rental_app.tests.base import BaseTestCase

from car_rental_app import db
from car_rental_app.models.passport import Passport
from car_rental_app.service import passport_service


test_passport = {
    "series": "KC",
    "number": 22899239,
    "published_by": 4920,
    "date_of_birth": date.fromisoformat("2001-12-04"),
}


class TestPassportService(BaseTestCase):
    def test_create_passport(self):
        passport = passport_service.create_passport(**test_passport)
        self.assertEqual(1, Passport.query.count())

    def test_read_passport(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        self.assertEqual(1, passport_service.read_passport_by_id(1).id)

    def test_update_passport(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        old_data = passport.to_dict()
        data_to_update = {"series": "PP", "number": 999999999}
        passport_service.update_passport(1, data_to_update)
        self.assertNotEqual(old_data["series"], Passport.query.get(1).series)
        self.assertNotEqual(old_data["number"], Passport.query.get(1).number)


if __name__ == "__main__":
    unittest.main()
