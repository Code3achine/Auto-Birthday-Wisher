---
tags: [project/birthday-reminder, design]
---

# Modules

1. **Contact Management** — add/edit/delete/view contacts ([[Functional-Requirements#FR-1 · Contact Management]])
2. **Birthday Checker** — compares today's date against stored birthdays ([[Functional-Requirements#FR-2 · Birthday Detection]])
3. **WhatsApp Automation** — drives Chrome/WhatsApp Web via Selenium ([[Functional-Requirements#FR-3 · WhatsApp Automation]])
4. **Logger** — records send status and errors ([[Logging]])

## Project File Layout
```text
BirthdayReminder/
│
├── main.py
├── birthday_checker.py
├── whatsapp_sender.py
├── logger.py
├── config.py
├── contacts.csv
├── requirements.txt
└── logs/
    └── sent_log.csv
```

## Related
- [[Database-Schema]]
- [[Workflow]]
- [[Project-Setup]]
- [[00-Home|← Back to Home]]
