import cv2

def take_snapshot(filename="reference.jpg"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Webcam not detected.")
        return

    print("📷 Press 's' to take a snapshot or 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        cv2.imshow("Snapshot - Press 's' to save", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            cv2.imwrite(filename, frame)
            print(f"✅ Snapshot saved as {filename}")
            break
        elif key == ord('q'):
            print("❌ Snapshot canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_snapshot()
