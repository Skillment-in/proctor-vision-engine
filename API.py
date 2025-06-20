"""
API.py
Optional FastAPI microservice for Skillment proctoring engine.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class RegisterRequest(BaseModel):
    user_id: str

class LogResponse(BaseModel):
    type: str
    timestamp: str
    frame: str = None

@app.post("/register")
def register_face(request: RegisterRequest):
    """
    Register a user's face.
    """
    # Placeholder logic
    return {"status": "registered"}

@app.post("/start-monitoring")
def start_monitoring():
    """
    Start monitoring for the registered user.
    """
    # Placeholder logic
    return {"status": "monitoring started"}

@app.get("/get-logs", response_model=List[LogResponse])
def get_logs():
    """
    Get all logged violations.
    """
    # Placeholder logic
    return [] 