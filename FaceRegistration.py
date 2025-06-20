"""
FaceRegistration.py
Handles user face capture and encoding registration.
"""

import face_recognition
import cv2

class FaceRegistration:
    """
    Handles capturing a user's face and saving the face encoding.
    """
    def __init__(self, camera_index=0):
        """
        Initialize the FaceRegistration with a camera index.
        """
        self.camera_index = camera_index
        self.face_encoding = None

    def capture_face(self):
        """
        Capture a face from the webcam and return the frame and face location.
        """
        pass

    def register_face(self):
        """
        Detect and encode the user's face, save encoding to file or memory.
        """
        pass

    def save_encoding(self, path):
        """
        Save the face encoding to a file.
        """
        pass

    def load_encoding(self, path):
        """
        Load a face encoding from a file.
        """
        pass 