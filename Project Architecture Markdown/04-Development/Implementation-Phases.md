---
tags: [project/birthday-reminder, development]
---

# Implementation Phases

## Phase 5 — Create Contact Database
See [[Database-Schema]] for `contacts.csv` structure.

## Phase 6 — Implement Birthday Checker
- Load contacts from CSV
- Read today's date
- Compare birthdays
- Ignore inactive contacts
- Skip contacts already messaged today

## Phase 7 — Implement WhatsApp Automation
See [[Workflow#WhatsApp Automation Sub-flow]].

## Phase 8 — First-Time Login
1. Run the program
2. WhatsApp Web opens
3. Scan the QR code
4. Keep the session logged in

## Phase 9 — Send Birthday Message
1. Open WhatsApp Web
2. Search contact
3. Open chat
4. Copy message to clipboard (`pyperclip.copy`)
5. Click message box, paste with Ctrl+V
6. Press Enter

> [!warning] Emoji fix
> Direct `send_keys(message)` crashes on emoji ("ChromeDriver only supports characters in the BMP"). Clipboard-paste avoids this without removing emoji.

## Phase 10 — Logging
See [[Logging]].

## Phase 11 — Prevent Duplicate Wishes
After a successful message:
```text
LastSent = Today's Date
```
Before sending:
```text
If LastSent == Today
    → Skip
```

## Phase 12 — Automate Daily Execution
Use **Windows Task Scheduler**.

- Trigger: Every Day, 9:00 AM
- Action: `python main.py`

## Related
- [[Project-Setup]]
- [[Development-Order]]
- [[Timeline]]
- [[00-Home|← Back to Home]]
