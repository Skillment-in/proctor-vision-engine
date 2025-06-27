# FlagLogger.py
import datetime
import json
import csv

class FlagLogger:
    def __init__(self, debug=False):
        self.logs = []
        self.debug = debug

    def log_violation(self, violation_type, frame_path=None):
        entry = {
            "type": violation_type,
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "frame": frame_path
        }
        self.logs.append(entry)

        if self.debug:
            print(f"[🛑 Violation Logged] {entry}")

    def export_json(self, path):
        with open(path, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def export_csv(self, path):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["type", "timestamp", "frame"])
            writer.writeheader()
            for entry in self.logs:
                writer.writerow(entry)
