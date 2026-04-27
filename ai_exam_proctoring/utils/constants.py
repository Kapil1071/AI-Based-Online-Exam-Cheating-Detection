"""
System Constants (Enhanced Version)
----------------------------------

Central configuration for:
- Detection thresholds
- Video settings
- Object detection
- Cheating scoring system

Designed for scalability and easy tuning.
"""

# ===============================
# CHEATING BEHAVIOR LIMITS
# ===============================

# Maximum allowed tab switches before warning/termination
MAX_TAB_SWITCHES = 3

# Maximum allowed seconds looking away
MAX_LOOK_AWAY_TIME = 5


# ===============================
# AI DETECTION PARAMETERS
# ===============================

# Head pose threshold (pixels)
HEAD_POSE_THRESHOLD = 40

# Eye gaze threshold (pixels)
EYE_GAZE_THRESHOLD = 100


# ===============================
# VIDEO SETTINGS
# ===============================

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# FPS control (used in video_stream)
TARGET_FPS = 30


# ===============================
# OBJECT DETECTION
# ===============================

# Objects considered suspicious (excluding "person" logic handled separately)
CHEATING_OBJECTS = [
    "cell phone",
    "book",
    "laptop"
]

# Minimum number of persons to trigger cheating
MULTIPLE_PERSON_THRESHOLD = 2


# ===============================
# CHEATING SCORE SYSTEM
# ===============================

# Score assigned per event
CHEATING_SCORES = {

    # Frontend behavior
    "Tab Switch": 2,
    "Window Focus Lost": 2,

    # Face + attention
    "Looking Left": 3,
    "Looking Right": 3,
    "Looking Down": 4,

    # Face detection issues
    "No Face Detected": 5,
    "Multiple Faces Detected": 6,

    # Object detection
    "cell phone detected": 10,
    "book detected": 5,
    "laptop detected": 5,
}

# Termination threshold
CHEATING_SCORE_THRESHOLD = 12


# ===============================
# UI / SYSTEM FLAGS
# ===============================

# Enable/disable logging (useful for debugging)
ENABLE_LOGGING = True

# Enable/disable AI detection (for testing UI only)
ENABLE_AI_DETECTION = True


# ===============================
# MESSAGE CONSTANTS
# ===============================

MESSAGES = {
    "NORMAL": "Monitoring Active",
    "WARNING": "Suspicious Activity Detected",
    "TERMINATED": "Exam Terminated Due to Cheating"
}