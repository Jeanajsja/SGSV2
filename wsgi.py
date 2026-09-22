import os
import sys

# para que uvicorn/gunicorn encuentren controllers, services, etc.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from main import app

# local: python -m uvicorn wsgi:app --reload --port 5000
# server: gunicorn -k uvicorn.workers.UvicornWorker wsgi:app --bind 0.0.0.0:5000
