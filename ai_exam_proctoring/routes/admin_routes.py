"""
Admin Routes
"""

import json
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from database.db import db
from database.models import CheatingLog, ExamSession, User, Exam, Question, StudentExam

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    logs = CheatingLog.query.order_by(CheatingLog.timestamp.desc()).all()
    sessions = ExamSession.query.all()
    users = User.query.all()
    exams = Exam.query.all()

    return render_template(
        "dashboard.html",
        logs=logs,
        sessions=sessions,
        users=users,
        exams=exams
    )


@admin_bp.route("/admin/exam/<int:exam_id>/settings", methods=["POST"])
@login_required
def update_exam_settings(exam_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    exam = Exam.query.get_or_404(exam_id)
    exam.max_warnings = int(request.form.get("max_warnings", exam.max_warnings))
    exam.duration_minutes = int(request.form.get("duration_minutes", exam.duration_minutes))
    db.session.commit()
    flash(f"Exam '{exam.title}' settings updated.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/question/<int:question_id>/points", methods=["POST"])
@login_required
def update_question_points(question_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    question = Question.query.get_or_404(question_id)
    question.points = int(request.form.get("points", question.points))
    db.session.commit()
    flash("Question points updated.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/exam/schedule", methods=["POST"])
@login_required
def schedule_exam():
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    title = request.form.get("title", "").strip()
    duration_minutes = int(request.form.get("duration_minutes", 60))
    max_warnings = int(request.form.get("max_warnings", 3))
    start_str = request.form.get("scheduled_start", "")
    end_str = request.form.get("scheduled_end", "")

    if not title:
        flash("Exam title required.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    scheduled_start = None
    scheduled_end = None
    try:
        if start_str:
            scheduled_start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
        if end_str:
            scheduled_end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        flash("Invalid date format.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    exam = Exam(
        title=title,
        duration_minutes=duration_minutes,
        max_warnings=max_warnings,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        created_by=current_user.id
    )
    db.session.add(exam)
    db.session.commit()

    # Assign all students
    students = User.query.filter_by(role="student").all()
    for s in students:
        se = StudentExam(student_id=s.id, exam_id=exam.id, status="upcoming")
        db.session.add(se)
    db.session.commit()

    flash(f"Exam '{title}' scheduled and all students assigned.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/exam/<int:exam_id>/assign_students", methods=["POST"])
@login_required
def assign_students(exam_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    exam = Exam.query.get_or_404(exam_id)
    students = User.query.filter_by(role="student").all()
    count = 0
    for s in students:
        existing = StudentExam.query.filter_by(student_id=s.id, exam_id=exam_id).first()
        if not existing:
            se = StudentExam(student_id=s.id, exam_id=exam_id, status="upcoming")
            db.session.add(se)
            count += 1
    db.session.commit()
    flash(f"{count} student(s) assigned to '{exam.title}'.", "success")
    return redirect(url_for("admin.admin_dashboard"))