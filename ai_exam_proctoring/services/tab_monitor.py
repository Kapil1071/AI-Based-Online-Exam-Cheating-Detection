"""
Tab Monitor Service
-------------------

This module tracks browser tab switching events during an exam.

The frontend JavaScript sends tab-switch events to the backend.
This service counts violations and determines when cheating
thresholds are exceeded.
"""

from services.cheating_logger import log_cheating_event


class TabMonitor:
    """
    Tracks tab-switch behavior for a particular exam session.
    """

    def __init__(self, session_id, max_allowed=3):
        """
        Initialize tab monitoring.

        Parameters
        ----------
        session_id : int
            The exam session associated with this monitor

        max_allowed : int
            Maximum allowed tab switches before cheating is flagged
        """

        self.session_id = session_id
        self.max_allowed = max_allowed
        self.switch_count = 0


    def record_tab_switch(self):
        """
        Record a tab-switch event.
        """

        self.switch_count += 1

        # Log event
        log_cheating_event(self.session_id, "Tab Switch")

        print(f"[TAB SWITCH] Session {self.session_id} -> Count: {self.switch_count}")

        # Check if threshold exceeded
        if self.switch_count > self.max_allowed:

            log_cheating_event(self.session_id, "Excessive Tab Switching")

            return {
                "cheating": True,
                "message": "Too many tab switches detected"
            }

        return {
            "cheating": False,
            "message": "Tab switch recorded"
        }


    def reset(self):
        """
        Reset tab switch counter.
        """

        self.switch_count = 0