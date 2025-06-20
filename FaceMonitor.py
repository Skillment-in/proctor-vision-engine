"""
FaceMonitor.py
Continuously compares live face to registered encoding and flags impersonation.
"""

import face_recognition
import cv2
import time

class FaceMonitor:
    """
    Monitors the webcam feed for face verification and impersonation detection.
    """
    def __init__(self, registered_encoding, camera_index=0, flag_callback=None):
        """
        Initialize with registered face encoding, camera index, and optional flag callback.
        """
        self.registered_encoding = registered_encoding
        self.camera_index = camera_index
        self.flag_callback = flag_callback
        self.mismatch_start_time = None

    def verify_face(self, frame):
        """
        Compare the face in the frame to the registered encoding.
        Returns True if matched, False otherwise.
        """
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) != 1:
            return False, face_locations
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        match = face_recognition.compare_faces([self.registered_encoding], face_encoding)[0]
        return match, face_locations

    def monitor(self):
        """
        Continuously monitor the webcam for impersonation events.
        Flags if face mismatch persists for more than 2 seconds.
        """
        cap = cv2.VideoCapture(self.camera_index)
        self.mismatch_start_time = None
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            match, face_locations = self.verify_face(frame)
            if not match:
                if self.mismatch_start_time is None:
                    self.mismatch_start_time = time.time()
                elif time.time() - self.mismatch_start_time > 2:
                    if self.flag_callback:
                        self.flag_callback('impersonation')
                    # Optionally, save frame or take further action
            else:
                self.mismatch_start_time = None
            # Optionally, show frame for debugging
            cv2.imshow('Face Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows() 