from flask import Flask, jsonify, request
from threading import Thread
from core.ProctoringEngine import ProctoringEngine
from flask_cors import CORS
import json
import logging
import time
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for browser-based clients

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# Initialize Proctoring Engine
engine = ProctoringEngine()
engine_thread = None

# === Helper Function to Log Violations ===
def log_to_file(violation_type):
    log_file = "proctoring_log.json"
    violation_entry = {
        "type": violation_type,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "frame": None
    }
    log = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(violation_entry)

    # Save updated logs
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

@app.route('/')
def index():
    return jsonify({"message": "Proctor Vision API is running."})

@app.route('/health', methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

@app.route('/start', methods=["GET"])
def start_engine():
    global engine_thread
    if not engine.running:
        engine_thread = Thread(target=engine.start)
        engine_thread.start()
        app.logger.info("Engine started.")
        return jsonify({"status": "Engine started."})
    else:
        return jsonify({"status": "Already running."})

@app.route('/stop', methods=["GET"])
def stop_engine():
    if engine.running:
        engine.stop()
        app.logger.info("Engine stopped.")
        return jsonify({"status": "Engine stopped."})
    else:
        return jsonify({"status": "Already stopped."})

@app.route('/restart', methods=["GET"])
def restart_engine():
    global engine_thread
    if engine.running:
        engine.stop()
        time.sleep(1)
    engine_thread = Thread(target=engine.start)
    engine_thread.start()
    app.logger.info("Engine restarted.")
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
        log_to_file(violation_type)  # Save to file
        app.logger.info(f"Violation logged: {violation_type}")
        return jsonify({"status": f"Violation '{violation_type}' logged."})
    return jsonify({"status": "Invalid request"}), 400

@app.route("/download_logs", methods=["GET"])
def download_logs():
    try:
        with open("violation_log.json", "r") as f:
            lines = f.readlines()
        logs = [json.loads(line.strip()) for line in lines]
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=["GET"])
def stats():
    return jsonify({"total_violations": len(engine.flag_logger.logs)})

# === MAIN ENTRY ===
if __name__ == '__main__':
    app.run(debug=True)
