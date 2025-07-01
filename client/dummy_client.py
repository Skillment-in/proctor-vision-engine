import cv2
import time
import random
import requests

BASE_URL = "http://127.0.0.1:5000"

VIOLATIONS = [
    "impersonation",
    "spoofing_detected",
    "phone_detected",
    "off_camera",
    "eyes_off_screen",
    "eyes_closed",
    "audio_detected",
    "speaking"
]

def send_violation(violation):
    try:
        res = requests.post(f"{BASE_URL}/simulate_violation", json={"type": violation})
        if res.status_code == 200:
            print(f"[✅] Sent: {violation}")
        else:
            print(f"[❌] Failed to send: {violation}")
    except Exception as e:
        print(f"[⚠️] Error: {e}")

def run_camera_dummy():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    print("🚀 Dummy client started with camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[⚠️] Camera frame not captured.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            send_violation("impersonation")  # No face found
        else:
            # Randomly send a different violation
            if random.random() < 0.3:
                violation = random.choice(VIOLATIONS[1:])  # skip "impersonation"
                send_violation(violation)

        cv2.imshow('Dummy Client Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(random.randint(2, 5))  # Simulate human interval

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera_dummy()
