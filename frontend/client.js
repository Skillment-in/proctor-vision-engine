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

startBtn.addEventListener("click", async () => {
  try {
    // Start engine on backend
    const engineRes = await fetch(`${BASE_URL}/start`);
    const engineData = await engineRes.json();
    console.log("Engine Start:", engineData.status);
    statusText.textContent = `Status: ${engineData.status}`;

    // Request camera & mic access
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    video.srcObject = stream;

    // Simulate violations every 5 seconds
    setInterval(() => {
      const violation = VIOLATIONS[Math.floor(Math.random() * VIOLATIONS.length)];
      sendViolation(violation);
    }, 5000);

  } catch (err) {
    console.error("Error:", err);
    statusText.textContent = "Status: Error accessing camera or backend";
  }
});

async function sendViolation(type) {
  try {
    const res = await fetch(`${BASE_URL}/simulate_violation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type })
    });
    const result = await res.json();
    console.log("[📤] Sent violation:", result.status);
  } catch (err) {
    console.error("Failed to send violation:", err);
  }
}
