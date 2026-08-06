"""
main.py
-------
The entry point. Run this file (directly, or via Windows Task
Scheduler) to execute one full daily cycle:

    load contacts -> find today's birthdays -> send WhatsApp messages
    -> log results -> update contacts.csv so no duplicates go out

This module contains almost no logic of its own — it just calls into
birthday_checker, whatsapp_sender, and logger in the right order.
"""

import birthday_checker
import logger
from whatsapp_sender import WhatsAppSender


def main():
    contacts = birthday_checker.load_contacts()
    todays_birthdays = birthday_checker.get_todays_birthdays(contacts)

    if todays_birthdays.empty:
        print("No birthdays today. Exiting.")
        return

    print(f"Found {len(todays_birthdays)} birthday(s) today.")

    sender = WhatsAppSender()
    sender.start()

    try:
        for _, row in todays_birthdays.iterrows():
            name = row["Name"]
            phone = row["Phone"]
            message = birthday_checker.build_message(row)

            try:
                sender.send_message(phone, message)
                logger.log_result(name, "Success")
                contacts = birthday_checker.mark_as_sent(contacts, name)
                print(f"✅ Sent birthday message to {name}")
            except Exception as e:
                logger.log_result(name, "Failed", str(e))
                print(f"❌ Failed to send to {name}: {e}")
    finally:
        sender.stop()
        birthday_checker.save_contacts(contacts)


if __name__ == "__main__":
    main()
