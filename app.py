from flask import Flask, jsonify, render_template,request
from threading import Thread
from core.ProctoringEngine import ProctoringEngine

app = Flask(__name__)
engine = ProctoringEngine()
engine_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_engine():
    global engine_thread
    if not engine.running:
        engine_thread = Thread(target=engine.start)
        engine_thread.start()
        return jsonify({"status": "Engine started."})
    else:
        return jsonify({"status": "Already running."})

@app.route('/stop')
def stop_engine():
    if engine.running:
        engine.stop()
        return jsonify({"status": "Engine stopped."})
    else:
        return jsonify({"status": "Already stopped."})

@app.route('/status')
def status():
    return jsonify(engine.status)

@app.route('/violations')
def violations():
    return jsonify(engine.flag_logger.logs)

@app.route("/simulate_violation", methods=["POST"])
def simulate_violation():
    data = request.get_json()
    violation_type = data.get("type")
    if engine and violation_type:
        engine.handle_violation(violation_type)
        return jsonify({"status": f"Violation '{violation_type}' logged."})
    return jsonify({"status": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
