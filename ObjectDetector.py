"""
ObjectDetector.py
Detects objects (e.g., mobile phones) in webcam frames using YOLOv8.
"""

import cv2
# from ultralytics import YOLO  # Uncomment when YOLOv8 is installed

class ObjectDetector:
    """
    Uses YOLOv8 to detect objects such as mobile phones in webcam frames.
    """
    def __init__(self, model_path=None):
        """
        Initialize the object detector with a YOLOv8 model.
        """
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """
        Load the YOLOv8 model.
        """
        pass

    def detect_objects(self, frame):
        """
        Detect objects in the frame. Returns list of detected objects with labels and bounding boxes.
        """
        pass 