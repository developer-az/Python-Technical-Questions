import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app

# This is the WSGI application that Vercel will call
def application(environ, start_response):
    return app(environ, start_response)

# For direct access (what Vercel expects)
app = app