"""
EyeTracker.py
(Optional) Tracks eye gaze using mediapipe iris landmarks.
"""

import mediapipe as mp
import cv2
import time
import numpy as np

class EyeTracker:
    """
    Uses mediapipe to estimate gaze direction and eye closure.
    """
    def __init__(self, camera_index=0, flag_callback=None):
        """
        Initialize the eye tracker with a camera index.
        """
        self.camera_index = camera_index
        self.flag_callback = flag_callback
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
        self.off_screen_start_time = None
        self.closed_eyes_start_time = None

    def estimate_gaze(self, frame):
        """
        Estimate gaze direction from the frame.
        Returns direction string and flag if eyes are off screen or closed.
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        if not results.multi_face_landmarks:
            return 'No Face', False
        landmarks = results.multi_face_landmarks[0].landmark
        # Use iris landmarks for gaze estimation (simple heuristic)
        left_iris = np.array([landmarks[474].x, landmarks[474].y])
        right_iris = np.array([landmarks[469].x, landmarks[469].y])
        left_eye = np.array([landmarks[33].x, landmarks[33].y])
        right_eye = np.array([landmarks[263].x, landmarks[263].y])
        eye_center = (left_eye + right_eye) / 2
        iris_center = (left_iris + right_iris) / 2
        dx = iris_center[0] - eye_center[0]
        # Heuristic: if dx is large, eyes are off screen
        if abs(dx) > 0.04:
            direction = 'Eyes Off Screen'
            if self.off_screen_start_time is None:
                self.off_screen_start_time = time.time()
            elif time.time() - self.off_screen_start_time > 2:
                if self.flag_callback:
                    self.flag_callback('eyes_off_screen')
        else:
            direction = 'Eyes Centered'
            self.off_screen_start_time = None
        # Simple eye closure detection (vertical distance between eyelids)
        left_eye_top = np.array([landmarks[159].x, landmarks[159].y])
        left_eye_bottom = np.array([landmarks[145].x, landmarks[145].y])
        eye_open = np.linalg.norm(left_eye_top - left_eye_bottom) > 0.01
        if not eye_open:
            if self.closed_eyes_start_time is None:
                self.closed_eyes_start_time = time.time()
            elif time.time() - self.closed_eyes_start_time > 2:
                if self.flag_callback:
                    self.flag_callback('eyes_closed')
        else:
            self.closed_eyes_start_time = None
        return direction, not eye_open 