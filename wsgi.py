"""WSGI entry point for Render deployment.

This module exports the Flask app for gunicorn to use.
Render looks for this file to start the application.
"""

# Import Flask app from app module
from app import app

# Explicitly export app for gunicorn
__all__ = ['app']

if __name__ == "__main__":
    # For local testing
    app.run()
