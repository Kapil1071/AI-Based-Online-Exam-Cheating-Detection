# Flask utilities
from flask import Blueprint, render_template, Response, request

# Flask login utilities
from flask_login import login_required, current_user

# Database imports
from database.db import db
from database.models import ExamSession

# Video streaming service
from services.video_stream import VideoCamera

import time


# Create blueprint for exam routes
exam_bp = Blueprint("exam", __name__)


# ===============================
# START EXAM
# ===============================
@exam_bp.route("/exam")
@login_required
def start_exam():
    """
    Start a new exam session for the logged-in student.
    """

    # Create exam session
    session = ExamSession(user_id=current_user.id)

    db.session.add(session)
    db.session.commit()

    # Send session_id to frontend
    return render_template("exam.html", session_id=session.id)


# ===============================
# FRAME GENERATOR
# ===============================
def generate_frames(camera):
    """
    Generator for streaming frames with FPS control.
    """

    while True:

        frame = camera.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

        # ✅ FPS control (important for performance)
        time.sleep(0.03)  # ~30 FPS


# ===============================
# VIDEO FEED
# ===============================
@exam_bp.route("/video_feed")
@login_required
def video_feed():
    """
    Live video streaming route.

    Now supports session-aware monitoring.
    """

    # ✅ Get session_id from query params
    session_id = request.args.get("session_id", type=int)

    # Create camera with session context
    camera = VideoCamera(session_id=session_id)

    return Response(
        generate_frames(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )