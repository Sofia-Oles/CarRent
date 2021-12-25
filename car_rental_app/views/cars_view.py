import datetime
from flask import render_template, url_for, request, jsonify
from flask_restful.inputs import date
from flask import Blueprint

public_blueprint = Blueprint("public", __name__)


@public_blueprint.route("/")
def home():
    """
    Render the home page template for public users
    """
    return render_template("index.html")


@public_blueprint.route("/all")
def show_cars():
    """
    Render the cars page template
    """
    return render_template("cars.html")


@public_blueprint.route("/User", methods=['POST'])
def register():
    from ..models.user import User
    from ..models.order import Order
    from ..models.passport import Passport
    from ..models.car import Car
    from ..models.administrator import Administrator

    data = request.get_json()
    # {
    #     "login": "NOTE7", "name": "ckk", "surname": "NOTE7", "password": "coooooook"
    # }

    # {
    #     "series": "CC", "number": 126099823, "published_by": 4622, "date_of_birth": "2001-12-22"
    # }

    series = data.get('series')
    number = data.get('number')
    published_by = data.get('published_by')
    date_of_birth = data.get('date_of_birth')
    data_to = date(date_of_birth)

    # login = data.get('login')
    name = data.get('name')
    # surname = data.get('surname')
    # password = data.get('password')

    new_passport = Passport(series=series, number=number, published_by=published_by, date_of_birth=data_to)
    new_passport.save()
    #
    new_user = User(login="Taras@gmail.com", name="hjjhxxc", surname="GGG", password="9999999",
                    passport=new_passport)  # backref
    new_user.save()

    new_car = Car(name=name, model="model 4", year=2019, price_per_day=40, people_count=4)
    new_car.save()

    car = Car.query.filter_by(id=1).first()

    user = User.query.filter_by(id=1).first()
    datetime_object = datetime.datetime(2020, 1, 9)
    data_to = datetime_object.replace(hour=9, minute=00)
    data_end = date("2001-12-22")
    new_order = Order(creator=user, car=car, start_date=data_to,
                      end_date=data_end, price=100)
    new_order.save()

    adm = Administrator(login="admin", password="admin")
    adm.save()

    return jsonify(message="The user was created", status=200)


@public_blueprint.route("/test", methods=['POST', 'GET'])
def tes():
    from ..models.user import User
    from ..models.order import Order
    from ..models.passport import Passport
    from ..models.car import Car
    from ..models.administrator import Administrator

    from ..service.car_service import read_all_cars, read_car_by_id, update_car
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    model = data.get('model')

    cars = Car.query.all()
    update_car(id, name, model=model)
    return jsonify(status=200)
    # read_car_by_id(1)
    # render_template('cars.html', cars=cars)
