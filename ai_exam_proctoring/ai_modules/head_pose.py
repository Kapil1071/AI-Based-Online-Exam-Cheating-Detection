"""
Head Pose Estimation Module
---------------------------

This module estimates the head orientation of the student using
MediaPipe Face Mesh and OpenCV.

Purpose in cheating detection:

1. Detect if student looks left or right frequently
2. Detect if student looks down (possible phone usage)
3. Detect if student looks away from screen
"""

import cv2
import mediapipe as mp
import numpy as np


# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)


def estimate_head_pose(frame):
    """
    Estimate head pose orientation.

    Parameters
    ----------
    frame : numpy array
        Frame captured from webcam

    Returns
    -------
    dict
        Head direction result
    """

    h, w, _ = frame.shape

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if not results.multi_face_landmarks:

        return {
            "status": "Face Not Detected",
            "cheating": True
        }

    face_landmarks = results.multi_face_landmarks[0]

    landmarks = []

    for lm in face_landmarks.landmark:

        x = int(lm.x * w)
        y = int(lm.y * h)

        landmarks.append((x, y))

    # Important facial landmarks
    nose = landmarks[1]
    left_eye = landmarks[33]
    right_eye = landmarks[263]

    # Calculate face direction
    eye_center_x = (left_eye[0] + right_eye[0]) / 2

    dx = nose[0] - eye_center_x

    # Threshold for detecting head direction
    threshold = 40

    if dx > threshold:

        return {
            "status": "Looking Right",
            "cheating": True
        }

    elif dx < -threshold:

        return {
            "status": "Looking Left",
            "cheating": True
        }

    else:

        return {
            "status": "Looking Forward",
            "cheating": False
        }


def draw_head_pose(frame):
    """
    Draw simple head pose indicator on frame.
    """

    result = estimate_head_pose(frame)

    text = result["status"]

    cv2.putText(
        frame,
        text,
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255) if result["cheating"] else (0, 255, 0),
        2
    )

    return frame