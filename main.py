"""
main.py
Entry point for Skillment proctoring engine. Orchestrates all modules and UI.
"""

import threading
import cv2
from FaceRegistration import FaceRegistration
from FaceMonitor import FaceMonitor
from HeadPoseDetector import HeadPoseDetector
from ObjectDetector import ObjectDetector
from EyeTracker import EyeTracker  # Optional
from FlagLogger import FlagLogger

class ProctoringEngine:
    """
    Orchestrates all modules, manages threads, and handles UI.
    """
    def __init__(self):
        self.face_registration = FaceRegistration()
        self.flag_logger = FlagLogger()
        self.face_monitor = None
        self.head_pose_detector = HeadPoseDetector()
        self.object_detector = ObjectDetector()
        self.eye_tracker = EyeTracker()  # Optional
        self.threads = []
        self.running = False

    def start(self):
        """
        Start the proctoring engine: register face, launch monitoring threads, and UI.
        """
        pass

    def stop(self):
        """
        Stop all threads and clean up resources.
        """
        pass

if __name__ == "__main__":
    engine = ProctoringEngine()
    engine.start() 