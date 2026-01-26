"""
Flask Extensions Module
Centralized extension instances for the application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Database ORM
db = SQLAlchemy()

# Cross-Origin Resource Sharing
cors = CORS()

# Database Migrations
migrate = Migrate()
