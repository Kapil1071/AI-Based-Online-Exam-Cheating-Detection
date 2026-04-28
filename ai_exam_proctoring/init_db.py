"""
Database Initialization Script
------------------------------

This script creates the database tables defined in SQLAlchemy models.

It also optionally creates default users and demo exam data so the system
can be accessed immediately after setup.

Run this file once before starting the application.

Command:
    python init_db.py
"""

from datetime import datetime, timedelta

# Import Flask app factory
from app import create_app

# Import database instance
from database.db import db

# Import models
from database.models import User, Exam, Question

# Import password hashing utility
from werkzeug.security import generate_password_hash


def initialize_database():
    """
    Create database tables and insert default users and demo exam data.
    """

    app = create_app()

    with app.app_context():

        db.create_all()
        print("Database tables created successfully.")

        # ── Admin ──────────────────────────────────────────────
        if not User.query.filter_by(username="admin").first():
            db.session.add(User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            ))
            print("Created admin  →  admin / admin123")

        # ── Staff ──────────────────────────────────────────────
        if not User.query.filter_by(username="staff").first():
            db.session.add(User(
                username="staff",
                password=generate_password_hash("staff123"),
                role="staff"
            ))
            print("Created staff  →  staff / staff123")

        # ── Student ────────────────────────────────────────────
        if not User.query.filter_by(username="student").first():
            db.session.add(User(
                username="student",
                password=generate_password_hash("student123"),
                role="student"
            ))
            print("Created student  →  student / student123")

        db.session.commit()

        # ── Demo Exam ──────────────────────────────────────────
        if not Exam.query.filter_by(title="Artificial Intelligence Basics").first():
            staff_user = User.query.filter_by(username="staff").first()
            exam = Exam(
                title="Artificial Intelligence Basics",
                description="A foundational exam covering AI and machine learning concepts.",
                duration_minutes=60,
                max_warnings=3,
                scheduled_at=datetime.utcnow() - timedelta(minutes=5),  # active now
                created_by=staff_user.id if staff_user else None,
            )
            db.session.add(exam)
            db.session.flush()

            questions = [
                Question(
                    exam_id=exam.id,
                    text="What does AI stand for?",
                    option_a="Automated Intelligence",
                    option_b="Artificial Intelligence",
                    option_c="Augmented Integration",
                    option_d="Advanced Informatics",
                    correct_answer="B",
                    points=10,
                    order=1,
                ),
                Question(
                    exam_id=exam.id,
                    text="Which of the following is a supervised learning algorithm?",
                    option_a="K-Means Clustering",
                    option_b="Principal Component Analysis",
                    option_c="Linear Regression",
                    option_d="DBSCAN",
                    correct_answer="C",
                    points=10,
                    order=2,
                ),
                Question(
                    exam_id=exam.id,
                    text="What is a neural network inspired by?",
                    option_a="The human digestive system",
                    option_b="The human brain",
                    option_c="DNA replication",
                    option_d="Quantum mechanics",
                    correct_answer="B",
                    points=10,
                    order=3,
                ),
                Question(
                    exam_id=exam.id,
                    text="Which Python library is commonly used for deep learning?",
                    option_a="NumPy",
                    option_b="Pandas",
                    option_c="TensorFlow",
                    option_d="Matplotlib",
                    correct_answer="C",
                    points=10,
                    order=4,
                ),
                Question(
                    exam_id=exam.id,
                    text="What does 'overfitting' mean in machine learning?",
                    option_a="The model performs poorly on training data",
                    option_b="The model performs well on training data but poorly on new data",
                    option_c="The model is too simple",
                    option_d="The model cannot be trained",
                    correct_answer="B",
                    points=10,
                    order=5,
                ),
            ]
            db.session.add_all(questions)
            db.session.commit()
            print(f"Created demo exam '{exam.title}' with {len(questions)} questions.")
        else:
            print("Demo exam already exists.")


if __name__ == "__main__":

    initialize_database()