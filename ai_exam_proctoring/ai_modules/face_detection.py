"""
Face Detection Module
---------------------

This module performs real-time face detection using OpenCV.

Purpose in the cheating detection system:

1. Detect if the student is present in front of the camera
2. Detect multiple faces (possible cheating)
3. Return detection results to the monitoring system
"""

import cv2


# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_faces(frame):
    """
    Detect faces in a video frame.

    Parameters:
    frame : numpy array
        The image frame captured from webcam

    Returns:
    faces : list
        List of detected face coordinates
    """

    # Convert frame to grayscale
    # Haar cascade works better with grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    return faces


def analyze_face_behavior(frame):
    """
    Analyze face detection results to determine cheating behavior.

    Returns:
    dict with detection result
    """

    faces = detect_faces(frame)

    face_count = len(faces)

    # Case 1: No face detected
    if face_count == 0:

        return {
            "status": "No Face Detected",
            "cheating": True
        }

    # Case 2: Multiple faces detected
    if face_count > 1:

        return {
            "status": "Multiple Faces Detected",
            "cheating": True
        }

    # Case 3: Normal
    return {
        "status": "Single Face Detected",
        "cheating": False
    }


def draw_face_boxes(frame):
    """
    Draw bounding boxes around detected faces.

    Used for debugging or live monitoring.

    Returns:
    frame with rectangles drawn
    """

    faces = detect_faces(frame)

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    return frame