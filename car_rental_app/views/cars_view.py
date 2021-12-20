from flask import render_template, url_for, request, jsonify
from flask_restful.inputs import date
from . import public_blueprint


@public_blueprint.route("/all")
def show_cars():
    """
    Render the cars page template
    """
    return render_template("clients/cars.html")


@public_blueprint.route("/User", methods=['POST'])
def register():
    from ..models.user import User
    from ..models.order import Order
    from ..models.passport import Passport
    # {
    #     "login": "NOTE7", "name": "ckk", "surname": "NOTE7", "password": "coooooook"
    # }
    data = request.get_json()
    # {
    #     "series": "BC", "number": 823899823, "published_by": 4622, "date_of_birth": "2001-12-22"
    # }
    series = data.get('series')
    number = data.get('number')
    published_by = data.get('published_by')
    date_of_birth = data.get('date_of_birth')
    data_to = date(date_of_birth)

    # login = data.get('login')
    # name = data.get('name')
    # surname = data.get('surname')
    # password = data.get('password')

    new_passport = Passport(series=series, number=number, published_by=published_by, date_of_birth=data_to)
    new_passport.save()

    new_user = User(login="login2", name="hjjhcxxc", surname="None", password="9999999",
                    passport=new_passport) #backref
    new_user.save()

    new_order = Order(creator=new_user)
    new_order.save()
    return jsonify(message="The user was created", status=200)
