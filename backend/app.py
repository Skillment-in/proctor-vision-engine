from flask import Flask, jsonify, request
from threading import Thread
from core.ProctoringEngine import ProctoringEngine
from flask_cors import CORS
import json
import logging
import time
import os
from datetime import datetime
import atexit
import sys

app = Flask(__name__)
CORS(app)

# === Setup Logging ===
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# === Create new log file on server start ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f"proctoring_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
with open(log_filename, "w") as f:
    f.write("[]")  # Initialize empty list

# === Initialize Engine with dynamic log path ===
engine = ProctoringEngine(log_path=log_filename)
engine_thread = None

# === Log Violations to JSON ===
def log_to_file(violation_type):
    violation_entry = {
        "type": violation_type,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "frame": None
    }
    logs = []
    if os.path.exists(engine.log_path):
        with open(engine.log_path, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(violation_entry)
    with open(engine.log_path, "w") as f:
        json.dump(logs, f, indent=2)

@app.route('/')
def index():
    return jsonify({"message": "✅ Proctor Vision API is running."})

@app.route('/health', methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

@app.route('/start', methods=["GET"])
def start_engine():
    global engine_thread

    if not os.path.exists("reference.jpg"):
        app.logger.warning("Reference image not found.")
        log_to_file("reference_image_missing")
        return jsonify({
            "status": "Reference image missing. Please upload a snapshot first.",
            "reference_missing": True
        }), 200

    if not engine.running:
        engine_thread = Thread(target=engine.start, daemon=True)
        engine_thread.start()
        app.logger.info("🚀 Engine started.")
        return jsonify({"status": "Engine started.", "reference_missing": False})
    else:
        return jsonify({"status": "Already running.", "reference_missing": False})

@app.route('/upload_reference', methods=["POST"])
def upload_reference():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    save_path = "reference.jpg"
    try:
        file.save(save_path)
        app.logger.info(f"📸 Reference image saved to {save_path}")
        return jsonify({"status": "Reference image uploaded successfully."}), 200
    except Exception as e:
        app.logger.error(f"❌ Failed to save reference image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stop', methods=["GET"])
def stop_engine():
    if engine.running:
        engine.stop()
        app.logger.info("🛑 Engine stopped.")
        return jsonify({"status": "Engine stopped."})
    else:
        return jsonify({"status": "Already stopped."})

@app.route('/restart', methods=["GET"])
def restart_engine():
    global engine_thread
    if engine.running:
        engine.stop()
        time.sleep(1)
    engine_thread = Thread(target=engine.start, daemon=True)
    engine_thread.start()
    app.logger.info("🔁 Engine restarted.")
    return jsonify({"status": "Engine restarted."})

@app.route('/status', methods=["GET"])
def status():
    return jsonify(engine.status)

@app.route('/violations', methods=["GET"])
def violations():
    return jsonify(engine.flag_logger.logs)

@app.route("/simulate_violation", methods=["POST"])
def simulate_violation():
    data = request.get_json()
    violation_type = data.get("type")
    if engine and violation_type:
        engine.handle_violation(violation_type)
        log_to_file(violation_type)
        app.logger.info(f"⚠️ Violation simulated and logged: {violation_type}")
        return jsonify({"status": f"Violation '{violation_type}' logged."})
    return jsonify({"status": "Invalid request"}), 400

@app.route("/download_logs", methods=["GET"])
def download_logs():
    try:
        with open(engine.log_path, "r") as f:
            logs = json.load(f)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/log_filename", methods=["GET"])
def get_log_filename():
    return jsonify({"log_file": engine.log_path})

@app.route('/stats', methods=["GET"])
def stats():
    return jsonify({"total_violations": len(engine.flag_logger.logs)})

# === Graceful Shutdown ===
def on_shutdown():
    print("📦 Cleaning up engine before exit...")
    if engine.running:
        engine.stop()

atexit.register(on_shutdown)

# === MAIN ENTRY ===
if __name__ == '__main__':
    try:
        print(f"🚀 Starting Proctor Vision Server...")
        print(f"📝 Log File: {log_filename}")
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt received. Shutting down engine...")
        on_shutdown()
        sys.exit(0)
