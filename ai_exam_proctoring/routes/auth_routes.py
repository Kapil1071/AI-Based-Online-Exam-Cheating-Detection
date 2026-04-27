"""
Authentication Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import db
from database.models import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.role)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful", "success")
            return _redirect_by_role(user.role)
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


def _redirect_by_role(role):
    if role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif role == "staff":
        return redirect(url_for("staff.staff_dashboard"))
    else:
        return redirect(url_for("exam.student_dashboard"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))