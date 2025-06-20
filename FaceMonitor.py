"""
FaceMonitor.py
Continuously compares live face to registered encoding and flags impersonation.
"""

import face_recognition
import cv2

class FaceMonitor:
    """
    Monitors the webcam feed for face verification and impersonation detection.
    """
    def __init__(self, registered_encoding, camera_index=0):
        """
        Initialize with registered face encoding and camera index.
        """
        self.registered_encoding = registered_encoding
        self.camera_index = camera_index

    def verify_face(self, frame):
        """
        Compare the face in the frame to the registered encoding.
        Returns True if matched, False otherwise.
        """
        pass

    def monitor(self):
        """
        Continuously monitor the webcam for impersonation events.
        """
        pass 