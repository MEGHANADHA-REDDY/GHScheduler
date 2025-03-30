import sys
import os

# Add your project directory to the sys.path
project_home = os.path.expanduser('~/GHScheduler')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your app from app.py
from app import application

# This is the WSGI entry point that Gunicorn will use
app = application 
