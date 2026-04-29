from flask import Blueprint, request, jsonify
from services.tab_monitor import TabMonitor
from database.models import ExamSession

monitor_bp = Blueprint("monitor", __name__)

# store monitors for each session
tab_monitors = {}


@monitor_bp.route("/log_event", methods=["POST"])
def log_event():

    data = request.get_json()

    session_id = data.get("session_id")
    event_type = data.get("event_type")

    if not session_id:
        return jsonify({"error": "No session_id"}), 400

    # create monitor if not exists, reading max_warnings from exam config
    if session_id not in tab_monitors:
        session = ExamSession.query.get(session_id)
        max_warnings = 3  # default
        if session and session.exam:
            max_warnings = session.exam.max_warnings
        tab_monitors[session_id] = TabMonitor(session_id, max_allowed=max_warnings)

    monitor = tab_monitors[session_id]

    # handle events
    if event_type == "Tab Switch":
        result = monitor.record_tab_switch()
    elif event_type == "Window Focus Lost":
        result = monitor.record_focus_loss()
    else:
        result = {"message": "Unknown event"}

    # Persist terminated state to DB
    if result.get("terminated"):
        session = ExamSession.query.get(session_id)
        if session and not session.terminated:
            session.terminated = True
            from database.db import db
            db.session.commit()

    return jsonify(result)