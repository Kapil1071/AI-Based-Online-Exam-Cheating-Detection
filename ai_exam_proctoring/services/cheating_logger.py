"""
Cheating Logger Service
-----------------------

This module handles logging cheating events into the database.

It provides a centralized function so that any part of the
system (AI modules, routes, monitoring services) can log
cheating events easily.
"""

from database.db import db
from database.models import CheatingLog


def log_cheating_event(session_id, event_type, image_path=None):
    """
    Save a cheating event into the database.

    Parameters
    ----------
    session_id : int
        The exam session ID associated with the cheating event

    event_type : str
        Description of the cheating event

    image_path : str (optional)
        Path to evidence image if available
    """

    try:

        log = CheatingLog(
            session_id=session_id,
            event_type=event_type,
            image_path=image_path
        )

        db.session.add(log)
        db.session.commit()

        print(f"[CHEATING LOGGED] Session {session_id}: {event_type}")

    except Exception as e:

        print("Error logging cheating event:", str(e))