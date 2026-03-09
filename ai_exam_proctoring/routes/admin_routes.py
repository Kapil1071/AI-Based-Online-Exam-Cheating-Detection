"""
Admin Routes
------------

This module provides routes for the administrator dashboard.

Admin capabilities:
1. View cheating logs
2. View exam sessions
3. Monitor student behavior
"""

# Flask utilities
from flask import Blueprint, render_template, redirect, url_for

# Login utilities
from flask_login import login_required, current_user

# Database imports
from database.models import CheatingLog, ExamSession, User


# Create blueprint
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """
    Admin dashboard page.

    Only users with role='admin' should access this page.
    """

    # Check if user is admin
    if current_user.role != "admin":
        return redirect(url_for("exam.start_exam"))

    # Fetch all cheating logs
    logs = CheatingLog.query.order_by(CheatingLog.timestamp.desc()).all()

    # Fetch all exam sessions
    sessions = ExamSession.query.all()

    # Fetch users
    users = User.query.all()

    return render_template(
        "dashboard.html",
        logs=logs,
        sessions=sessions,
        users=users
    )