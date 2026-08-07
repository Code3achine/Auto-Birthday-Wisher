---
tags: [project/birthday-reminder, design]
---

# Database Schema

## Contact Table

| Field | Type |
|---|---|
| ContactID | Integer |
| Name | Text |
| PhoneNumber | Text |
| BirthDate | Date |
| CustomMessage | Text |
| Active | Boolean |
| LastSentDate | Date |

## Log Table

| Field | Type |
|---|---|
| LogID | Integer |
| ContactID | Integer |
| Date | Date |
| Time | Time |
| Status | Text |
| ErrorMessage | Text |

## Sample `contacts.csv`
```csv
Name,Phone,Birthday,Message,Active,LastSent
Ali,+923001234567,15-08-2004,Happy Birthday Ali!,True,
Ahmed,+923111111111,01-01-2003,Happy Birthday Ahmed!,True,
Sara,+923222222222,10-10-2004,Happy Birthday Sara!,False,
```

## Sample `logs/sent_log.csv`
```csv
Date,Time,Name,Status
15-08-2026,09:00,Ali,Success
15-08-2026,09:02,Ahmed,Success
```

## Related
- [[Modules]]
- [[Functional-Requirements]]
- [[Logging]]
- [[00-Home|← Back to Home]]
