"""
Application Configuration File
------------------------------

This file stores all configuration settings for the Flask application.

Keeping configuration separate from the main application code
is a best practice used in professional software development.

It allows easy modification of settings like:
- database connection
- secret keys
- debug mode
- model paths
"""

import os


class Config:
    """
    Base configuration class.

    Flask can load settings directly from this class.
    """

    # Secret key used for session security and form protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_key")


    # Database configuration
    # SQLite database stored in project root folder
    SQLALCHEMY_DATABASE_URI = "sqlite:///exam_proctoring.db"


    # Disable modification tracking to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Upload folder for storing cheating snapshots
    UPLOAD_FOLDER = "static/images"


    # Maximum allowed file size (example: 16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    # AI Model paths
    # These will be used later when loading YOLO / AI models
    YOLO_MODEL_PATH = "models/yolov8n.pt"


    # Cheating detection parameters
    # These values control how sensitive the system is
    MAX_LOOK_AWAY_TIME = 5
    MAX_TAB_SWITCHES = 3