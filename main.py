"""
main.py
-------
Main execution script for the Auto Birthday Wisher automation.

This module handles:
1. Fetching active contacts from the Supabase database.
2. Evaluating birthday matches for the current calendar day (MM-DD).
3. Resolving custom vs. default message content (using config.py).
4. Sending WhatsApp messages via Green API.
5. Updating database records (last_sent) and writing log entries (logger.py).

FIXES applied:
- send_whatsapp() now has a timeout + try/except, never raises. One bad
  contact (network blip, malformed response) no longer kills the whole
  run for every remaining contact.
- logger.log_send(...) called directly — no more hasattr guessing that
  silently swallowed every log call.
"""

import os
import requests
from datetime import datetime, timezone
from supabase import create_client, Client

import config
import logger

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GREEN_INSTANCE_ID = os.getenv("GREEN_INSTANCE_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def send_whatsapp(phone_number: str, message_text: str) -> dict:
    """
    Sends a WhatsApp message via Green API REST endpoint.

    Always returns a dict — on any network/parse failure returns
    {"error": "..."} instead of raising, so one bad contact never
    kills the whole run.
    """
    url = f"https://api.green-api.com/waInstance{GREEN_INSTANCE_ID}/sendMessage/{GREEN_API_TOKEN}"
    payload = {
        "chatId": f"{phone_number}@c.us",
        "message": message_text
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"request_failed: {e}"}
    except ValueError:
        return {"error": f"non_json_response: {response.text}"}


def reset_stale_last_sent(row, now):
    """
    If last_sent is from a previous year, null it out in Supabase.
    Not required for dup-prevention (full YYYY-MM-DD compare already
    handles that), but keeps the LastSent column clean year over year.
    Mutates row in place so the rest of check_birthdays sees fresh data.
    """
    last_sent = row.get("last_sent")
    if not last_sent:
        return
    try:
        last_sent_year = int(str(last_sent)[:4])
    except (ValueError, TypeError):
        return
    if last_sent_year != now.year:
        supabase.table("contacts").update({"last_sent": None}).eq("id", row["id"]).execute()
        row["last_sent"] = None


def check_birthdays():
    """
    Queries active database contacts, evaluates birthday matches for today,
    dispatches WhatsApp notifications, and updates sent records.
    """
    response = supabase.table("contacts").select("*").eq("active", True).execute()
    contacts = response.data or []

    now = datetime.now(timezone.utc)
    today_md = now.strftime("%m-%d")
    today_ymd = now.strftime("%Y-%m-%d")

    for row in contacts:
        reset_stale_last_sent(row, now)

        if not row.get("birthday") or not row.get("phone"):
            continue

        bday_str = str(row["birthday"])[:10]
        try:
            bday_md = datetime.strptime(bday_str, "%Y-%m-%d").strftime("%m-%d")
        except ValueError:
            continue

        if bday_md != today_md or str(row.get("last_sent")) == today_ymd:
            continue

        name = str(row.get("name") or "Friend").strip()
        custom_msg = str(row.get("message") or "").strip()

        if not custom_msg or custom_msg.lower() in ["none", "nan", "null"]:
            final_msg = config.DEFAULT_MESSAGE.format(name=name)
        else:
            final_msg = custom_msg

        phone = str(row["phone"]).replace("+", "").replace("-", "").replace(" ", "").strip()

        res = send_whatsapp(phone, final_msg)

        if res.get("idMessage"):
            supabase.table("contacts").update({"last_sent": today_ymd}).eq("id", row["id"]).execute()
            print(f"SUCCESS: Sent to {name}")
            logger.log_send(name, phone, final_msg, "SUCCESS")
        else:
            print(f"FAILED for {name}: {res}")
            logger.log_send(name, phone, final_msg, f"FAILED: {res}")


if __name__ == "__main__":
    check_birthdays()
