"""
Helper Utility Functions
------------------------

This module contains reusable helper functions used across
different parts of the AI Exam Proctoring System.
"""

import os
import uuid
import cv2
from datetime import datetime


def generate_unique_filename(extension="jpg"):
    """
    Generate a unique filename for saving images.

    Example:
        evidence_3f2c9a7b.jpg
    """

    unique_id = uuid.uuid4().hex

    filename = f"evidence_{unique_id}.{extension}"

    return filename


def save_evidence_image(frame, folder="static/evidence"):
    """
    Save a webcam frame as an evidence image.

    Parameters
    ----------
    frame : numpy array
        Image captured from webcam

    folder : str
        Folder where evidence images will be stored

    Returns
    -------
    str
        Path to saved image
    """

    # Create folder if it does not exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = generate_unique_filename()

    filepath = os.path.join(folder, filename)

    cv2.imwrite(filepath, frame)

    return filepath


def current_timestamp():
    """
    Return current timestamp.

    Useful for logging events.
    """

    return datetime.utcnow()


def format_time(timestamp):
    """
    Format timestamp for display in dashboard.
    """

    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def is_suspicious_event(event_name):
    """
    Check if event should be considered suspicious.
    """

    suspicious_events = [
        "Tab Switch",
        "Window Focus Lost",
        "Looking Left",
        "Looking Right",
        "Multiple Faces Detected",
        "No Face Detected",
        "cell phone detected"
    ]

    return event_name in suspicious_events