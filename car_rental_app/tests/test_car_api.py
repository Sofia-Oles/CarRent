import http
import json

from unittest.mock import patch
import unittest
from car_rental_app import create_app
from car_rental_app import db
from car_rental_app.models.car import Car
from car_rental_app.tests.base import BaseTestCase


class TestCarApi(BaseTestCase):
    """
    This is the class for car_api test cases
    """

    def test_get(self):
        """
        Testing the get request to /api/cars.
        It should return the status code 200
        """
        client = create_app().test_client()
        response = client.get("/api/cars")
        assert response.json["status"] == http.HTTPStatus.OK

    @patch(
        "car_rental_app.service.car_service.read_all_cars",
        autospec=True,
        return_value=[],
    )
    def test_get_car_with_mock_db(self, mock_requests):
        """
        Testing the get request to /api/cars with mock method read_all_cars.
        It should return the status code 200 and an empty list
        """
        client = create_app().test_client()
        response = client.get("/api/cars")
        mock_requests.assert_called_once()
        assert response.json["status"] == http.HTTPStatus.OK
        assert len(response.json["cars_data"]) == 0

    def test_get_car_by_id(self):
        """
        Testing the get request to /api/car/<id>
        It should return the status code 200
        """
        car = Car(
            name="Smart",
            model="DF6792",
            year=2015,
            price_per_day=75,
            people_count=2,
        )
        db.session.add(car)
        db.session.commit()

        client = create_app().test_client()
        response = client.get("/api/car/1")
        assert len(response.json["car_data"]) != 0
        assert response.json["status"] == http.HTTPStatus.OK

    def test_post_car_with_mock(self):
        """
        Testing the post request to /api/car with mock
        """
        with patch(
            "car_rental_app.db.session.add", autospec=True
        ) as mock_session_add, patch(
            "car_rental_app.db.session.commit", autospec=True
        ) as mock_session_commit:
            client = create_app().test_client()
            data = {
                "name": "Land Cruiser",
                "model": "DF6732",
                "year": 2017,
                "price_per_day": 100,
                "people_count": 6,
            }
            response = client.post(
                "/api/cars",
                data=json.dumps(data),
                content_type="application/json",
            )
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert response.json["status"] == http.HTTPStatus.CREATED

    def test_post_car_fail(self):
        """
        Testing the post request to /api/car with 400
        """
        client = create_app().test_client()
        data = {}
        response = client.post(
            "/api/cars",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.json["status"] == http.HTTPStatus.BAD_REQUEST

    def test_put_car(self):
        """
        Testing the put request to /api/car/<id>.
        First create instance of car in test db. Than update.
        It should return the status code 200
        """
        car = Car(
            name="Smart",
            model="DF6792",
            year=2015,
            price_per_day=75,
            people_count=2,
        )
        db.session.add(car)
        db.session.commit()

        client = create_app().test_client()
        url = "/api/car/1"
        data = {
            "name": "UPDATED Cruiser",
            "model": "UPDATED",
        }
        response = client.put(
            url,
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.json["status"] == http.HTTPStatus.OK

    def test_delete_car_with_mock(self):
        """
        Testing the post request to /api/car/id with mock
        """
        with patch(
            "car_rental_app.db.session.delete", autospec=True
        ) as mock_session_del, patch(
            "car_rental_app.db.session.commit", autospec=True
        ) as mock_session_commit:
            client = create_app().test_client()
            response = client.delete("/api/car/1", content_type="application/json")
            mock_session_del.assert_called_once()
            mock_session_commit.assert_called_once()
            assert response.json["status"] == http.HTTPStatus.OK


if __name__ == "__main__":
    unittest.main()
