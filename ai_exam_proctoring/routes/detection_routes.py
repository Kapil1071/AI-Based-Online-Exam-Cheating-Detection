from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.db import db
from database.models import ExamSession

# ✅ Correct blueprint name
detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/exam")
@login_required
def start_exam():
    session = ExamSession(user_id=current_user.id)

    db.session.add(session)
    db.session.commit()

    return render_template("exam.html", session_id=session.id)