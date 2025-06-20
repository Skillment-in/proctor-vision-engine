"""
EyeTracker.py
(Optional) Tracks eye gaze using mediapipe iris landmarks.
"""

import mediapipe as mp
import cv2

class EyeTracker:
    """
    Uses mediapipe to estimate gaze direction and eye closure.
    """
    def __init__(self, camera_index=0):
        """
        Initialize the eye tracker with a camera index.
        """
        self.camera_index = camera_index

    def estimate_gaze(self, frame):
        """
        Estimate gaze direction from the frame.
        Returns direction string and flag if eyes are off screen or closed.
        """
        pass 