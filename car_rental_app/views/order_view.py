"""
This module represents endpoints: /register, /login and /logout
"""
import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import public_blueprint, admin_blueprint
from ..func import change_time
from ..form import OrderForm
from ..service import user_service, car_service, order_service, admin_service


@admin_blueprint.route("/orders", methods=["GET", "POST"])
def show_orders():
    """
    Function working on reading all orders
    :return: the template of the orders page
    """
    admin = True
    orders = order_service.read_all_orders()
    return render_template("orders.html", orders=orders, admin=admin)


@public_blueprint.route("/my_orders", methods=["GET", "POST"])
@login_required
def show_user_orders():
    """
    Function working on reading all orders by current user
    :return: redirects to the template of the orders page
    """
    admin = False
    orders = order_service.read_all_orders_by_user_id(current_user.id)
    if not orders:
        flash(f"You have not orders! Choose car for yourself!", category="danger")
        return redirect(url_for("public.show_cars"))
    return render_template("orders.html", orders=orders, admin=admin)


@public_blueprint.route("/order/<car_id>", methods=["GET", "POST"])
@login_required
def order_page(car_id):
    """
    Function working on creating order by current user
    :param car_id: id of car, user want to order
    :return: redirects to the template of the profile_page
    """
    car = car_service.read_car_by_id(car_id)
    form = OrderForm()
    if form.validate_on_submit() and form.validate_date(form):
        start_date = form.start_date.data
        end_date = form.end_date.data
        # check if dates is available
        orders = order_service.retrieve_busy_dates(car_id, start_date, end_date)
        # enough balance
        user = user_service.read_user_by_id(current_user.id)
        # price to pay
        price_to_pay = (end_date - start_date).days * car.price_per_day
        if user.balance <= price_to_pay:
            flash("Balance too low! You can retrieve it", category="danger")
            # redirect to your retrieving page
            return redirect(url_for("public.edit_balance"))
        if not orders:
            order_service.create_order(
                user_id=current_user.id,
                car_id=car_id,
                start_date=change_time(start_date),
                end_date=change_time(end_date),
                price=price_to_pay,
            )
            user_service.update_user_balance(user.id, (user.balance - price_to_pay))
            admin_service.update_balance(price_to_pay)
            flash("The order was created!", category="success")
            # redirect to your orders page
            return redirect(url_for("public.show_user_orders"))
        flash(f"These dates are busy. Choose another dates!", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating order: {err_msg}", category="danger")
    return render_template("order.html", car=car, form=form)


@public_blueprint.route("/order/delete/<order_id>", methods=["GET", "POST"])
@login_required
def delete_order(order_id):
    """
    Function working on deleting order made by current user
    :param order_id: id of order, user want to delete
    :return: redirects to the template of the orders page
    """
    admin = False
    try:
        order_service.delete_order(order_id)
        return redirect(url_for("public.show_user_orders", admin=admin))
    except:
        flash(f"Failed to delete order with id={order_id}", category="danger")
        return redirect(url_for("public.show_user_orders", admin=admin))
