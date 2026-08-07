---
tags: [project/birthday-reminder, operations]
---

# Logging

## FR-5 Logging Requirement
Each log entry stores:
- Contact Name
- Date
- Time
- Status
- Error Details

## Log Table Schema
See [[Database-Schema#Log Table]].

## Sample `logs/sent_log.csv`
```csv
Date,Time,Name,Status
15-08-2026,09:00,Ali,Success
15-08-2026,09:02,Ahmed,Success
```

## Related
- [[Functional-Requirements]]
- [[Error-Handling]]
- [[00-Home|← Back to Home]]
