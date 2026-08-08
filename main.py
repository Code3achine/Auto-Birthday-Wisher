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
"""

import os
import requests
from datetime import datetime
from supabase import create_client, Client

# Local module imports
import config
import logger

# Load environment variables for remote service authentication
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GREEN_INSTANCE_ID = os.getenv("GREEN_INSTANCE_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def send_whatsapp(phone_number: str, message_text: str) -> dict:
    """
    Sends a WhatsApp message payload via Green API REST endpoint.

    Args:
        phone_number (str): Clean recipient phone number without special symbols.
        message_text (str): Evaluated text content to deliver.

    Returns:
        dict: Parsed JSON response object from Green API server.
    """
    url = f"https://api.green-api.com/waInstance{GREEN_INSTANCE_ID}/sendMessage/{GREEN_API_TOKEN}"
    payload = {
        "chatId": f"{phone_number}@c.us",
        "message": message_text
    }
    response = requests.post(url, json=payload)
    return response.json()


def check_birthdays():
    """
    Queries active database contacts, evaluates birthday matches for today,
    dispatches WhatsApp notifications, and updates sent records.
    """
    # Fetch all active contacts from Supabase table
    response = supabase.table("contacts").select("*").eq("active", True).execute()
    contacts = response.data
    
    # Determine current month-day and full date strings for accurate matching
    today_md = datetime.now().strftime("%m-%d")
    today_ymd = datetime.now().strftime("%Y-%m-%d")

    for row in contacts:
        # Skip records without a valid birthday entry
        if not row.get("birthday"):
            continue

        # Safely extract YYYY-MM-DD prefix and convert to MM-DD comparison format
        bday_str = str(row["birthday"])[:10]
        try:
            bday_md = datetime.strptime(bday_str, "%Y-%m-%d").strftime("%m-%d")
        except ValueError:
            # Skip invalid date string formats
            continue

        # Check if today matches birthday month-day AND message hasn't been sent today
        if bday_md == today_md and str(row.get("last_sent")) != today_ymd:
            name = str(row.get("name") or "Friend").strip()
            custom_msg = str(row.get("message") or "").strip()
            
            # Fallback to config default message if custom message is empty or NULL
            if not custom_msg or custom_msg.lower() in ["none", "nan", "null"]:
                final_msg = config.DEFAULT_MESSAGE.format(name=name)
            else:
                final_msg = custom_msg

            # Clean phone number by removing country signs, dashes, and spaces
            phone = str(row["phone"]).replace("+", "").replace("-", "").replace(" ", "").strip()

            # Dispatch WhatsApp message via Green API
            res = send_whatsapp(phone, final_msg)

            # Process API response and update tracking records
            if res.get("idMessage"):
                # Update database last_sent timestamp on successful delivery
                supabase.table("contacts").update({"last_sent": today_ymd}).eq("id", row["id"]).execute()
                print(f"SUCCESS: Sent to {name}")
                
                # Delegate log persistence to the dedicated logger module
                if hasattr(logger, "log_send"):
                    logger.log_send(name, phone, final_msg, "SUCCESS")
                elif hasattr(logger, "log"):
                    logger.log(name, phone, "SUCCESS")
            else:
                print(f"FAILED for {name}: {res}")
                
                # Log failure status using logger module
                if hasattr(logger, "log_send"):
                    logger.log_send(name, phone, final_msg, f"FAILED: {res}")
                elif hasattr(logger, "log"):
                    logger.log(name, phone, f"FAILED: {res}")

if __name__ == "__main__":
    check_birthdays()
