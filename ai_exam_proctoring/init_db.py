"""
Database Initialization Script
"""

from app import create_app
from database.db import db
from database.models import User, Exam, Question, StudentExam
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json


def initialize_database():
    app = create_app()

    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

        # Admin user
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / admin123")

        # Staff user
        if not User.query.filter_by(username="staff").first():
            staff = User(username="staff", password=generate_password_hash("staff123"), role="staff")
            db.session.add(staff)
            db.session.commit()
            print("Staff user created: staff / staff123")

        # Student user
        if not User.query.filter_by(username="student").first():
            student = User(username="student", password=generate_password_hash("student123"), role="student")
            db.session.add(student)
            db.session.commit()
            print("Student user created: student / student123")

        # Demo exam
        if not Exam.query.filter_by(title="Demo Exam").first():
            staff_user = User.query.filter_by(username="staff").first()
            now = datetime.utcnow()
            exam = Exam(
                title="Demo Exam",
                description="A sample exam covering AI and programming basics.",
                duration_minutes=60,
                max_warnings=3,
                scheduled_start=now - timedelta(minutes=5),
                scheduled_end=now + timedelta(hours=2),
                created_by=staff_user.id
            )
            db.session.add(exam)
            db.session.commit()

            # Add 5 questions
            questions = [
                Question(
                    exam_id=exam.id,
                    text="What does AI stand for?",
                    question_type="mcq",
                    options=json.dumps(["Artificial Intelligence", "Automated Interface", "Advanced Integration", "Analog Input"]),
                    correct_answer="Artificial Intelligence",
                    points=10
                ),
                Question(
                    exam_id=exam.id,
                    text="Which of the following is a supervised learning algorithm?",
                    question_type="mcq",
                    options=json.dumps(["K-Means Clustering", "Linear Regression", "DBSCAN", "PCA"]),
                    correct_answer="Linear Regression",
                    points=10
                ),
                Question(
                    exam_id=exam.id,
                    text="What is the purpose of a neural network activation function?",
                    question_type="mcq",
                    options=json.dumps(["To initialise weights", "To introduce non-linearity", "To normalise input data", "To compute loss"]),
                    correct_answer="To introduce non-linearity",
                    points=10
                ),
                Question(
                    exam_id=exam.id,
                    text="Explain the difference between overfitting and underfitting in machine learning.",
                    question_type="text",
                    options=None,
                    correct_answer=None,
                    points=20
                ),
                Question(
                    exam_id=exam.id,
                    text="Describe two real-world applications of computer vision.",
                    question_type="text",
                    options=None,
                    correct_answer=None,
                    points=20
                ),
            ]
            for q in questions:
                db.session.add(q)
            db.session.commit()

            # Assign demo student to the exam
            student_user = User.query.filter_by(username="student").first()
            student_exam = StudentExam(
                student_id=student_user.id,
                exam_id=exam.id,
                status="upcoming"
            )
            db.session.add(student_exam)
            db.session.commit()

            print("Demo exam created with 5 questions and student assigned.")


if __name__ == "__main__":
    initialize_database()