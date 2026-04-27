"""
Database Initialization Module
------------------------------

This file creates the SQLAlchemy database object.

SQLAlchemy is an ORM (Object Relational Mapper) that allows
Python classes to represent database tables.

Instead of writing SQL queries manually, we interact with
the database using Python objects.

Example:
User(name="Kapil") → automatically becomes a row in database
"""

# Import SQLAlchemy ORM
from flask_sqlalchemy import SQLAlchemy


# Create the SQLAlchemy database instance
# This object will be used across the entire application
db = SQLAlchemy()