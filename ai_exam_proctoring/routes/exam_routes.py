"""
Exam Routes
"""

import json
from datetime import datetime

from flask import Blueprint, render_template, Response, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from database.db import db
from database.models import ExamSession, Exam, StudentExam, Question

from services.video_stream import VideoCamera

import time

exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/student/dashboard")
@login_required
def student_dashboard():
    if current_user.role not in ("student",):
        if current_user.role == "admin":
            return redirect(url_for("admin.admin_dashboard"))
        if current_user.role == "staff":
            return redirect(url_for("staff.staff_dashboard"))

    student_exams = StudentExam.query.filter_by(student_id=current_user.id).all()
    return render_template("student_dashboard.html", student_exams=student_exams)


@exam_bp.route("/exam/<int:exam_id>")
@login_required
def start_exam(exam_id):
    if current_user.role != "student":
        flash("Only students can access exams.", "danger")
        return redirect(url_for("auth.login"))

    exam = Exam.query.get_or_404(exam_id)

    student_exam = StudentExam.query.filter_by(
        student_id=current_user.id,
        exam_id=exam_id
    ).first()

    if not student_exam or student_exam.status not in ("upcoming", "active"):
        flash("You are not enrolled in this exam or it is not available.", "danger")
        return redirect(url_for("exam.student_dashboard"))

    # Create or reuse exam session
    if student_exam.session_id:
        session = ExamSession.query.get(student_exam.session_id)
    else:
        session = ExamSession(user_id=current_user.id, exam_id=exam_id)
        db.session.add(session)
        db.session.commit()
        student_exam.session_id = session.id

    # Mark as active
    if student_exam.status == "upcoming":
        student_exam.status = "active"
        student_exam.start_time = datetime.utcnow()

    db.session.commit()

    questions = Question.query.filter_by(exam_id=exam_id).all()
    questions_data = []
    for q in questions:
        qd = {
            "id": q.id,
            "text": q.text,
            "type": q.question_type,
            "points": q.points,
            "options": json.loads(q.options) if q.options else []
        }
        questions_data.append(qd)

    return render_template(
        "exam.html",
        session_id=session.id,
        exam=exam,
        exam_id=exam_id,
        questions=questions_data,
        max_warnings=exam.max_warnings
    )


@exam_bp.route("/exam/<int:exam_id>/submit", methods=["POST"])
@login_required
def submit_exam(exam_id):
    if current_user.role != "student":
        return jsonify({"error": "Forbidden"}), 403

    student_exam = StudentExam.query.filter_by(
        student_id=current_user.id,
        exam_id=exam_id
    ).first()

    if not student_exam:
        flash("Exam record not found.", "danger")
        return redirect(url_for("exam.student_dashboard"))

    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})

    questions = Question.query.filter_by(exam_id=exam_id).all()
    total_score = 0
    for q in questions:
        if q.question_type == "mcq":
            submitted = answers.get(str(q.id), "")
            if submitted and submitted.strip() == (q.correct_answer or "").strip():
                total_score += q.points

    student_exam.answers = json.dumps(answers)
    student_exam.score = total_score
    student_exam.status = "finished"
    student_exam.end_time = datetime.utcnow()
    db.session.commit()

    return jsonify({"success": True, "score": total_score})


def generate_frames(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )
        time.sleep(0.03)


@exam_bp.route("/video_feed")
@login_required
def video_feed():
    session_id = request.args.get("session_id", type=int)
    camera = VideoCamera(session_id=session_id)
    return Response(
        generate_frames(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )