const BASE_URL = "http://127.0.0.1:5000";
const statusText = document.getElementById("status");
const video = document.getElementById("video");
const startBtn = document.getElementById("startBtn");

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

async function sendViolation(type) {
  try {
    const res = await fetch(`${BASE_URL}/simulate_violation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type })
    });
    const result = await res.json();
    console.log("[📤] Violation:", result.status);

    // Show browser-style popup alert
    alert(getWarningMessage(type));

  } catch (err) {
    console.error("❌ Failed to send violation:", err);
  }
}

startBtn.addEventListener("click", async () => {
  try {
    const res = await fetch(`${BASE_URL}/start`);
    const data = await res.json();
    statusText.textContent = `Status: ${data.status}`;

    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    video.srcObject = stream;

    video.onloadedmetadata = () => {
      video.play();
    };

    // Simulate random violations every 6 seconds
    setInterval(() => {
      const randomViolation = VIOLATIONS[Math.floor(Math.random() * VIOLATIONS.length)];
      sendViolation(randomViolation);
    }, 6000);
  } catch (err) {
    console.error("Startup Error:", err);
    statusText.textContent = "Status: Camera or backend error.";

    let violationCount = 0;

function showPopup(message) {
  popupMessage.textContent = message;
  popup.classList.remove("hidden");

  // Increment and check violation count
  violationCount++;
  console.log(`🚨 Violation Count: ${violationCount}`);

  if (violationCount >= 10) {
    alert("Too many violations. Closing the test window...");
    window.close(); // Will work if tab was opened with window.open()
  }
}

  }
});
