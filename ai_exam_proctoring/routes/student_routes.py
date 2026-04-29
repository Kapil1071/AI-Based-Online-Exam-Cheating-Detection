"""
Student Routes
--------------

Student dashboard showing:
- Upcoming exams
- Active exams
- Finished exams (with score)
- Absent exams
"""

from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from database.db import db
from database.models import Exam, ExamSession, ExamResult

student_bp = Blueprint("student", __name__)


@student_bp.route("/student/dashboard")
@login_required
def student_dashboard():
    if current_user.role != "student":
        if current_user.role == "admin":
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for("staff.staff_dashboard"))

    all_exams = Exam.query.order_by(Exam.scheduled_at).all()

    upcoming = []
    active = []
    finished_exams = []
    absent = []

    for exam in all_exams:
        status = exam.status
        # Find existing session for this student & exam
        session = (
            ExamSession.query
            .filter_by(user_id=current_user.id, exam_id=exam.id)
            .order_by(ExamSession.start_time.desc())
            .first()
        )
        result = session.result if session else None

        if status == "upcoming":
            upcoming.append({"exam": exam, "session": session})
        elif status == "active":
            active.append({"exam": exam, "session": session})
        elif status == "finished":
            if session and result:
                finished_exams.append({"exam": exam, "session": session, "result": result})
            else:
                absent.append({"exam": exam})

    return render_template(
        "student_dashboard.html",
        upcoming=upcoming,
        active=active,
        finished=finished_exams,
        absent=absent,
    )
