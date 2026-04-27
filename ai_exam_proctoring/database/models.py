"""
Database Models
---------------

Defines all database tables using SQLAlchemy ORM.
"""

from datetime import datetime
from flask_login import UserMixin
from database.db import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="student")

    exam_sessions = db.relationship("ExamSession", backref="user", lazy=True)
    student_exams = db.relationship("StudentExam", backref="student", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class ExamSession(db.Model):
    __tablename__ = "exam_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=True)

    cheating_logs = db.relationship("CheatingLog", backref="session", lazy=True)

    def __repr__(self):
        return f"<ExamSession {self.id} - User {self.user_id}>"


class CheatingLog(db.Model):
    __tablename__ = "cheating_logs"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CheatingLog {self.event_type} - Session {self.session_id}>"


class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    duration_minutes = db.Column(db.Integer, default=60)
    max_warnings = db.Column(db.Integer, default=3)
    scheduled_start = db.Column(db.DateTime, nullable=True)
    scheduled_end = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    questions = db.relationship("Question", backref="exam", lazy=True, cascade="all, delete-orphan")
    student_exams = db.relationship("StudentExam", backref="exam", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Exam {self.title}>"


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default="text")  # "text" or "mcq"
    options = db.Column(db.Text, nullable=True)  # JSON string for MCQ options
    correct_answer = db.Column(db.Text, nullable=True)
    points = db.Column(db.Integer, default=10)

    def __repr__(self):
        return f"<Question {self.id}>"


class StudentExam(db.Model):
    __tablename__ = "student_exams"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    status = db.Column(db.String(20), default="upcoming")  # upcoming, active, finished, absent
    score = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    answers = db.Column(db.Text, nullable=True)  # JSON string of answers
    session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), nullable=True)

    def __repr__(self):
        return f"<StudentExam student={self.student_id} exam={self.exam_id}>"