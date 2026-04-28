"""
Staff Routes
------------

Staff members can:
1. View / create / edit / delete exams
2. Add / edit / delete questions
3. Customise exam duration and warning limit
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database.db import db
from database.models import Exam, Question

staff_bp = Blueprint("staff", __name__)


def _require_staff():
    """Return an error response if the current user is not staff/admin."""
    if current_user.role not in ("staff", "admin"):
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))
    return None


# ── Staff Dashboard ────────────────────────────────────────────────────────
@staff_bp.route("/staff/dashboard")
@login_required
def staff_dashboard():
    denied = _require_staff()
    if denied:
        return denied

    exams = Exam.query.order_by(Exam.scheduled_at.desc()).all()
    return render_template("staff_dashboard.html", exams=exams)


# ── Create Exam ────────────────────────────────────────────────────────────
@staff_bp.route("/staff/exams/new", methods=["GET", "POST"])
@login_required
def create_exam():
    denied = _require_staff()
    if denied:
        return denied

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        duration = int(request.form.get("duration_minutes", 60))
        max_warnings = int(request.form.get("max_warnings", 3))
        scheduled_at_str = request.form.get("scheduled_at", "").strip()

        if not title:
            flash("Exam title is required.", "danger")
            return render_template("staff_exam_form.html", exam=None)

        scheduled_at = None
        if scheduled_at_str:
            try:
                from datetime import datetime
                scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date/time format.", "danger")
                return render_template("staff_exam_form.html", exam=None)

        exam = Exam(
            title=title,
            description=description,
            duration_minutes=duration,
            max_warnings=max_warnings,
            scheduled_at=scheduled_at,
            created_by=current_user.id,
        )
        db.session.add(exam)
        db.session.commit()
        flash(f"Exam '{title}' created successfully.", "success")
        return redirect(url_for("staff.manage_questions", exam_id=exam.id))

    return render_template("staff_exam_form.html", exam=None)


# ── Edit Exam ──────────────────────────────────────────────────────────────
@staff_bp.route("/staff/exams/<int:exam_id>/edit", methods=["GET", "POST"])
@login_required
def edit_exam(exam_id):
    denied = _require_staff()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        exam.title = request.form.get("title", exam.title).strip()
        exam.description = request.form.get("description", "").strip()
        exam.duration_minutes = int(request.form.get("duration_minutes", exam.duration_minutes))
        exam.max_warnings = int(request.form.get("max_warnings", exam.max_warnings))
        scheduled_at_str = request.form.get("scheduled_at", "").strip()

        if scheduled_at_str:
            try:
                from datetime import datetime
                exam.scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date/time format.", "danger")
                return render_template("staff_exam_form.html", exam=exam)
        else:
            exam.scheduled_at = None

        db.session.commit()
        flash("Exam updated successfully.", "success")
        return redirect(url_for("staff.staff_dashboard"))

    return render_template("staff_exam_form.html", exam=exam)


# ── Delete Exam ────────────────────────────────────────────────────────────
@staff_bp.route("/staff/exams/<int:exam_id>/delete", methods=["POST"])
@login_required
def delete_exam(exam_id):
    denied = _require_staff()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    flash("Exam deleted.", "info")
    return redirect(url_for("staff.staff_dashboard"))


# ── Manage Questions ───────────────────────────────────────────────────────
@staff_bp.route("/staff/exams/<int:exam_id>/questions")
@login_required
def manage_questions(exam_id):
    denied = _require_staff()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).order_by(Question.order).all()
    return render_template("staff_questions.html", exam=exam, questions=questions)


# ── Add Question ───────────────────────────────────────────────────────────
@staff_bp.route("/staff/exams/<int:exam_id>/questions/add", methods=["POST"])
@login_required
def add_question(exam_id):
    denied = _require_staff()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)
    text = request.form.get("text", "").strip()
    if not text:
        flash("Question text is required.", "danger")
        return redirect(url_for("staff.manage_questions", exam_id=exam_id))

    option_a = request.form.get("option_a", "").strip() or None
    option_b = request.form.get("option_b", "").strip() or None
    option_c = request.form.get("option_c", "").strip() or None
    option_d = request.form.get("option_d", "").strip() or None
    correct_answer = request.form.get("correct_answer", "").strip().upper() or None
    points = int(request.form.get("points", 10))
    last_order = db.session.query(db.func.max(Question.order)).filter_by(exam_id=exam_id).scalar() or 0

    q = Question(
        exam_id=exam_id,
        text=text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer,
        points=points,
        order=last_order + 1,
    )
    db.session.add(q)
    db.session.commit()
    flash("Question added.", "success")
    return redirect(url_for("staff.manage_questions", exam_id=exam_id))


# ── Edit Question ──────────────────────────────────────────────────────────
@staff_bp.route("/staff/questions/<int:question_id>/edit", methods=["GET", "POST"])
@login_required
def edit_question(question_id):
    denied = _require_staff()
    if denied:
        return denied

    q = Question.query.get_or_404(question_id)

    if request.method == "POST":
        q.text = request.form.get("text", q.text).strip()
        q.option_a = request.form.get("option_a", "").strip() or None
        q.option_b = request.form.get("option_b", "").strip() or None
        q.option_c = request.form.get("option_c", "").strip() or None
        q.option_d = request.form.get("option_d", "").strip() or None
        q.correct_answer = request.form.get("correct_answer", "").strip().upper() or None
        q.points = int(request.form.get("points", q.points))
        db.session.commit()
        flash("Question updated.", "success")
        return redirect(url_for("staff.manage_questions", exam_id=q.exam_id))

    return render_template("staff_question_edit.html", question=q)


# ── Delete Question ────────────────────────────────────────────────────────
@staff_bp.route("/staff/questions/<int:question_id>/delete", methods=["POST"])
@login_required
def delete_question(question_id):
    denied = _require_staff()
    if denied:
        return denied

    q = Question.query.get_or_404(question_id)
    exam_id = q.exam_id
    db.session.delete(q)
    db.session.commit()
    flash("Question deleted.", "info")
    return redirect(url_for("staff.manage_questions", exam_id=exam_id))
