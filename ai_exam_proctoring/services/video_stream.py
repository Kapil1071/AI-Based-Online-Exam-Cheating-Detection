"""
Video Stream Service (Improved Version)
--------------------------------------

Handles:
1. Webcam capture
2. AI cheating detection
3. Frame processing and streaming

Optimizations:
- Safe camera handling
- Frame resizing for performance
- FPS control
- Error handling
"""

import cv2
import time

from ai_modules.cheating_logic import evaluate_cheating


class VideoCamera:
    """
    Video camera handler class.
    """

    def __init__(self):
        """
        Initialize webcam capture safely.
        """
        self.video = cv2.VideoCapture(0)

        # ✅ Check if camera opened
        if not self.video.isOpened():
            raise RuntimeError("❌ Cannot access webcam")

    def __del__(self):
        """
        Release webcam properly.
        """
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        """
        Capture frame and process AI detection.

        Returns:
        JPEG encoded frame
        """

        success, frame = self.video.read()

        if not success:
            return None

        # ✅ Resize for faster processing (IMPORTANT)
        frame = cv2.resize(frame, (640, 480))

        # 🧠 Run AI detection
        result = evaluate_cheating(frame)

        status_text = ", ".join(result["events"])

        # 🎯 Draw status text
        cv2.putText(
            frame,
            status_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255) if result["cheating"] else (0, 255, 0),
            2
        )

        # Optional: draw border color
        color = (0, 0, 255) if result["cheating"] else (0, 255, 0)
        cv2.rectangle(frame, (0, 0), (640, 480), color, 2)

        # Encode frame
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()


# ===============================
# FRAME GENERATOR (IMPORTANT)
# ===============================

def generate_frames(camera):
    """
    Generator for streaming frames.
    """

    while True:

        frame = camera.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

        # ✅ Control FPS (VERY IMPORTANT)
        time.sleep(0.03)  # ~30 FPS