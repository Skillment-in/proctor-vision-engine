const BASE_URL = "http://127.0.0.1:5000";
const statusText = document.getElementById("status");
const video = document.getElementById("video");
const startBtn = document.getElementById("startBtn");
const uploadSection = document.getElementById("uploadSection");
const snapshotCanvas = document.getElementById("snapshotCanvas");
const snapshotCtx = snapshotCanvas.getContext("2d");

let violationCount = 0;

const VIOLATIONS = [
  "impersonation",
  "spoofing_detected",
  "phone_detected",
  "off_camera",
  "eyes_off_screen",
  "eyes_closed",
  "audio_detected",
  "speaking"
];

// 🧠 Map type to message
function getWarningMessage(type) {
  switch (type) {
    case "phone_detected": return "📱 Please take your phone down!";
    case "speaking":
    case "audio_detected": return "🔇 Please stay silent!";
    case "eyes_off_screen": return "👀 Look at the screen!";
    case "eyes_closed": return "😴 Don't fall asleep!";
    case "off_camera": return "📷 Stay in the camera frame!";
    case "impersonation": return "🚨 Unknown face detected!";
    case "spoofing_detected": return "🛑 Spoofing attempt!";
    default: return "⚠️ Violation detected!";
  }
}

// 🚨 Violation handler
function showViolationAlert(message) {
  alert(message);
  violationCount++;
  if (violationCount >= 10) {
    alert("🚫 Too many violations! Closing test...");
    window.close();
  }
}

// 📤 Send violation to backend
async function sendViolation(type) {
  try {
    const res = await fetch(`${BASE_URL}/simulate_violation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type })
    });
    const result = await res.json();
    showViolationAlert(getWarningMessage(type));
  } catch (err) {
    console.error("Violation send failed:", err);
  }
}

// 📸 Snapshot capture and upload
function captureSnapshot() {
  snapshotCtx.drawImage(video, 0, 0, snapshotCanvas.width, snapshotCanvas.height);
  snapshotCanvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append("image", blob, "reference.jpg");

    try {
      const res = await fetch(`${BASE_URL}/upload_reference`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      alert("✅ Snapshot uploaded. You can now start the engine.");
      uploadSection.style.display = "none";
    } catch (err) {
      alert("❌ Snapshot upload failed.");
      console.error(err);
    }
  }, "image/jpeg");
}

// 🚀 Start engine
startBtn.addEventListener("click", async () => {
  try {
    const res = await fetch(`${BASE_URL}/start`);
    const data = await res.json();

    statusText.textContent = `Status: ${data.status}`;

    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    video.srcObject = stream;
    video.onloadedmetadata = () => video.play();

    if (data.reference_missing) {
      uploadSection.style.display = "block";
      alert("📸 Please capture your reference image to continue.");
      return;
    }

    // Simulate violations every 6s for testing
    setInterval(() => {
      const randomType = VIOLATIONS[Math.floor(Math.random() * VIOLATIONS.length)];
      sendViolation(randomType);
    }, 6000);
  } catch (err) {
    console.error("Startup error:", err);
    statusText.textContent = "Status: Camera or backend error.";
  }
});
// 📷 Capture snapshot on button click
document.getElementById("captureBtn").addEventListener("click", () => {
  captureSnapshot();
});
// 🖼️ Resize canvas to match video dimensions
video.addEventListener("loadedmetadata", () => {
  snapshotCanvas.width = video.videoWidth;
  snapshotCanvas.height = video.videoHeight;
});
// 🖼️ Resize canvas on video resize
window.addEventListener("resize", () => {
  snapshotCanvas.width = video.videoWidth;
  snapshotCanvas.height = video.videoHeight;
});