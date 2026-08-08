"""
logger.py
---------
Writes every WhatsApp send attempt (success or failure) to
logs/sent_log.csv, creating the file with a header row if missing.

FIX: main.py calls logger.log_send(...) — that function didn't exist
before (only log_result did), so nothing was ever logged. log_send is
now the real, single source of truth for log rows.
"""

import csv
import os
from datetime import datetime, timezone

import config

FIELDNAMES = ["Date", "Time", "Name", "Phone", "Message", "Status", "ErrorMessage"]


def ensure_log_file():
    """Create logs/sent_log.csv with a header row if it doesn't exist yet."""
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    if not os.path.exists(config.LOG_FILE):
        with open(config.LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def log_send(name, phone, message, status):
    """Append one row describing the outcome of a WhatsApp send attempt.

    status: pass "SUCCESS" or "FAILED: <details>" — FAILED prefix gets
    split out into the ErrorMessage column automatically.
    """
    ensure_log_file()
    now = datetime.now(timezone.utc)

    error_message = ""
    clean_status = status
    if isinstance(status, str) and status.startswith("FAILED"):
        clean_status = "FAILED"
        error_message = status

    with open(config.LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "Date": now.strftime("%Y-%m-%d"),   # ISO date, was %d-%m (no year) before
            "Time": now.strftime("%H:%M:%S"),
            "Name": name,
            "Phone": phone,
            "Message": message,
            "Status": clean_status,
            "ErrorMessage": error_message,
        })


# Kept for backwards compatibility only — old name, do not use in new code.
def log_result(name, status, error_message=""):
    full_status = status if not error_message else f"FAILED: {error_message}"
    log_send(name, "", "", full_status)


if __name__ == "__main__":
    log_send("Fahad Tariq", "923009144966", "Happy Birthday!", "SUCCESS")
    log_send("Test Target", "923000000000", "Happy Birthday!", "FAILED: element timeout")
    print("Test rows written to logs/sent_log.csv!")
