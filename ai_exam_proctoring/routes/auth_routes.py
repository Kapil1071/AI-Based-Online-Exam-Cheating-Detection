"""
Authentication Routes
---------------------

This module handles:

1. User login
2. User logout
3. Session management

Flask-Login is used to manage user sessions securely.
"""

# Import Flask utilities
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Import database and models
from database.db import db
from database.models import User

# Import password hashing utilities
from werkzeug.security import check_password_hash

# Import Flask-Login utilities
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


# Create Blueprint
# Blueprints allow modular route organization
auth_bp = Blueprint("auth", __name__)


# Initialize Login Manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login uses this function to load the user object
    from the database using the stored session ID.
    """

    return User.query.get(int(user_id))


# Login Page Route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.

    GET  → show login page
    POST → authenticate user
    """

    # If user already logged in redirect to exam page
    if current_user.is_authenticated:
        return redirect(url_for("exam.start_exam"))

    # Handle login form submission
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Find user in database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            # Log the user in
            login_user(user)

            flash("Login successful", "success")

            return redirect(url_for("exam.start_exam"))

        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


# Logout Route
@auth_bp.route("/logout")
@login_required
def logout():
    """
    Logs the user out and clears session.
    """

    logout_user()

    flash("You have been logged out", "info")

    return redirect(url_for("auth.login"))