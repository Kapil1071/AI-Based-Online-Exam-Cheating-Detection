"""
Exam Routes
-----------

This module manages everything related to the student exam interface.

Responsibilities:
1. Start an exam session
2. Render the exam page
3. Provide a live webcam monitoring feed
"""

# Flask utilities
from flask import Blueprint, render_template, Response

# Flask login utilities
from flask_login import login_required, current_user

# Database imports
from database.db import db
from database.models import ExamSession

# Video streaming service
from services.video_stream import VideoCamera


# Create blueprint for exam routes
exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/exam")
@login_required
def start_exam():
    """
    Start a new exam session for the logged-in student.
    """

    # Create exam session linked to current user
    session = ExamSession(user_id=current_user.id)

    # Save session in database
    db.session.add(session)
    db.session.commit()

    # Render exam page with session id
    return render_template("exam.html", session_id=session.id)



def generate_frames(camera):
    """
    Generator function that continuously provides
    webcam frames for video streaming.
    """

    while True:

        frame = camera.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )



@exam_bp.route("/video_feed")
@login_required
def video_feed():
    """
    Live video streaming route.

    The browser accesses this endpoint to display
    the AI monitored webcam feed.
    """

    camera = VideoCamera()

    return Response(
        generate_frames(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )