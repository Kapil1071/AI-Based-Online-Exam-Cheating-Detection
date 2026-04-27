from flask import Blueprint, request, jsonify
from services.tab_monitor import TabMonitor
from database.models import ExamSession, Exam
from config import Config

monitor_bp = Blueprint("monitor", __name__)

tab_monitors = {}


@monitor_bp.route("/log_event", methods=["POST"])
def log_event():
    data = request.get_json()
    session_id = data.get("session_id")
    event_type = data.get("event_type")

    if not session_id:
        return jsonify({"error": "No session_id"}), 400

    if session_id not in tab_monitors:
        # Try to get max_warnings from Exam via ExamSession
        max_allowed = Config.MAX_TAB_SWITCHES
        try:
            exam_session = ExamSession.query.get(session_id)
            if exam_session and exam_session.exam_id:
                exam = Exam.query.get(exam_session.exam_id)
                if exam:
                    max_allowed = exam.max_warnings
        except Exception:
            pass
        tab_monitors[session_id] = TabMonitor(session_id, max_allowed=max_allowed)

    monitor = tab_monitors[session_id]

    if event_type == "Tab Switch":
        result = monitor.record_tab_switch()
    elif event_type == "Window Focus Lost":
        result = monitor.record_focus_loss()
    else:
        result = {"message": "Unknown event"}

    return jsonify(result)