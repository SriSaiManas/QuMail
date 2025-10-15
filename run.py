#!/usr/bin/env python3
"""
QuMail Application Runner
Quantum Secure Email Client

Run this file to start the QuMail application.
"""

import os
import sys
from backend.app import create_app


def main():
    """Main entry point for the application."""

    # Set environment variables if not already set
    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'development'

    if not os.environ.get('SECRET_KEY'):
        print("Warning: Using default secret key. Set SECRET_KEY environment variable in production.")
        os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    # Create Flask application
    try:
        app = create_app()
    except Exception as e:
        print(f"Error creating Flask app: {e}")
        sys.exit(1)

    # Print startup information
    print("=" * 60)
    print("🔒 QuMail Application Started!")
    print("Access the app at http://127.0.0.1:5000/")
    print("=" * 60)

    # Run the app
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running the application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
