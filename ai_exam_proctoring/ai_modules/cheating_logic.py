"""
Cheating Decision Engine
------------------------

This module combines outputs from all AI detection modules
and produces a final cheating decision.

Detectors used:

1. Face Detection
2. Eye Tracking
3. Head Pose Estimation
4. Object Detection
"""

# Import detection modules
from ai_modules.face_detection import analyze_face_behavior
from ai_modules.eye_tracking import detect_eye_direction
from ai_modules.head_pose import estimate_head_pose
from ai_modules.object_detection import analyze_objects


def evaluate_cheating(frame):
    """
    Run all AI detectors on the given frame.

    Parameters
    ----------
    frame : numpy array
        Frame captured from webcam

    Returns
    -------
    dict
        Final cheating evaluation
    """

    # Run all detection modules
    face_result = analyze_face_behavior(frame)

    eye_result = detect_eye_direction(frame)

    head_result = estimate_head_pose(frame)

    object_result = analyze_objects(frame)

    # Store suspicious activities
    suspicious_events = []

    # Face detection check
    if face_result["cheating"]:
        suspicious_events.append(face_result["status"])

    # Eye tracking check
    if eye_result["cheating"]:
        suspicious_events.append(eye_result["status"])

    # Head pose check
    if head_result["cheating"]:
        suspicious_events.append(head_result["status"])

    # Object detection check
    if object_result["cheating"]:
        suspicious_events.append(object_result["status"])

    # Final decision
    if len(suspicious_events) > 0:

        return {
            "cheating": True,
            "events": suspicious_events
        }

    return {
        "cheating": False,
        "events": ["Normal Behavior"]
    }