from flask import render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from wtforms import ValidationError

from log import logger

from . import public_blueprint, admin_blueprint
from .. import bcrypt
from ..func import prepare_to_service
from ..service import user_service, passport_service
from ..form import UserForm, BalanceForm, PassportForm


@public_blueprint.route("/profile", methods=["GET"])
@login_required
def profile_page():
    """
    Render the profile page template
    """
    return render_template("profile.html")


@public_blueprint.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    """
    Function working on updating current user
    :return: redirects to  the template of the profile_page
    """
    edit_profile = True
    form = UserForm()
    if form.validate_on_submit():
        data_to_validate = prepare_to_service(form.data)
        try:
            if data_to_validate["password"]:
                data_to_validate["password"] = bcrypt.generate_password_hash(
                    data_to_validate["password"]
                )
        except:
            logger.error(f"Failed to hash password!")
        user_service.update_user(current_user.id, data_to_validate)
        flash(
            "You have successfully edited your personal info.",
            category="success",
        )
        # redirect to the profile page
        return redirect(url_for("public.profile_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    return render_template("edit_profile.html", form=form, edit_profile=edit_profile)


@public_blueprint.route("/passport/edit", methods=["GET", "POST"])
@login_required
def edit_passport():
    """
    Function working on updating current user`s passport data
    :return: redirects to  the template of the profile_page
    """
    edit_profile = False
    form = PassportForm()
    if form.validate_on_submit():
        data_to_validate = prepare_to_service(form.data)
        try:
            passport_service.update_passport(current_user.passport_id, data_to_validate)
            flash(
                "You have successfully edited your passport info.", category="success"
            )
            # redirect to the profile page
            return redirect(url_for("public.profile_page"))
        except ValidationError as err:
            flash(f"{err.messages}", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with updating passport data: {err_msg}", category="danger")
    return render_template("edit_profile.html", form=form, edit_profile=edit_profile)


@public_blueprint.route("/balance", methods=["GET", "POST"])
@login_required
def edit_balance():
    """
    Function working on retrieving current user`s balance
    :return: redirects to  the template of the profile_page
    """
    form = BalanceForm()
    if form.validate_on_submit():
        user_service.update_user_balance(current_user.id, form.balance.data)
        flash("You have successfully edited your personal info.", category="success")
        # redirect to the profile page
        return redirect(url_for("public.profile_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating account: {err_msg}", category="danger")
    return render_template("edit_balance.html", form=form)


@public_blueprint.route("/profile/delete", methods=["GET", "POST"])
@login_required
def delete_user():
    """
    Function working on deleting current user`s account
    :return: the template of the register page
    """
    try:
        user_service.delete_user(current_user.id)
        return redirect(url_for("register.html"))
    except:
        logger.error(f"Failed delete user!")
        return render_template("profile.html")


@admin_blueprint.route("/users", methods=["GET", "POST"])
def show_all_users():
    """
    Function working on reading all users (uses user_service)
    :return: the template of the users page
    """
    admin = True
    try:
        users = user_service.read_all_users()
        return render_template("users.html", admin=admin, users=users)
    except:
        return render_template("cars.html")
