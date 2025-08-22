# simulator/mgmt/routes/telemetry.py
import os
import time
import json
import queue
import threading
import logging
import socket
from typing import Optional, Set, Dict, Any
from typing import Tuple
import requests
from flask import jsonify, Response, stream_with_context, current_app
from . import bp
from .utils import LITE

# python-socketio client (to receive from Companion Computer)
import socketio as sio_client

log = logging.getLogger(__name__)

DEFAULT_COMPANION = f"http://10.13.0.3:3000"

COMPANION_BASE_URL = os.getenv("COMPANION_BASE_URL", DEFAULT_COMPANION)

# ---------- Public helpers used by other modules ----------
def start_companion_telemetry(data: dict):
    url = f"{COMPANION_BASE_URL}/telemetry/start-telemetry"
    try:
        r = requests.post(url, json=data, timeout=10)
        log.info("[telemetry] start -> %s %s", r.status_code, r.text[:200])
    except Exception as e:
        pass

def stop_companion_telemetry():
    url = f"{COMPANION_BASE_URL}/telemetry/stop-telemetry"
    try:
        r = requests.post(url, timeout=10)
        log.info("[telemetry] stop -> %s %s", r.status_code, r.text[:200])
    except Exception as e:
        pass