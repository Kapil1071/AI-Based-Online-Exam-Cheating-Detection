"""
Admin Routes
------------

This module provides routes for the administrator dashboard.

Admin capabilities:
1. View cheating logs and exam sessions
2. Schedule exams (set scheduled_at, duration, max_warnings)
3. View scores / manage users
"""

from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database.db import db
from database.models import CheatingLog, ExamSession, User, Exam, ExamResult


admin_bp = Blueprint("admin", __name__)


def _require_admin():
    if current_user.role != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))
    return None


# ── Admin Dashboard ────────────────────────────────────────────────────────
@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    denied = _require_admin()
    if denied:
        return denied

    logs = CheatingLog.query.order_by(CheatingLog.timestamp.desc()).all()
    sessions = ExamSession.query.all()
    users = User.query.all()
    exams = Exam.query.order_by(Exam.scheduled_at.desc()).all()
    results = ExamResult.query.all()

    return render_template(
        "dashboard.html",
        logs=logs,
        sessions=sessions,
        users=users,
        exams=exams,
        results=results,
    )


# ── Schedule / Edit Exam (admin view) ─────────────────────────────────────
@admin_bp.route("/admin/exams/<int:exam_id>/schedule", methods=["GET", "POST"])
@login_required
def schedule_exam(exam_id):
    denied = _require_admin()
    if denied:
        return denied

    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        scheduled_at_str = request.form.get("scheduled_at", "").strip()
        exam.duration_minutes = int(request.form.get("duration_minutes", exam.duration_minutes))
        exam.max_warnings = int(request.form.get("max_warnings", exam.max_warnings))

        if scheduled_at_str:
            try:
                exam.scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date/time format.", "danger")
                return render_template("admin_schedule_exam.html", exam=exam)
        else:
            exam.scheduled_at = None

        db.session.commit()
        flash("Exam schedule updated.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin_schedule_exam.html", exam=exam)


# ── View Scores ────────────────────────────────────────────────────────────
@admin_bp.route("/admin/scores")
@login_required
def view_scores():
    denied = _require_admin()
    if denied:
        return denied

    results = (
        ExamResult.query
        .join(ExamSession, ExamResult.session_id == ExamSession.id)
        .join(User, ExamSession.user_id == User.id)
        .join(Exam, ExamSession.exam_id == Exam.id)
        .add_columns(User.username, Exam.title, ExamResult.score, ExamResult.total_points,
                     ExamResult.status, ExamResult.submitted_at)
        .order_by(ExamResult.submitted_at.desc())
        .all()
    )

    return render_template("admin_scores.html", results=results)