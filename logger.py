"""
logger.py
---------
Responsible for writing every send attempt (success or failure) to
logs/sent_log.csv, and making sure that file exists with the right
header before anything is appended.
"""

import csv
import os
from datetime import datetime

import config

FIELDNAMES = ["Date", "Time", "Name", "Status", "ErrorMessage"]


def ensure_log_file():
    """Create logs/sent_log.csv with a header row if it doesn't exist yet."""
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    if not os.path.exists(config.LOG_FILE):
        with open(config.LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def log_result(name, status, error_message=""):
    """Append one row describing the outcome of a send attempt."""
    ensure_log_file()
    now = datetime.now()

    with open(config.LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "Date": now.strftime(config.DATE_FORMAT),
            "Time": now.strftime("%H:%M"),
            "Name": name,
            "Status": status,
            "ErrorMessage": error_message,
        })

if __name__ == "__main__":
    log_result("Fahad Tariq", "Success", "")
    log_result("Test Target", "Failed", "Element timeout")
    print("Test rows written to logs/sent_log.csv!")