"""
API.py
FastAPI microservice for Skillment Proctoring Engine.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import threading
from core.ProctoringEngine import ProctoringEngine
import os
import json

app = FastAPI(title="Skillment Proctoring API")

# Initialize the engine (lazy start)
engine = ProctoringEngine()
engine_thread = None


# ----------- Models -----------
class RegisterRequest(BaseModel):
    user_id: str

class LogResponse(BaseModel):
    type: str
    timestamp: str
    frame: str = None


# ----------- Endpoints -----------

@app.post("/register")
def register_face(request: RegisterRequest):
    """
    Register a user's face from reference.jpg (placeholder).
    You can extend this to accept image data via file upload.
    """
    try:
        engine.face_monitor.known_encoding = engine.face_monitor.load_reference_encoding()
        return {"status": "registered", "user_id": request.user_id}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/start-monitoring")
def start_monitoring():
    """
    Start the proctoring engine.
    """
    global engine_thread
    if not engine.running:
        engine_thread = threading.Thread(target=engine.start, daemon=True)
        engine_thread.start()
        return {"status": "monitoring started"}
    return {"status": "already running"}


@app.post("/stop-monitoring")
def stop_monitoring():
    """
    Stop the proctoring engine.
    """
    if engine.running:
        engine.stop()
        return {"status": "monitoring stopped"}
    return {"status": "not running"}


@app.get("/get-logs", response_model=List[LogResponse])
def get_logs():
    """
    Get all logged violations from JSON file.
    """
    log_path = engine.log_path
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
        return logs
    return []


@app.get("/status")
def get_status():
    """
    Get current status of the engine.
    """
    return engine.status
