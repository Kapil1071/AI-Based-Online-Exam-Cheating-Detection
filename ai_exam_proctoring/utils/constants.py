"""
System Constants
----------------

This file stores global constants used throughout
the AI Exam Proctoring System.

Keeping constants centralized makes the system
easier to maintain and modify.
"""


# ===============================
# CHEATING THRESHOLDS
# ===============================

# Maximum allowed tab switches before flagging cheating
MAX_TAB_SWITCHES = 3

# Maximum seconds a student can look away from screen
MAX_LOOK_AWAY_TIME = 5


# ===============================
# AI DETECTION PARAMETERS
# ===============================

# Head pose threshold for detecting looking left/right
HEAD_POSE_THRESHOLD = 40

# Eye gaze threshold for determining screen focus
EYE_GAZE_THRESHOLD = 100


# ===============================
# VIDEO SETTINGS
# ===============================

# Default webcam device index
CAMERA_INDEX = 0

# Video resolution
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ===============================
# OBJECT DETECTION
# ===============================

# Suspicious objects detected by YOLO
CHEATING_OBJECTS = [
    "cell phone",
    "book",
    "laptop",
    "person"
]


# ===============================
# CHEATING SCORE SYSTEM
# ===============================

# Points assigned for each violation
CHEATING_SCORES = {
    "Tab Switch": 2,
    "Window Focus Lost": 2,
    "Looking Left": 3,
    "Looking Right": 3,
    "No Face Detected": 5,
    "Multiple Faces Detected": 6,
    "cell phone detected": 10
}

# Score threshold after which cheating is flagged
CHEATING_SCORE_THRESHOLD = 10