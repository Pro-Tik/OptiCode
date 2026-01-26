"""
WSGI Entry Point
For production deployment on PythonAnywhere and other WSGI servers.
"""
import os
import sys

# Add the project directory to the path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import and create the Flask app
from app import create_app

# Create the application instance
# PythonAnywhere will use this 'application' variable
application = create_app('production')

# For compatibility with some deployment platforms
app = application

if __name__ == '__main__':
    application.run()
