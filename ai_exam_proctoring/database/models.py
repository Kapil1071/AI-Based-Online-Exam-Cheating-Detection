"""
Database Models
---------------

Defines all database tables using SQLAlchemy ORM.

Tables:
1. User
2. ExamSession
3. CheatingLog
"""

from datetime import datetime
from flask_login import UserMixin
from database.db import db


# ============================
# USER MODEL
# ============================

class User(UserMixin, db.Model):
    """
    User Table

    Stores all system users:
    - students
    - administrators
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="student"
    )

    # Relationship: One user → many exam sessions
    exam_sessions = db.relationship(
        "ExamSession",
        backref="user",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"


# ============================
# EXAM SESSION MODEL
# ============================

class ExamSession(db.Model):
    """
    Exam Session Table

    Stores information about an active exam attempt.
    """

    __tablename__ = "exam_sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    start_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    end_time = db.Column(
        db.DateTime,
        nullable=True
    )

    # Relationship: One session → many cheating logs
    cheating_logs = db.relationship(
        "CheatingLog",
        backref="session",
        lazy=True
    )

    def __repr__(self):
        return f"<ExamSession {self.id} - User {self.user_id}>"


# ============================
# CHEATING LOG MODEL
# ============================

class CheatingLog(db.Model):
    """
    Cheating Log Table

    Stores suspicious activities detected during exam.
    """

    __tablename__ = "cheating_logs"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("exam_sessions.id"),
        nullable=False
    )

    event_type = db.Column(
        db.String(100),
        nullable=False
    )

    image_path = db.Column(
        db.String(200),
        nullable=True
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<CheatingLog {self.event_type} - Session {self.session_id}>"