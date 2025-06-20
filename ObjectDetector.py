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
    def __init__(self, model_path=None, flag_callback=None):
        """
        Initialize the object detector with a YOLOv8 model.
        """
        self.model_path = model_path
        self.model = None
        self.flag_callback = flag_callback

    def load_model(self):
        """
        Load the YOLOv8 model.
        """
        # Uncomment when ultralytics is installed
        # self.model = YOLO(self.model_path or 'yolov8n.pt')
        pass

    def detect_objects(self, frame):
        """
        Detect objects in the frame. Returns list of detected objects with labels and bounding boxes.
        Flags if a cell phone is detected.
        """
        # Uncomment and implement when YOLOv8 is available
        # results = self.model(frame)
        # detections = []
        # for r in results:
        #     for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
        #         label = self.model.names[int(cls)]
        #         bbox = box.cpu().numpy().astype(int)
        #         detections.append({'label': label, 'bbox': bbox, 'conf': float(conf)})
        #         if label.lower() in ['cell phone', 'mobile phone', 'phone']:
        #             if self.flag_callback:
        #                 self.flag_callback('phone_detected')
        # return detections
        return [] 