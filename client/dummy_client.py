import time
import requests
import random

# Server URL (update if hosted elsewhere)
BASE_URL = "http://127.0.0.1:5000"

# Sample violation types
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
        response = requests.post(f"{BASE_URL}/simulate_violation", json={"type": violation})
        if response.status_code == 200:
            print(f"[✅] Sent: {violation}")
        else:
            print(f"[❌] Failed to send: {violation}")
    except Exception as e:
        print(f"[⚠️] Error: {e}")

if __name__ == "__main__":
    print("🚀 Dummy client started. Sending simulated violations...")
    while True:
        violation = random.choice(VIOLATIONS)
        send_violation(violation)
        time.sleep(random.randint(2, 5))  # Send every 2–5 seconds
