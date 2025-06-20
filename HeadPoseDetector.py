"""
HeadPoseDetector.py
Estimates head pose (yaw, pitch) and flags if user looks away.
"""

import mediapipe as mp
import cv2

class HeadPoseDetector:
    """
    Uses mediapipe to estimate head pose and detect looking away.
    """
    def __init__(self, camera_index=0):
        """
        Initialize the head pose detector with a camera index.
        """
        self.camera_index = camera_index

    def estimate_head_pose(self, frame):
        """
        Estimate yaw and pitch from the frame.
        Returns (yaw, pitch, direction_str).
        """
        pass

    def detect_look_away(self, yaw, pitch):
        """
        Determine if the user is looking left, right, or forward.
        Returns direction string and flag if looking away.
        """
        pass 