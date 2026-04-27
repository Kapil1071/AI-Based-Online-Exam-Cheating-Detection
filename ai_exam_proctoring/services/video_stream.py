import cv2
import time

from ai_modules.cheating_logic import evaluate_cheating


class VideoCamera:

    def __init__(self, session_id=None):
        self.session_id = session_id
        self.video = cv2.VideoCapture(0)

        if not self.video.isOpened():
            raise RuntimeError("Cannot access webcam")

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        success, frame = self.video.read()

        if not success:
            return None

        frame = cv2.resize(frame, (640, 480))

        result = evaluate_cheating(frame)

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

        color = (0, 0, 255) if result["cheating"] else (0, 255, 0)
        cv2.rectangle(frame, (0, 0), (640, 480), color, 2)

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()


def generate_frames(camera):
    while True:
        frame = camera.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

        time.sleep(0.03)
