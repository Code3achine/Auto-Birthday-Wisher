import os
import requests
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GREEN_INSTANCE_ID = os.getenv("GREEN_INSTANCE_ID")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_whatsapp(phone_number, message_text):
    url = f"https://api.green-api.com/waInstance{GREEN_INSTANCE_ID}/sendMessage/{GREEN_API_TOKEN}"
    payload = {
        "chatId": f"{phone_number}@c.us",
        "message": message_text
    }
    response = requests.post(url, json=payload)
    return response.json()

def check_birthdays():
    response = supabase.table("contacts").select("*").eq("active", True).execute()
    contacts = response.data
    today_md = datetime.now().strftime("%m-%d")
    today_ymd = datetime.now().strftime("%Y-%m-%d")

    for row in contacts:
        bday = datetime.strptime(row["birthday"], "%Y-%m-%d").strftime("%m-%d")
        if bday == today_md and row.get("last_sent") != today_ymd:
            res = send_whatsapp(str(row["phone"]), str(row["message"]))
            if res.get("idMessage"):
                supabase.table("contacts").update({"last_sent": today_ymd}).eq("id", row["id"]).execute()
                print(f"Sent to {row['name']}")
            else:
                print(f"Failed for {row['name']}: {res}")

if __name__ == "__main__":
    check_birthdays()