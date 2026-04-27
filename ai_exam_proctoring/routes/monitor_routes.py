from flask import Blueprint, request, jsonify
from services.tab_monitor import TabMonitor

monitor_bp = Blueprint("monitor", __name__)

# store monitors for each session
tab_monitors = {}


@monitor_bp.route("/log_event", methods=["POST"])
def log_event():

    data = request.get_json()

    session_id = data.get("session_id")
    event_type = data.get("event_type")

    # safety check
    if not session_id:
        return jsonify({"error": "No session_id"}), 400

    # create monitor if not exists
    if session_id not in tab_monitors:
        tab_monitors[session_id] = TabMonitor(session_id)

    monitor = tab_monitors[session_id]

    # handle events
    if event_type == "Tab Switch":
        result = monitor.record_tab_switch()

    elif event_type == "Window Focus Lost":
        result = monitor.record_focus_loss()

    else:
        result = {"message": "Unknown event"}

    return jsonify(result)