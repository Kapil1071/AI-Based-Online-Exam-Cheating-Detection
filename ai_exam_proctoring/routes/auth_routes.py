"""
Authentication Routes
---------------------

This module handles:

1. User login  (Student / Staff / Admin)
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
auth_bp = Blueprint("auth", __name__)

# Initialize Login Manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def _redirect_after_login(user):
    """Return the appropriate redirect response based on user role."""
    if user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif user.role == "staff":
        return redirect(url_for("staff.staff_dashboard"))
    else:
        return redirect(url_for("student.student_dashboard"))


# ── Login ──────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    GET  → show login page with Student / Staff role tabs
    POST → authenticate user and redirect by role
    """

    if current_user.is_authenticated:
        return _redirect_after_login(current_user)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role_hint = request.form.get("role", "student")  # 'student' or 'staff'

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Staff tab should only allow staff/admin accounts
            if role_hint == "staff" and user.role not in ("staff", "admin"):
                flash("This account does not have staff access.", "danger")
            elif role_hint == "student" and user.role not in ("student",):
                # Admin/staff trying student portal → allow but redirect correctly
                login_user(user)
                flash("Login successful", "success")
                return _redirect_after_login(user)
            else:
                login_user(user)
                flash("Login successful", "success")
                return _redirect_after_login(user)
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


# ── Logout ─────────────────────────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))