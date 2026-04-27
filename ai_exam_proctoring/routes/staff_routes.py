"""
Staff Routes
------------
Routes for staff members to manage exams and questions.
"""

import json
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from database.db import db
from database.models import Exam, Question, StudentExam, User

staff_bp = Blueprint("staff", __name__)


def staff_required(f):
    """Decorator to require staff or admin role."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.role not in ("staff", "admin"):
            flash("Access denied. Staff only.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@staff_bp.route("/staff/dashboard")
@login_required
@staff_required
def staff_dashboard():
    exams = Exam.query.filter_by(created_by=current_user.id).all()
    return render_template("staff_dashboard.html", exams=exams)


@staff_bp.route("/staff/exam/create", methods=["POST"])
@login_required
@staff_required
def create_exam():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    duration_minutes = int(request.form.get("duration_minutes", 60))
    max_warnings = int(request.form.get("max_warnings", 3))
    scheduled_start_str = request.form.get("scheduled_start", "")
    scheduled_end_str = request.form.get("scheduled_end", "")

    if not title:
        flash("Exam title is required.", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    scheduled_start = None
    scheduled_end = None
    try:
        if scheduled_start_str:
            scheduled_start = datetime.strptime(scheduled_start_str, "%Y-%m-%dT%H:%M")
        if scheduled_end_str:
            scheduled_end = datetime.strptime(scheduled_end_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        flash("Invalid date format.", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    exam = Exam(
        title=title,
        description=description,
        duration_minutes=duration_minutes,
        max_warnings=max_warnings,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        created_by=current_user.id
    )
    db.session.add(exam)
    db.session.commit()
    flash(f"Exam '{title}' created successfully.", "success")
    return redirect(url_for("staff.staff_dashboard"))


@staff_bp.route("/staff/exam/<int:exam_id>/questions")
@login_required
@staff_required
def manage_questions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    return render_template("staff_questions.html", exam=exam, questions=questions)


@staff_bp.route("/staff/exam/<int:exam_id>/questions/add", methods=["POST"])
@login_required
@staff_required
def add_question(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    text = request.form.get("text", "").strip()
    question_type = request.form.get("question_type", "text")
    options_raw = request.form.get("options", "").strip()
    correct_answer = request.form.get("correct_answer", "").strip()
    points = int(request.form.get("points", 10))

    if not text:
        flash("Question text is required.", "danger")
        return redirect(url_for("staff.manage_questions", exam_id=exam_id))

    options_json = None
    if question_type == "mcq" and options_raw:
        opts = [o.strip() for o in options_raw.split("\n") if o.strip()]
        options_json = json.dumps(opts)

    question = Question(
        exam_id=exam_id,
        text=text,
        question_type=question_type,
        options=options_json,
        correct_answer=correct_answer or None,
        points=points
    )
    db.session.add(question)
    db.session.commit()
    flash("Question added.", "success")
    return redirect(url_for("staff.manage_questions", exam_id=exam_id))


@staff_bp.route("/staff/question/<int:question_id>/delete", methods=["POST"])
@login_required
@staff_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    exam_id = question.exam_id
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted.", "success")
    return redirect(url_for("staff.manage_questions", exam_id=exam_id))


@staff_bp.route("/staff/exam/<int:exam_id>/edit", methods=["GET", "POST"])
@login_required
@staff_required
def edit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        exam.title = request.form.get("title", exam.title).strip()
        exam.description = request.form.get("description", exam.description).strip()
        exam.duration_minutes = int(request.form.get("duration_minutes", exam.duration_minutes))
        exam.max_warnings = int(request.form.get("max_warnings", exam.max_warnings))

        start_str = request.form.get("scheduled_start", "")
        end_str = request.form.get("scheduled_end", "")
        try:
            if start_str:
                exam.scheduled_start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
            if end_str:
                exam.scheduled_end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("staff.edit_exam", exam_id=exam_id))

        db.session.commit()
        flash("Exam updated.", "success")
        return redirect(url_for("staff.staff_dashboard"))

    return render_template("staff_edit_exam.html", exam=exam)
