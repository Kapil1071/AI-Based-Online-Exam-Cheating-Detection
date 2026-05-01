"""
Admin Exam Management Routes
-----------------------------

This module provides routes for admin to create and manage exams.

Admin exam management capabilities:
1. Create new exams
2. Add questions to exams
3. Edit exam details
4. Delete exams and questions
5. View all exams and questions
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from database.db import db
from database.models import Exam, Question, User

admin_exam_bp = Blueprint("admin_exam", __name__)

def _require_admin():
    """Check if current user is admin."""
    if current_user.role != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))
    return None


# ── Create New Exam ────────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams/create", methods=["GET", "POST"])
@login_required
def create_exam():
    """
    Create a new exam.
    """
    denied = _require_admin()
    if denied:
        return denied

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        duration_minutes = int(request.form.get("duration_minutes", 60))
        max_warnings = int(request.form.get("max_warnings", 3))
        scheduled_at_str = request.form.get("scheduled_at", "").strip()

        # Validation
        if not title:
            flash("Exam title is required.", "danger")
            return render_template("admin_create_exam.html")

        if duration_minutes < 1:
            flash("Duration must be at least 1 minute.", "danger")
            return render_template("admin_create_exam.html")

        if max_warnings < 1:
            flash("Maximum warnings must be at least 1.", "danger")
            return render_template("admin_create_exam.html")

        # Parse scheduled time if provided
        scheduled_at = None
        if scheduled_at_str:
            try:
                scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date/time format.", "danger")
                return render_template("admin_create_exam.html")

        # Create new exam
        exam = Exam(
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            max_warnings=max_warnings,
            scheduled_at=scheduled_at,
            created_by=current_user.id
        )

        db.session.add(exam)
        db.session.commit()

        flash(f"Exam '{title}' created successfully!", "success")
        return redirect(url_for("admin_exam.add_questions", exam_id=exam.id))

    return render_template("admin_create_exam.html")


# ── Add Questions to Exam ──────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams/<int:exam_id>/add-questions", methods=["GET", "POST"])
@login_required
def add_questions(exam_id):
    """
    Add questions to an exam.
    """
    denied = _require_admin()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        question_text = request.form.get("question_text", "").strip()
        question_type = request.form.get("question_type", "mcq")  # mcq or open
        points = int(request.form.get("points", 10))

        if not question_text:
            flash("Question text is required.", "danger")
            return render_template("admin_add_questions.html", exam=exam, questions=exam.questions)

        if points < 1:
            flash("Points must be at least 1.", "danger")
            return render_template("admin_add_questions.html", exam=exam, questions=exam.questions)

        # Create question
        if question_type == "mcq":
            option_a = request.form.get("option_a", "").strip()
            option_b = request.form.get("option_b", "").strip()
            option_c = request.form.get("option_c", "").strip()
            option_d = request.form.get("option_d", "").strip()
            correct_answer = request.form.get("correct_answer", "").strip()

            if not all([option_a, option_b, option_c, option_d, correct_answer]):
                flash("All options and correct answer are required for MCQ.", "danger")
                return render_template("admin_add_questions.html", exam=exam, questions=exam.questions)

            question = Question(
                exam_id=exam_id,
                text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                points=points,
                order=len(exam.questions) + 1
            )
        else:
            # Open-ended question
            question = Question(
                exam_id=exam_id,
                text=question_text,
                points=points,
                order=len(exam.questions) + 1
            )

        db.session.add(question)
        db.session.commit()

        flash("Question added successfully!", "success")
        return redirect(url_for("admin_exam.add_questions", exam_id=exam_id))

    return render_template("admin_add_questions.html", exam=exam, questions=exam.questions)


# ── Edit Exam ──────────────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams/<int:exam_id>/edit", methods=["GET", "POST"])
@login_required
def edit_exam(exam_id):
    """
    Edit exam details.
    """
    denied = _require_admin()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        exam.title = request.form.get("title", exam.title).strip()
        exam.description = request.form.get("description", exam.description).strip()
        exam.duration_minutes = int(request.form.get("duration_minutes", exam.duration_minutes))
        exam.max_warnings = int(request.form.get("max_warnings", exam.max_warnings))

        scheduled_at_str = request.form.get("scheduled_at", "").strip()
        if scheduled_at_str:
            try:
                exam.scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date/time format.", "danger")
                return render_template("admin_edit_exam.html", exam=exam)
        else:
            exam.scheduled_at = None

        db.session.commit()
        flash("Exam updated successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin_edit_exam.html", exam=exam)


# ── Delete Question ────────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/questions/<int:question_id>/delete", methods=["POST"])
@login_required
def delete_question(question_id):
    """
    Delete a question from an exam.
    """
    denied = _require_admin()
    if denied:
        return denied

    question = Question.query.get_or_404(question_id)
    exam_id = question.exam_id

    db.session.delete(question)
    db.session.commit()

    flash("Question deleted successfully!", "success")
    return redirect(url_for("admin_exam.add_questions", exam_id=exam_id))


# ── Delete Exam ────────────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams/<int:exam_id>/delete", methods=["POST"])
@login_required
def delete_exam(exam_id):
    """
    Delete an entire exam and all its questions.
    """
    denied = _require_admin()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)
    exam_title = exam.title

    db.session.delete(exam)
    db.session.commit()

    flash(f"Exam '{exam_title}' and all its questions have been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# ── List All Exams ────────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams")
@login_required
def list_exams():
    """
    List all exams created.
    """
    denied = _require_admin()
    if denied:
        return denied

    exams = Exam.query.order_by(Exam.created_at.desc()).all()
    return render_template("admin_list_exams.html", exams=exams)


# ── Reorder Questions ──────────────────────────────────────────────────────
@admin_exam_bp.route("/admin/exams/<int:exam_id>/reorder-questions", methods=["POST"])
@login_required
def reorder_questions(exam_id):
    """
    Reorder questions via AJAX (drag and drop).
    """
    denied = _require_admin()
    if denied:
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    question_ids = data.get("question_ids", [])

    for index, question_id in enumerate(question_ids, 1):
        question = Question.query.get(question_id)
        if question:
            question.order = index

    db.session.commit()
    return jsonify({"status": "success", "message": "Questions reordered successfully"})