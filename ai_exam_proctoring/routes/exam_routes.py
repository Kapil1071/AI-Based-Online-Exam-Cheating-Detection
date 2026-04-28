# Flask utilities
from flask import Blueprint, render_template, Response, request, redirect, url_for, flash, jsonify

# Flask login utilities
from flask_login import login_required, current_user

# Database imports
from database.db import db
from database.models import Exam, ExamSession, Question, ExamAnswer, ExamResult

# Video streaming service
from services.video_stream import VideoCamera

import time


# Create blueprint for exam routes
exam_bp = Blueprint("exam", __name__)


# ===============================
# START EXAM
# ===============================
@exam_bp.route("/exam/<int:exam_id>")
@login_required
def start_exam(exam_id):
    """
    Start or resume an exam session for the logged-in student.
    """
    if current_user.role != "student":
        flash("Only students can take exams.", "warning")
        return redirect(url_for("auth.login"))

    exam = Exam.query.get_or_404(exam_id)

    if exam.status == "upcoming":
        flash("This exam has not started yet.", "warning")
        return redirect(url_for("student.student_dashboard"))

    if exam.status == "finished":
        flash("This exam has already finished.", "info")
        return redirect(url_for("student.student_dashboard"))

    # Check for an existing non-terminated session
    session = (
        ExamSession.query
        .filter_by(user_id=current_user.id, exam_id=exam_id, terminated=False)
        .filter(ExamSession.end_time.is_(None))
        .first()
    )

    if not session:
        session = ExamSession(user_id=current_user.id, exam_id=exam_id)
        db.session.add(session)
        db.session.commit()

    questions = Question.query.filter_by(exam_id=exam_id).order_by(Question.order).all()

    # Load existing answers
    existing_answers = {
        a.question_id: a.answer_text
        for a in ExamAnswer.query.filter_by(session_id=session.id).all()
    }

    return render_template(
        "exam.html",
        session_id=session.id,
        exam=exam,
        questions=questions,
        existing_answers=existing_answers,
    )


# Legacy redirect for old /exam route
@exam_bp.route("/exam")
@login_required
def start_exam_default():
    exam = Exam.query.order_by(Exam.scheduled_at).first()
    if exam:
        return redirect(url_for("exam.start_exam", exam_id=exam.id))
    flash("No exams available.", "info")
    return redirect(url_for("student.student_dashboard"))


# ===============================
# SAVE ANSWER (AJAX)
# ===============================
@exam_bp.route("/exam/save_answer", methods=["POST"])
@login_required
def save_answer():
    """
    Save or update a single answer via AJAX.
    """
    data = request.get_json()
    session_id = data.get("session_id")
    question_id = data.get("question_id")
    answer_text = data.get("answer_text", "")

    if not session_id or not question_id:
        return jsonify({"error": "Missing data"}), 400

    session = ExamSession.query.get(session_id)
    if not session or session.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    answer = ExamAnswer.query.filter_by(
        session_id=session_id, question_id=question_id
    ).first()

    if answer:
        answer.answer_text = answer_text
    else:
        answer = ExamAnswer(
            session_id=session_id,
            question_id=question_id,
            answer_text=answer_text,
        )
        db.session.add(answer)

    db.session.commit()
    return jsonify({"saved": True})


# ===============================
# SUBMIT EXAM
# ===============================
@exam_bp.route("/exam/submit/<int:session_id>", methods=["POST"])
@login_required
def submit_exam(session_id):
    """
    Submit the exam: grade MCQs, create ExamResult.
    """
    session = ExamSession.query.get_or_404(session_id)
    if session.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if session.result:
        flash("Exam already submitted.", "info")
        return redirect(url_for("student.student_dashboard"))

    exam = session.exam
    questions = Question.query.filter_by(exam_id=exam.id).all()
    total = sum(q.points for q in questions)
    score = 0

    for q in questions:
        ans = ExamAnswer.query.filter_by(
            session_id=session_id, question_id=q.id
        ).first()
        if ans and q.is_mcq and ans.answer_text:
            correct = ans.answer_text.strip().upper() == (q.correct_answer or "").upper()
            ans.is_correct = correct
            if correct:
                ans.points_awarded = q.points
                score += q.points

    from datetime import datetime
    session.end_time = datetime.utcnow()

    result = ExamResult(
        session_id=session_id,
        score=score,
        total_points=total,
        status="terminated" if session.terminated else "completed",
    )
    db.session.add(result)
    db.session.commit()

    flash(f"Exam submitted! Your score: {score} / {total}", "success")
    return redirect(url_for("student.student_dashboard"))


# ===============================
# FRAME GENERATOR
# ===============================
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


# ===============================
# VIDEO FEED
# ===============================
@exam_bp.route("/video_feed")
@login_required
def video_feed():
    session_id = request.args.get("session_id", type=int)
    camera = VideoCamera(session_id=session_id)
    return Response(
        generate_frames(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )