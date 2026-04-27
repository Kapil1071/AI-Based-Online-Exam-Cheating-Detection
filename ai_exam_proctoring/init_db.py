"""
Database Initialization Script
------------------------------

This script creates the database tables defined in SQLAlchemy models.

It also optionally creates a default admin user so the system
can be accessed immediately after setup.

Run this file once before starting the application.

Command:
    python init_db.py
"""

# Import Flask app factory
from app import create_app

# Import database instance
from database.db import db

# Import models
from database.models import User

# Import password hashing utility
from werkzeug.security import generate_password_hash


def initialize_database():
    """
    Create database tables and insert default admin user.
    """

    # Create Flask application context
    app = create_app()

    with app.app_context():

        # Create all tables defined in models
        db.create_all()

        print("Database tables created successfully.")

        # Check if admin user already exists
        admin_user = User.query.filter_by(username="admin").first()

        if not admin_user:

            # Create default admin account
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

            print("Default admin account created.")
            print("Username: admin")
            print("Password: admin123")

        else:

            print("Admin user already exists.")


if __name__ == "__main__":

    initialize_database()