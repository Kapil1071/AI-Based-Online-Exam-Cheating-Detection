"""
Object Detection Module (Enhanced Version)
------------------------------------------

Uses YOLOv8 to detect suspicious objects and multiple persons.

Improvements:
- Confidence filtering
- Uses centralized constants
- Efficient detection (single pass)
- Clean structured output
"""

from ultralytics import YOLO
import cv2

from utils.constants import CHEATING_OBJECTS, MULTIPLE_PERSON_THRESHOLD

# Load YOLO model once
model = YOLO("models/yolov8n.pt")

# Minimum confidence to consider detection valid
CONF_THRESHOLD = 0.5


def detect_objects(frame):
    """
    Detect objects in a frame using YOLOv8.

    Returns:
    list of (label, confidence)
    """

    results = model(frame)

    detected_objects = []

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])

            # ✅ Ignore low-confidence detections
            if conf < CONF_THRESHOLD:
                continue

            class_id = int(box.cls[0])
            label = model.names[class_id]

            detected_objects.append((label, conf))

    return detected_objects


def analyze_objects(frame):
    """
    Analyze detected objects and determine cheating.
    """

    detections = detect_objects(frame)

    labels = [obj[0] for obj in detections]

    person_count = labels.count("person")

    # 🚨 Rule 1: Multiple persons
    if person_count >= MULTIPLE_PERSON_THRESHOLD:
        return {
            "status": f"Multiple persons detected ({person_count})",
            "cheating": True,
            "type": "MULTI_PERSON"
        }

    # 🚨 Rule 2: Suspicious objects
    for label, conf in detections:
        if label in CHEATING_OBJECTS:
            return {
                "status": f"{label} detected ({conf:.2f})",
                "cheating": True,
                "type": "OBJECT"
            }

    return {
        "status": "Normal",
        "cheating": False,
        "type": "NONE"
    }


def draw_object_boxes(frame):
    """
    Draw bounding boxes on frame.
    """

    results = model(frame)

    annotated_frame = results[0].plot()

    return annotated_frame