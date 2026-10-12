"""
Vercel entry helper — keep in sync with api/index.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("VERCEL", os.environ.get("VERCEL", "1"))

from app import app as flask_app

flask_app.template_folder = os.path.join(ROOT, "templates")
flask_app.static_folder = os.path.join(ROOT, "static")
flask_app.root_path = ROOT

app = flask_app
