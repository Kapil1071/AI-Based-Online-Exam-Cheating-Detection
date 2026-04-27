

from services.cheating_logger import log_cheating_event


class TabMonitor:
    """
    Tracks tab-switch behavior for a particular exam session.
    """

    def __init__(self, session_id, max_allowed=3):
        self.session_id = session_id
        self.max_allowed = max_allowed
        self.switch_count = 0
        self.exam_terminated = False

    def record_tab_switch(self):
        """
        Record a tab-switch event and return structured response.
        """

        # If already terminated, ignore further events
        if self.exam_terminated:
            return {
                "cheating": True,
                "terminated": True,
                "warnings": self.switch_count,
                "message": "Exam already terminated"
            }

        # Increase counter
        self.switch_count += 1

        # Log basic event
        log_cheating_event(self.session_id, "Tab Switch")

        print(f"[TAB SWITCH] Session {self.session_id} -> Count: {self.switch_count}")

        # 🚨 Threshold reached → terminate exam
        if self.switch_count >= self.max_allowed:

            self.exam_terminated = True

            log_cheating_event(self.session_id, "Exam Terminated (Tab Abuse)")

            return {
                "cheating": True,
                "terminated": True,
                "warnings": self.switch_count,
                "message": "Exam terminated due to excessive tab switching"
            }

        # ⚠️ Warning stage
        return {
            "cheating": False,
            "terminated": False,
            "warnings": self.switch_count,
            "remaining": self.max_allowed - self.switch_count,
            "message": f"Warning {self.switch_count}/{self.max_allowed}"
        }

    def record_focus_loss(self):
        """
        Optional: Track window focus loss separately.
        """

        log_cheating_event(self.session_id, "Window Focus Lost")

        return {
            "cheating": False,
            "message": "Focus lost detected"
        }

    def reset(self):
        """
        Reset tab switch counter.
        """

        self.switch_count = 0
        self.exam_terminated = False

    def get_status(self):
        """
        Get current monitoring status.
        """

        return {
            "warnings": self.switch_count,
            "max_allowed": self.max_allowed,
            "terminated": self.exam_terminated
        }