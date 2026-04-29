"""
Database Models
---------------

Defines all database tables using SQLAlchemy ORM.

Tables:
1. User
2. Exam
3. Question
4. ExamSession
5. ExamAnswer
6. ExamResult
7. CheatingLog
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
    - staff
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
# EXAM MODEL
# ============================

class Exam(db.Model):
    """
    Exam Table

    Represents a scheduled exam created by staff/admin.
    """

    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=True)

    # Duration in minutes
    duration_minutes = db.Column(db.Integer, default=60)

    # Maximum warnings before exam is terminated
    max_warnings = db.Column(db.Integer, default=3)

    # Scheduled start time
    scheduled_at = db.Column(db.DateTime, nullable=True)

    # Created by (staff/admin user id)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship("Question", backref="exam", lazy=True, cascade="all, delete-orphan")
    sessions = db.relationship("ExamSession", backref="exam", lazy=True)

    def __repr__(self):
        return f"<Exam {self.title}>"

    @property
    def status(self):
        """Return current status: upcoming / active / finished."""
        now = datetime.utcnow()
        if self.scheduled_at is None:
            return "active"
        from datetime import timedelta
        end_time = self.scheduled_at + timedelta(minutes=self.duration_minutes)
        if now < self.scheduled_at:
            return "upcoming"
        elif now <= end_time:
            return "active"
        else:
            return "finished"

    @property
    def total_points(self):
        return sum(q.points for q in self.questions)


# ============================
# QUESTION MODEL
# ============================

class Question(db.Model):
    """
    Question Table

    Stores exam questions added by staff/admin.
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id"),
        nullable=False
    )

    text = db.Column(db.Text, nullable=False)

    # Multiple choice options (nullable for open-ended)
    option_a = db.Column(db.String(300), nullable=True)
    option_b = db.Column(db.String(300), nullable=True)
    option_c = db.Column(db.String(300), nullable=True)
    option_d = db.Column(db.String(300), nullable=True)

    # Correct answer: 'A', 'B', 'C', 'D', or None for open-ended
    correct_answer = db.Column(db.String(1), nullable=True)

    # Points awarded for correct answer
    points = db.Column(db.Integer, default=10)

    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Question {self.id} - Exam {self.exam_id}>"

    @property
    def is_mcq(self):
        return self.option_a is not None


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

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id"),
        nullable=True
    )

    start_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    end_time = db.Column(
        db.DateTime,
        nullable=True
    )

    warning_count = db.Column(db.Integer, default=0)

    terminated = db.Column(db.Boolean, default=False)

    # Relationship: One session → many cheating logs
    cheating_logs = db.relationship(
        "CheatingLog",
        backref="session",
        lazy=True
    )

    answers = db.relationship(
        "ExamAnswer",
        backref="session",
        lazy=True,
        cascade="all, delete-orphan"
    )

    result = db.relationship(
        "ExamResult",
        backref="session",
        uselist=False,
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ExamSession {self.id} - User {self.user_id}>"


# ============================
# EXAM ANSWER MODEL
# ============================

class ExamAnswer(db.Model):
    """
    Stores each student answer per question per session.
    """

    __tablename__ = "exam_answers"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("exam_sessions.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False
    )

    # For MCQ: 'A'/'B'/'C'/'D'; for open-ended: free text
    answer_text = db.Column(db.Text, nullable=True)

    is_correct = db.Column(db.Boolean, nullable=True)

    points_awarded = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<ExamAnswer session={self.session_id} q={self.question_id}>"


# ============================
# EXAM RESULT MODEL
# ============================

class ExamResult(db.Model):
    """
    Stores the final score for a completed exam session.
    """

    __tablename__ = "exam_results"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("exam_sessions.id"),
        nullable=False,
        unique=True
    )

    score = db.Column(db.Integer, default=0)

    total_points = db.Column(db.Integer, default=0)

    status = db.Column(db.String(20), default="completed")  # completed / terminated

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ExamResult session={self.session_id} score={self.score}/{self.total_points}>"


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