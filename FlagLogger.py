"""
FlagLogger.py
Logs and exports all proctoring violations.
"""

import datetime
import json
import csv

class FlagLogger:
    """
    Maintains a log of all violations and exports them.
    """
    def __init__(self):
        """
        Initialize the logger with an empty log list.
        """
        self.logs = []

    def log_violation(self, violation_type, frame_path=None):
        """
        Log a violation with type, timestamp, and optional frame path.
        """
        entry = {
            "type": violation_type,
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "frame": frame_path
        }
        self.logs.append(entry)
    


    def export_json(self, path):
        """
        Export the logs to a JSON file.
        """
        with open(path, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def export_csv(self, path):
        """
        Export the logs to a CSV file.
        """
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["type", "timestamp", "frame"])
            writer.writeheader()
            for entry in self.logs:
                writer.writerow(entry) 