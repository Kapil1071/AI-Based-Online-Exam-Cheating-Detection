"""
Video Stream Service
--------------------

This module captures webcam frames and runs the AI cheating detection
pipeline on each frame.

Responsibilities:
1. Capture webcam frames
2. Run cheating detection logic
3. Return processed frames
"""

import cv2

# Import the cheating decision engine
from ai_modules.cheating_logic import evaluate_cheating


class VideoCamera:
    """
    Video camera handler class.

    This class manages webcam access and frame processing.
    """

    def __init__(self):
        """
        Initialize webcam capture.
        """
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        """
        Release webcam when object is destroyed.
        """
        self.video.release()

    def get_frame(self):
        """
        Capture a frame from the webcam and analyze cheating behavior.

        Returns:
        processed frame in JPEG format
        """

        success, frame = self.video.read()

        if not success:
            return None

        # Run AI cheating detection
        result = evaluate_cheating(frame)

        # Display detection status on frame
        status_text = ", ".join(result["events"])

        cv2.putText(
            frame,
            status_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255) if result["cheating"] else (0, 255, 0),
            2
        )

        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()