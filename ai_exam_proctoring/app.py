"""
Main Flask Application Entry Point
----------------------------------

This file starts the web server and connects all parts of the system.

Responsibilities:
1. Create Flask application
2. Load configuration
3. Initialize database
4. Register route modules
5. Start the server
"""

# Import Flask framework
from flask import Flask

# Import database object
from database.db import db

# Import configuration settings
from config import Config


# Import route blueprints
# Blueprints allow us to separate routes into multiple files
from routes.auth_routes import auth_bp
from routes.exam_routes import exam_bp
from routes.detection_routes import detection_bp
from routes.admin_routes import admin_bp



def create_app():
    """
    Application Factory Pattern

    This function creates and configures the Flask application.
    This pattern is used in professional Flask applications
    because it allows better scalability and testing.
    """

    # Create Flask application object
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize database with the Flask app
    db.init_app(app)

    # Register all route blueprints
    # Each blueprint represents a module of functionality

    app.register_blueprint(auth_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(admin_bp)

    return app



# Create the Flask app instance
app = create_app()


# Run the application
if __name__ == "__main__":

    """
    Debug mode automatically reloads server when code changes.
    Useful during development.
    """

    app.run(debug=True)