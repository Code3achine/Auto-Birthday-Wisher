"""
birthday_checker.py
--------------------
Responsible for everything related to *reading contacts* and *deciding
who should receive a birthday message today*.

It does NOT talk to WhatsApp and does NOT write log files — those jobs
belong to whatsapp_sender.py and logger.py respectively. Keeping this
module "pure data logic" makes it easy to unit test.
"""

from datetime import datetime
import pandas as pd

import config


def load_contacts():
    """Read contacts.csv into a pandas DataFrame."""
    df = pd.read_csv(config.CONTACTS_FILE)

    # Normalize types so comparisons below are reliable
    df["Active"] = df["Active"].astype(str).str.strip().str.lower() == "true"
    df["LastSent"] = df["LastSent"].fillna("").astype(str)
    return df


def save_contacts(df):
    """Persist any changes (e.g. updated LastSent) back to contacts.csv."""
    df.to_csv(config.CONTACTS_FILE, index=False)


def get_todays_birthdays(df=None, today=None):
    """
    Return the rows of the contacts DataFrame whose birthday matches
    today's day/month, skipping inactive contacts and anyone already
    messaged today.
    """
    if df is None:
        df = load_contacts()

    today = today or datetime.now()
    today_str = today.strftime(config.DATE_FORMAT)
    today_day_month = (today.day, today.month)

    def is_birthday_today(row):
        try:
            bday = datetime.strptime(row["Birthday"], config.DATE_FORMAT)
        except (ValueError, TypeError):
            return False
        return (bday.day, bday.month) == today_day_month

    matches = df[df.apply(is_birthday_today, axis=1)]
    matches = matches[matches["Active"]]
    matches = matches[matches["LastSent"] != today_str]

    return matches


def mark_as_sent(df, contact_name, today=None):
    """Update the LastSent column for a contact after a successful send."""
    today = today or datetime.now()
    today_str = today.strftime(config.DATE_FORMAT)
    df.loc[df["Name"] == contact_name, "LastSent"] = today_str
    return df


def build_message(row):
    """Return the message to send for a given contact row."""
    custom = str(row.get("Message", "")).strip()
    if custom and custom.lower() != "nan":
        return custom
    return config.DEFAULT_MESSAGE.format(name=row["Name"])

if __name__ == "__main__":
    df = load_contacts()
    targets = get_todays_birthdays(df)
    print("--- TODAY BIRTHDAY HUNTS ---")
    if targets.empty:
        print("No birthday target found today!")
    else:
        for idx, row in targets.iterrows():
            msg = build_message(row)
            print(f"Target: {row['Name']} | Phone: {row['Phone']} | Message: {msg}")