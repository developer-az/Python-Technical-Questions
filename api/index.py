import os
import sys
import traceback

# Project root on the Python path (Vercel runs from /var/task)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Serverless: keep writable state in /tmp
os.environ.setdefault("VERCEL", os.environ.get("VERCEL", "1"))

try:
    from app import app as flask_app
except Exception:
    traceback.print_exc()
    raise

# Explicit template/static roots — reliable under Vercel packaging
flask_app.template_folder = os.path.join(ROOT, "templates")
flask_app.static_folder = os.path.join(ROOT, "static")
flask_app.root_path = ROOT

# Vercel Python looks for `app` (WSGI)
app = flask_app


def application(environ, start_response):
    return app(environ, start_response)
