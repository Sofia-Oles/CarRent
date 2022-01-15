from flask import render_template, url_for, redirect, flash
from . import public_blueprint, admin_blueprint
from ..func import prepare_to_service
from ..models.administrator import Administrator
from ..service import car_service
from ..form import CarForm, CarEditForm


@public_blueprint.route("/cars", methods=["GET", "POST"])
def show_cars():
    """
    Render the cars page template
    """
    admin = False
    cars = car_service.read_all_cars()
    return render_template("cars.html", cars=cars, admin=admin)


@admin_blueprint.route("/cars", methods=["GET", "POST"])
def show_cars():
    """
    Render the cars page template for admin
    """
    admin = Administrator.query.get(1)
    cars = car_service.read_all_cars()
    return render_template("cars.html", cars=cars, admin=admin, balance=admin.balance)


@admin_blueprint.route("/car/add", methods=["GET", "POST"])
def car_page():
    """
    Function working on creating car by admin
    :return: redirects to the template of the cars page
    """
    admin = True
    add_car = True
    form = CarForm()
    if form.validate_on_submit():
        new_car = car_service.create_car(
            name=form.name.data,
            model=form.model.data,
            year=form.year.data,
            price_per_day=form.price_per_day.data,
            people_count=form.people_count.data,
        )
        if new_car:
            flash(f"Car was created successfully!", category="success")
            # redirect to the cars page
            return redirect(url_for("public.show_cars", admin=admin))
        else:
            flash(f"Check your car data!", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    # load template
    return render_template("car.html", form=form, add_car=add_car, admin=admin)


@admin_blueprint.route("/car/edit/<id>", methods=["GET", "POST"])
def edit_car(id):
    """
    Function working on editing car by its id
    :param id: id of car
    :return: redirects to the template of the cars page
    """
    admin = True
    add_car = False
    form = CarEditForm()
    if form.validate_on_submit():
        car_service.update_car(id, prepare_to_service(form.data))
        flash(f"Car was created successfully!", category="success")
        # redirect to the cars page
        return redirect(url_for("public.show_cars", admin=admin))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with updating car: {err_msg}", category="danger")
    # load template
    return render_template("car.html", form=form, add_car=add_car, admin=admin)


@admin_blueprint.route("/car/delete/<id>", methods=["GET", "POST"])
def delete_car(id):
    """
    Function working on deleting car by its id
    :param id: id of car
    :return: redirects to the template of the cars page
    """
    admin = True
    try:
        car_service.delete_car(id)
        return redirect(url_for("public.show_cars", admin=admin))
    except:
        flash(f"Failed to delete car with id={id}", category="danger")
        return redirect(url_for("public.show_cars", admin=admin))
