"""
Exam Routes
-----------

This module handles everything related to the exam interface.

Responsibilities:
1. Start an exam session
2. Render the exam page
3. Ensure only authenticated users access the exam
"""

# Flask utilities
from flask import Blueprint, render_template, redirect, url_for

# Flask login utilities
from flask_login import login_required, current_user

# Database imports
from database.db import db
from database.models import ExamSession


# Create Blueprint for exam routes
exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/exam")
@login_required
def start_exam():
    """
    Start the exam for the logged-in student.

    Steps:
    1. Create a new exam session
    2. Store it in the database
    3. Load the exam page
    """

    # Create a new exam session linked to the logged-in user
    session = ExamSession(user_id=current_user.id)

    # Add session to database
    db.session.add(session)

    # Save changes
    db.session.commit()

    # Render exam page
    return render_template("exam.html", session_id=session.id)