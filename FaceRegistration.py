"""
FaceRegistration.py
Handles user face capture and registration using OpenCV only.
"""

import cv2
import os

class FaceRegistration:
    """
    Handles capturing a user's face and saving the face image as reference.jpg.
    """
    def __init__(self, camera_index=0, save_path='reference.jpg'):
        self.camera_index = camera_index
        self.save_path = save_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 1:
            return frame, faces[0]
        return frame, None

    def register_face(self):
        """
        Detect and save the user's face as reference.jpg using OpenCV only.
        Returns True if successful, False otherwise.
        """
        cap = cv2.VideoCapture(self.camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 1:
                x, y, w, h = faces[0]
                face_img = frame[y:y+h, x:x+w]
                cv2.imwrite(self.save_path, face_img)
                cap.release()
                cv2.destroyAllWindows()
                print(f"Face registered and saved as {self.save_path}")
                return True
            # Show frame and prompt user to center face
            cv2.imshow('Register Face - Center your face', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return False 