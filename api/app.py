"""
Direct Flask app for Vercel deployment
This is a simplified version that imports everything needed
"""

import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the main app
from app import app

# Export for Vercel
app = app