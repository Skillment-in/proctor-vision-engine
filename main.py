"""
main.py
Entry point for Skillment proctoring engine. Orchestrates all modules and UI.
"""

import threading
import cv2
import os
import time
from FaceRegistration import FaceRegistration
from FaceMonitor import FaceMonitor
from HeadPoseDetector import HeadPoseDetector
from ObjectDetector import ObjectDetector
from EyeTracker import EyeTracker
from FlagLogger import FlagLogger

class ProctoringEngine:
    """
    Orchestrates all modules, manages threads, and handles UI.
    """
    def __init__(self):
        self.face_registration = FaceRegistration()
        self.flag_logger = FlagLogger()
        self.face_monitor = None
        self.head_pose_detector = None
        self.object_detector = None
        self.eye_tracker = None
        self.threads = []
        self.running = False
        self.status = {
            'face_match': False,
            'head_pose': 'Center',
            'phone_detected': False,
            'violations': 0,
            'eyes_status': 'Eyes Centered',
        }
        self.frame = None
        self.violation_frame_count = 0
        self.encoding_path = 'registered_face.pkl'
        self.log_path = 'proctoring_log.json'
        self.screenshot_dir = 'violations'
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def flag_callback(self, violation_type):
        # Save current frame as image
        frame_path = os.path.join(self.screenshot_dir, f'viol_{self.violation_frame_count}.jpg')
        if self.frame is not None:
            cv2.imwrite(frame_path, self.frame)
        else:
            frame_path = None
        self.flag_logger.log_violation(violation_type, frame_path)
        self.violation_frame_count += 1
        self.status['violations'] += 1
        if violation_type == 'phone_detected':
            self.status['phone_detected'] = True
        if violation_type.startswith('looking_'):
            self.status['head_pose'] = violation_type.replace('looking_', '').capitalize()
        if violation_type == 'impersonation':
            self.status['face_match'] = False
        if violation_type == 'eyes_off_screen' or violation_type == 'eyes_closed':
            self.status['eyes_status'] = violation_type.replace('_', ' ').capitalize()

    def start(self):
        # Register face if not already registered
        if not os.path.exists(self.encoding_path):
            print('Registering face...')
            if self.face_registration.register_face():
                self.face_registration.save_encoding(self.encoding_path)
                print('Face registered and encoding saved.')
            else:
                print('Face registration failed.')
                return
        else:
            self.face_registration.load_encoding(self.encoding_path)
            print('Loaded registered face encoding.')
        # Initialize modules
        self.face_monitor = FaceMonitor(self.face_registration.face_encoding, flag_callback=self.flag_callback)
        self.head_pose_detector = HeadPoseDetector(flag_callback=self.flag_callback)
        self.object_detector = ObjectDetector(flag_callback=self.flag_callback)
        self.eye_tracker = EyeTracker(flag_callback=self.flag_callback)
        self.running = True
        # Start main loop
        self.main_loop()

    def main_loop(self):
        cap = cv2.VideoCapture(0)
        phone_detected = False
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            self.frame = frame.copy()
            # Face verification
            match, face_locations = self.face_monitor.verify_face(frame)
            self.status['face_match'] = match
            # Draw face box and match status
            if face_locations:
                for (top, right, bottom, left) in face_locations:
                    color = (0, 255, 0) if match else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    label = 'MATCHED' if match else 'NOT MATCHED'
                    cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            # Head pose
            yaw, pitch, direction = self.head_pose_detector.estimate_head_pose(frame)
            self.status['head_pose'] = direction
            cv2.putText(frame, f'Head: {direction}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            if direction in ['Left', 'Right']:
                self.head_pose_detector.detect_look_away(direction)
                if self.head_pose_detector.look_away_start_time and time.time() - self.head_pose_detector.look_away_start_time > 3:
                    cv2.putText(frame, '⚠️ LOOKING AWAY > 3s', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            # Object detection (YOLOv8)
            detections = self.object_detector.detect_objects(frame)
            phone_detected = False
            for det in detections:
                label = det['label']
                bbox = det['bbox']
                if label.lower() in ['cell phone', 'mobile phone', 'phone']:
                    phone_detected = True
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
                    cv2.putText(frame, '📱 MOBILE DETECTED', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            self.status['phone_detected'] = phone_detected
            # Eye tracking
            eyes_status, eyes_closed = self.eye_tracker.estimate_gaze(frame)
            self.status['eyes_status'] = eyes_status
            if eyes_status == 'Eyes Off Screen':
                cv2.putText(frame, '⚠️ EYES OFF SCREEN', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            if eyes_closed:
                cv2.putText(frame, '⚠️ EYES CLOSED', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            # Status block
            status_block = [
                f'Face Match: {"✅" if self.status["face_match"] else "❌"}',
                f'Head Pose: {self.status["head_pose"]}',
                f'Phone Detected: {"✅" if self.status["phone_detected"] else "❌"}',
                f'Eyes: {self.status["eyes_status"]}',
                f'Violations Logged: {self.status["violations"]}',
            ]
            for i, line in enumerate(status_block):
                cv2.putText(frame, line, (10, 30 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Skillment Proctoring', frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                self.running = False
                break
        cap.release()
        cv2.destroyAllWindows()
        self.flag_logger.export_json(self.log_path)
        print(f'Logs exported to {self.log_path}')

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()

if __name__ == "__main__":
    engine = ProctoringEngine()
    engine.start() 