---
tags: [project/birthday-reminder, requirements]
---

# Functional Requirements

## FR-1 · Contact Management
Each contact stores:
- Contact ID
- Name
- Phone Number
- Date of Birth
- Custom Message (Optional)
- Active Status

See also: [[Database-Schema]]

## FR-2 · Birthday Detection
- Compare current date with stored birthdays
- Identify today's birthdays
- Ignore inactive contacts

## FR-3 · WhatsApp Automation
- Launch Chrome
- Open WhatsApp Web
- Search contact
- Copy message to clipboard, paste with Ctrl+V (not typed key-by-key)
- Send message using Selenium

> [!note] Why paste, not type
> ChromeDriver's `send_keys()` cannot type emoji (outside the BMP character range). Messages are copied to the clipboard with `pyperclip` and pasted instead, so emoji survive.

## FR-4 · Duplicate Prevention
- Store last sent date
- Prevent duplicate wishes

## FR-5 · Logging
Stores:
- Contact Name
- Date
- Time
- Status
- Error Details

See also: [[Logging]]

## Related
- [[Objectives]]
- [[Non-Functional-Requirements]]
- [[00-Home|← Back to Home]]
