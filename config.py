"""
config.py
---------
Central place for all project settings. Change values here instead of
hunting through the other modules.
"""

import os

# --- Paths -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONTACTS_FILE = os.path.join(BASE_DIR, "contacts.csv")
LOG_FILE = os.path.join(BASE_DIR, "logs", "sent_log.csv")

# --- Date format used in contacts.csv (DD-MM) ----------------------
DATE_FORMAT = "%d-%m"

# --- Default message (used if a contact has no CustomMessage) ----------
DEFAULT_MESSAGE = "🎉 Happy Birthday, {name}! Wishing you a fantastic year ahead!"

# --- Selenium / WhatsApp Web settings -----------------------------------
WHATSAPP_URL = "https://web.whatsapp.com"
QR_LOGIN_TIMEOUT = 60        # seconds to wait for the user to scan the QR code
SEARCH_TIMEOUT = 20          # seconds to wait for the contact search results
MESSAGE_SEND_DELAY = 2       # seconds to pause before pressing Enter

# --- Chrome profile (keeps you logged in between runs) ------------------
CHROME_PROFILE_DIR = os.path.join(BASE_DIR, "chrome_profile")
