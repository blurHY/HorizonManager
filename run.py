import os
from app import socketio, app

socketio.run(app, host="0.0.0.0")

# To Run:
# python run.py
# or
# python -m flask run
