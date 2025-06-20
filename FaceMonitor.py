"""
FaceMonitor.py
Continuously compares live face to registered encoding and flags impersonation.
"""

import cv2
import time

class FaceMonitor:
    """
    Stub: Face verification logic is disabled for now.
    """
    def __init__(self, reference_image_path='reference.jpg', camera_index=0, flag_callback=None):
        self.reference_image_path = reference_image_path
        self.camera_index = camera_index
        self.flag_callback = flag_callback

    def verify_face(self, frame):
        """
        Stub: Always returns True, no face verification.
        """
        return True, []

    def monitor(self):
        """
        Stub: Just shows the webcam frame, no verification.
        """
        cap = cv2.VideoCapture(self.camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imshow('Face Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows() 