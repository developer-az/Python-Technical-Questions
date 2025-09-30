# Vercel Entry Point for Flask App
import sys
import os

# Add the parent directory to Python path so we can import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the main Flask app
from app import app

# Vercel requires the app to be exposed for serverless functions
# This is the entry point for Vercel
app = app