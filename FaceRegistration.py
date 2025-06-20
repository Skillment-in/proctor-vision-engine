"""
FaceRegistration.py
Handles user face capture and encoding registration.
"""

import face_recognition
import cv2
import pickle

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
        Returns (frame, face_location) or (None, None) if not found.
        """
        cap = cv2.VideoCapture(self.camera_index)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None, None
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 1:
            return frame, face_locations[0]
        return frame, None

    def register_face(self):
        """
        Detect and encode the user's face, save encoding to memory.
        Returns True if successful, False otherwise.
        """
        cap = cv2.VideoCapture(self.camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            if len(face_locations) == 1:
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                self.face_encoding = face_encoding
                cap.release()
                return True
            # Optionally, show frame and prompt user to center face
            cv2.imshow('Register Face - Center your face', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return False

    def save_encoding(self, path):
        """
        Save the face encoding to a file using pickle.
        """
        if self.face_encoding is not None:
            with open(path, 'wb') as f:
                pickle.dump(self.face_encoding, f)

    def load_encoding(self, path):
        """
        Load a face encoding from a file using pickle.
        """
        with open(path, 'rb') as f:
            self.face_encoding = pickle.load(f)
        return self.face_encoding 