"""
Database Models
---------------

This file defines all database tables used in the system.

Using SQLAlchemy ORM, each Python class represents a database table.
Each class attribute represents a column in that table.

Tables in this system:

1. User
2. ExamSession
3. CheatingLog
"""

from datetime import datetime

# Import database instance
from database.db import db



class User(db.Model):
    """
    User Table

    Stores all system users:
    - students
    - administrators
    """

    # Primary key (unique id for each user)
    id = db.Column(db.Integer, primary_key=True)

    # Username used for login
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Password (hashed later)
    password = db.Column(db.String(200), nullable=False)

    # User role
    # student or admin
    role = db.Column(db.String(20), default="student")



class ExamSession(db.Model):
    """
    Exam Session Table

    Stores information about an active exam attempt.
    """

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Which student started the exam
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Exam start time
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    # Exam end time
    end_time = db.Column(db.DateTime, nullable=True)



class CheatingLog(db.Model):
    """
    Cheating Log Table

    Stores suspicious activities detected during exam.
    """

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Which exam session triggered the event
    session_id = db.Column(db.Integer, db.ForeignKey("exam_session.id"))

    # Type of cheating event
    event_type = db.Column(db.String(100))

    # Optional evidence image path
    image_path = db.Column(db.String(200))

    # Time of event
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)