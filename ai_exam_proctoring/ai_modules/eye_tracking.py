"""
Eye Tracking Module
-------------------

This module tracks eye behavior using MediaPipe Face Mesh.

Purpose in the cheating detection system:

1. Detect if eyes are looking away from screen
2. Detect if eyes are closed for long duration
3. Monitor student attention during exam
"""

import cv2
import mediapipe as mp
import numpy as np


# Initialize MediaPipe Face Mesh model
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)


# Landmark indices for eyes
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]


def get_eye_center(landmarks, eye_points):
    """
    Calculate the center point of an eye using landmark coordinates.
    """

    x1 = landmarks[eye_points[0]][0]
    y1 = landmarks[eye_points[0]][1]

    x2 = landmarks[eye_points[1]][0]
    y2 = landmarks[eye_points[1]][1]

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    return center_x, center_y


def detect_eye_direction(frame):
    """
    Detect basic eye direction.

    Returns:
    dict containing eye status
    """

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(frame_rgb)

    if not results.multi_face_landmarks:

        return {
            "status": "Face Not Detected",
            "cheating": True
        }

    face_landmarks = results.multi_face_landmarks[0]

    h, w, _ = frame.shape

    landmarks = []

    # Convert normalized landmarks to pixel coordinates
    for lm in face_landmarks.landmark:

        x = int(lm.x * w)
        y = int(lm.y * h)

        landmarks.append((x, y))

    # Calculate eye centers
    left_eye_center = get_eye_center(landmarks, LEFT_EYE)
    right_eye_center = get_eye_center(landmarks, RIGHT_EYE)

    # Calculate midpoint between both eyes
    gaze_x = (left_eye_center[0] + right_eye_center[0]) / 2

    # Simple logic for gaze direction
    screen_center = w / 2

    if gaze_x < screen_center - 100:

        return {
            "status": "Looking Left",
            "cheating": True
        }

    elif gaze_x > screen_center + 100:

        return {
            "status": "Looking Right",
            "cheating": True
        }

    else:

        return {
            "status": "Looking Forward",
            "cheating": False
        }


def draw_eye_landmarks(frame):
    """
    Draw eye landmarks for visualization.
    """

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(frame_rgb)

    if not results.multi_face_landmarks:

        return frame

    face_landmarks = results.multi_face_landmarks[0]

    h, w, _ = frame.shape

    for lm in face_landmarks.landmark:

        x = int(lm.x * w)
        y = int(lm.y * h)

        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    return frame