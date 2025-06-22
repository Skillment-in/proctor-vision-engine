"""
HeadPoseDetector.py
Estimates head pose (yaw, pitch) and flags if user looks away.
"""

import mediapipe as mp
import cv2
import time
import numpy as np

class HeadPoseDetector:
    """
    Uses mediapipe to estimate head pose and detect looking away.
    """
    def __init__(self, camera_index=0, flag_callback=None):
        """
        Initialize the head pose detector with a camera index and a flag callback.
        """
        self.camera_index = camera_index
        self.flag_callback = flag_callback
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.look_away_start_time = None
        self.last_direction = 'Center'

    def estimate_head_pose(self, frame):
        """
        Estimate yaw and pitch from the frame using mediapipe face mesh.
        Returns (yaw, pitch, direction_str).
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        if not results.multi_face_landmarks:
            return 0, 0, 'No Face'
        landmarks = results.multi_face_landmarks[0].landmark
        # Use key landmarks for pose estimation (nose tip, eyes, etc.)
        # For simplicity, use horizontal nose/eye position for yaw
        left_eye = np.array([landmarks[33].x, landmarks[33].y])
        right_eye = np.array([landmarks[263].x, landmarks[263].y])
        nose_tip = np.array([landmarks[1].x, landmarks[1].y])
        eye_center = (left_eye + right_eye) / 2
        dx = nose_tip[0] - eye_center[0]
        # Yaw: left/right, Pitch: up/down (not implemented here)
        yaw = dx * 100  # Scaled for easier thresholding
        if yaw < -0.5:
            direction = 'Left'
        elif yaw > 0.5:
            direction = 'Right'
        else:
            direction = 'Center'
        return yaw, 0, direction

    def detect_look_away(self, direction):
        """
        Determine if the user is looking left or right for more than 3 seconds.
        Calls flag_callback if violation occurs.
        """
        if direction in ['Left', 'Right']:
            if self.look_away_start_time is None:
                self.look_away_start_time = time.time()
            elif time.time() - self.look_away_start_time > 3:
                if self.flag_callback:
                    self.flag_callback(f'looking_{direction.lower()}')
        else:
            self.look_away_start_time = None 