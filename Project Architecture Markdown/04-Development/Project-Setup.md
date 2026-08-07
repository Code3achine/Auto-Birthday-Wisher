---
tags: [project/birthday-reminder, development]
---

# Project Setup

## Phase 1 — Install Required Software
1. Python 3.x
2. Google Chrome
3. VS Code (optional)
4. Git (optional)

## Phase 2 — Create Project Folder
See folder layout in [[Modules]].

## Phase 3 — Create a Virtual Environment
PowerShell

```
python -m venv venv
```

**Activate (Windows Command Prompt):**

DOS

```
venv\Scripts\activate
```

**Activate (Windows PowerShell — Recommended with Execution Policy Fix):**

PowerShell

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned ; .\venv\Scripts\Activate.ps1
```

#### Phase 3.1 — Reactivate / Relaunch Virtual Environment

Whenever opening a fresh terminal or restarting VS Code, wake up dormant environment:

PowerShell

```
.\venv\Scripts\Activate.ps1
```

_(If PowerShell blocks activation script again in new session, re-run full command from Phase 3 above!)_

## Phase 4 — Install Required Libraries
```bash
pip install selenium pandas webdriver-manager pyperclip
```
Or:
```bash
pip install -r requirements.txt
```

**requirements.txt**
```text
selenium
pandas
webdriver-manager
pyperclip
```

## Related
- [[System-Requirements]]
- [[Implementation-Phases]]
- [[00-Home|← Back to Home]]
