# Gmail Calendar Meeting Agent

## Project Description

This project implements an AI-based Gmail and Google Calendar meeting assistant.

The agent reads recent Gmail messages, identifies meeting requests, extracts meeting information, checks Google Calendar availability, and can prepare calendar events or email replies.

The project is implemented in Python using Google APIs and is designed to demonstrate an AI Agent workflow.

---

## Current Features

- Gmail OAuth authentication
- Google Calendar OAuth authentication
- Read recent Gmail messages
- Extract email subject
- Extract email body
- Meeting Skill specification for AI analysis
- Project documentation (PRD, PLAN, TODO)

---

## Planned Features

- AI meeting request detection
- Date extraction
- Multiple meeting time extraction
- Calendar availability check
- Automatic meeting scheduling
- Automatic reply generation when no suitable time is available

---

## Technologies

- Python
- Gmail API
- Google Calendar API
- Google OAuth 2.0
- Markdown
- AI / LLM

---

## Project Structure

```
gmail_calendar_agent/
│
├── real_main.py
├── PRD.md
├── PLAN.md
├── TODO.md
├── gmail_calendar_meeting_skill_prd.md
├── README.md
├── credentials.json
├── token.json
└── .venv/
```

---

## Notes

- `credentials.json` and `token.json` contain authentication information and should not be uploaded to GitHub.
- The AI meeting analysis will be connected in the final implementation.