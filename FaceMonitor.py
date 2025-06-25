import cv2
import face_recognition
import time

class FaceMonitor:
    def __init__(self, reference_image_path='reference.jpg', camera_index=0, flag_callback=None, tolerance=0.5):
        self.reference_image_path = reference_image_path
        self.camera_index = camera_index
        self.flag_callback = flag_callback
        self.tolerance = tolerance  # Lower means stricter matchimport cv2
import face_recognition
import time

class FaceMonitor:
    def __init__(self, reference_image_path='reference.jpg', camera_index=0, flag_callback=None, tolerance=0.5):
        self.reference_image_path = reference_image_path
        self.camera_index = camera_index
        self.flag_callback = flag_callback
        self.tolerance = tolerance  # Lower means stricter match
        self.known_encoding = self.load_reference_encoding()
        self.last_mismatch_time = None
        self.cooldown_seconds = 3

    def load_reference_encoding(self):
        image = face_recognition.load_image_file(self.reference_image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            raise ValueError("❌ No face found in reference image.")
        return encodings[0]

    def verify_face(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(encodings, face_locations):
            match = face_recognition.compare_faces([self.known_encoding], encoding, tolerance=self.tolerance)
            if match[0]:
                return True, [location]  # Face verified

        return False, face_locations  # Face not matched

    def monitor(self):
        cap = cv2.VideoCapture(self.camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            verified, locations = self.verify_face(frame)

            for top, right, bottom, left in locations:
                color = (0, 255, 0) if verified else (0, 0, 255)
                label = "Verified" if verified else "Imposter"
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if not verified:
                if self.last_mismatch_time is None:
                    self.last_mismatch_time = time.time()
                elif time.time() - self.last_mismatch_time > self.cooldown_seconds:
                    if self.flag_callback:
                        self.flag_callback("impersonation")
                    self.last_mismatch_time = time.time()
            else:
                self.last_mismatch_time = None

            cv2.imshow('Face Verification', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        self.known_encoding = self.load_reference_encoding()
        self.last_mismatch_time = None
        self.cooldown_seconds = 3

    def load_reference_encoding(self):
        image = face_recognition.load_image_file(self.reference_image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            raise ValueError("❌ No face found in reference image.")
        return encodings[0]

    def verify_face(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(encodings, face_locations):
            match = face_recognition.compare_faces([self.known_encoding], encoding, tolerance=self.tolerance)
            if match[0]:
                return True, [location]  # Face verified

        return False, face_locations  # Face not matched

    def monitor(self):
        cap = cv2.VideoCapture(self.camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            verified, locations = self.verify_face(frame)

            for top, right, bottom, left in locations:
                color = (0, 255, 0) if verified else (0, 0, 255)
                label = "Verified" if verified else "Imposter"
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if not verified:
                if self.last_mismatch_time is None:
                    self.last_mismatch_time = time.time()
                elif time.time() - self.last_mismatch_time > self.cooldown_seconds:
                    if self.flag_callback:
                        self.flag_callback("impersonation")
                    self.last_mismatch_time = time.time()
            else:
                self.last_mismatch_time = None

            cv2.imshow('Face Verification', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
