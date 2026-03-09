"""
Object Detection Module
-----------------------

This module detects cheating-related objects using YOLOv8.

Objects of interest:
- Mobile phone
- Book
- Laptop
- Multiple persons

If these objects are detected during an exam,
the system may flag cheating behavior.
"""

from ultralytics import YOLO
import cv2


# Load YOLOv8 model
# The lightweight 'yolov8n' model is used for faster inference
model = YOLO("models/yolov8n.pt")


# Objects that may indicate cheating
CHEATING_OBJECTS = [
    "cell phone",
    "book",
    "laptop",
    "person"
]


def detect_objects(frame):
    """
    Detect objects in a frame using YOLOv8.

    Parameters:
    frame : numpy array
        Image frame from webcam

    Returns:
    detected_objects : list
        List of detected object labels
    """

    results = model(frame)

    detected_objects = []

    # Extract detection results
    for r in results:

        for box in r.boxes:

            class_id = int(box.cls[0])

            label = model.names[class_id]

            detected_objects.append(label)

    return detected_objects


def analyze_objects(frame):
    """
    Analyze detected objects to determine cheating behavior.
    """

    objects = detect_objects(frame)

    cheating_detected = False

    for obj in objects:

        if obj in CHEATING_OBJECTS:

            cheating_detected = True

            return {
                "status": f"{obj} detected",
                "cheating": True
            }

    return {
        "status": "No suspicious objects",
        "cheating": False
    }


def draw_object_boxes(frame):
    """
    Draw bounding boxes around detected objects.

    Useful for debugging or monitoring.
    """

    results = model(frame)

    annotated_frame = results[0].plot()

    return annotated_frame