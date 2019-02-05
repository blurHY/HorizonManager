import os
from app import sio, app

sio.run(
    app, host="0.0.0.0", port=5000, debug=False
)  # Reloader may be not compatible with gevent,so just disable it.

# To Run:
# python run.py
# or
# python -m flask run
