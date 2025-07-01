import threading
import cv2
import os
import time
from Detectors.FaceMonitor import FaceMonitor
from Detectors.HeadPoseDetector import HeadPoseDetector
from Detectors.ObjectDetector import ObjectDetector
from Detectors.EyeTracker import EyeTracker
from core.FlagLogger import FlagLogger
from Detectors.audiomaster import AudioMonitor

class ProctoringEngine:
    def __init__(self, reference_image_path='reference.jpg', log_path='proctoring_log.json', flag_callback=None):
        self.reference_image_path = reference_image_path
        self.log_path = log_path
        self.flag_callback = flag_callback if flag_callback else self.handle_violation
        self.flag_logger = FlagLogger(debug=True)

        self.face_monitor = None
        self.head_pose_detector = None
        self.object_detector = None
        self.eye_tracker = None
        self.audio_monitor = None

        self.threads = []
        self.running = False
        self.frame = None
        self.violation_frame_count = 0
        self.encoding_path = 'registered_face.pkl'

        self.status = {
            'face_match': False,
            'head_pose': 'Center',
            'phone_detected': False,
            'violations': 0,
            'eyes_status': 'Eyes Centered',
            'audio_detected': False,
        }

    def take_reference_snapshot(self, filename="reference.jpg"):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open webcam.")
            return False

        print("📸 Press 's' to take a snapshot OR 'q' to cancel.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Take Snapshot", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                cv2.imwrite(filename, frame)
                print(f"✅ Snapshot saved as '{filename}'")
                break
            elif key == ord('q'):
                print("Cancelled.")
                break

        cap.release()
        cv2.destroyAllWindows()
        return os.path.exists(filename)

    def handle_violation(self, violation_type):
        self.flag_logger.log_violation(violation_type)
        self.violation_frame_count += 1
        self.status['violations'] += 1

        if violation_type == 'phone_detected':
            self.status['phone_detected'] = True
        if violation_type.startswith('looking_'):
            self.status['head_pose'] = violation_type.replace('looking_', '').capitalize()
        if violation_type in ['impersonation', 'spoofing_detected']:
            self.status['face_match'] = False
        if violation_type in ['eyes_off_screen', 'eyes_closed']:
            self.status['eyes_status'] = violation_type.replace('_', ' ').capitalize()
        if violation_type in ['audio_detected', 'speaking']:
            self.status['audio_detected'] = True
            threading.Timer(5, lambda: self.status.update({'audio_detected': False})).start()

        print(f"[⚠️ Violation Detected] {violation_type} | Total: {self.status['violations']}")

    def start(self):
        if not os.path.exists(self.reference_image_path):
            print("❗ No reference image found.")
            print("⚠️ Ask client to capture/upload the reference face.")
            self.running = False
            return

        print('✅ Loaded reference face image.')

        # Initialize detectors
        self.face_monitor = FaceMonitor(reference_image_path=self.reference_image_path, flag_callback=self.flag_callback)
        self.head_pose_detector = HeadPoseDetector(flag_callback=self.flag_callback)
        self.object_detector = ObjectDetector(flag_callback=self.flag_callback)
        self.eye_tracker = EyeTracker(flag_callback=self.flag_callback)
        self.audio_monitor = AudioMonitor(flag_callback=self.flag_callback, face_monitor=self.face_monitor)

        # Start audio monitor in separate thread
        audio_thread = threading.Thread(target=self.audio_monitor.start_monitoring, daemon=True)
        self.threads.append(audio_thread)
        audio_thread.start()

        self.running = True
        self.main_loop()

    def main_loop(self):
        cap = cv2.VideoCapture(0)
        no_face_start_time = None

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            self.frame = frame.copy()

            self.face_monitor.detect_lip_movement(frame)

            # Face verification
            is_verified, locations = self.face_monitor.verify_face(frame)
            self.status['face_match'] = is_verified
            for top, right, bottom, left in locations:
                color = (0, 255, 0) if is_verified else (0, 0, 255)
                label = "Verified" if is_verified else "Imposter"
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if not is_verified:
                self.flag_callback("impersonation")

            # Head pose
            yaw, pitch, direction = self.head_pose_detector.estimate_head_pose(frame)
            self.status['head_pose'] = direction
            if direction in ['Left', 'Right']:
                self.head_pose_detector.detect_look_away(direction)
                elapsed = time.time() - self.head_pose_detector.look_away_start_time if self.head_pose_detector.look_away_start_time else 0
                cv2.putText(frame, f'⚠️ LOOKING {direction.upper()} ({int(elapsed)}s)', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Face presence
            if direction == 'No Face':
                if no_face_start_time is None:
                    no_face_start_time = time.time()
                elif time.time() - no_face_start_time > 2:
                    cv2.putText(frame, '⚠️ FACE NOT IN CAMERA!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                    self.flag_callback("off_camera")
            else:
                no_face_start_time = None

            # Object detection
            detections = self.object_detector.detect_objects(frame)
            for det in detections:
                if det['label'].lower() in ['cell phone', 'mobile phone', 'phone']:
                    bbox = det['bbox']
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
                    cv2.putText(frame, '📱 MOBILE DETECTED', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    self.flag_callback("phone_detected")

            # Eye tracking
            eyes_status, eyes_closed = self.eye_tracker.estimate_gaze(frame)
            self.status['eyes_status'] = eyes_status
            if eyes_status == 'Eyes Off Screen':
                cv2.putText(frame, '⚠️ EYES OFF SCREEN', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
            if eyes_closed:
                cv2.putText(frame, '⚠️ EYES CLOSED', (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

            # Status overlay
            status_block = [
                f'Head Pose: {self.status["head_pose"]}',
                f'Phone Detected: {"✅" if self.status["phone_detected"] else "❌"}',
                f'Eyes: {self.status["eyes_status"]}',
                f'Audio: {"🎙️ Speech" if self.status["audio_detected"] else "🔇 Quiet"}',
                f'Face: {"✅ Verified" if self.status["face_match"] else "❌ Not Verified"}',
                f'Violations Logged: {self.status["violations"]}',
            ]
            for i, line in enumerate(status_block):
                cv2.putText(frame, line, (10, 30 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.imshow('Skillment Proctoring', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cap.release()
        cv2.destroyAllWindows()
        self.flag_logger.export_json(self.log_path)
        print(f'📄 Logs exported to {self.log_path}')

    def stop(self):
        self.running = False
        if self.audio_monitor:
            self.audio_monitor.stop_monitoring()
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=2)

if __name__ == "__main__":
    engine = ProctoringEngine()
    engine.start()
