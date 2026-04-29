

from database.db import db
from database.models import CheatingLog


def log_cheating_event(session_id, event_type, image_path=None):
   

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