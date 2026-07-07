# Gmail Calendar Meeting Agent

## Project Description

This project implements an AI-based Gmail and Google Calendar meeting assistant.

The agent reads recent Gmail messages, identifies meeting requests, extracts meeting information such as dates and times, checks Google Calendar availability, and generates draft email replies accordingly.

The project was developed in Python using Google APIs as part of an AI Agent assignment.

---

## Features

- Gmail OAuth authentication
- Google Calendar OAuth authentication
- Read recent Gmail messages
- Detect meeting requests
- Extract meeting dates
- Extract one or more proposed meeting times
- Identify missing meeting information
- Check Google Calendar availability
- Generate draft reply emails
- Project documentation (PRD, PLAN, TODO)

---

## Technologies

- Python
- Gmail API
- Google Calendar API
- Google OAuth 2.0
- Regular Expressions (Regex)
- Markdown

---

## Project Structure

```
gmail_calendar_agent/
│
├── real_main.py
├── pyproject.toml
├── README.md
├── PRD.md
├── PLAN.md
├── TODO.md
└── gmail_calendar_meeting_skill_prd.md
```

---

## Authentication

The project uses Google OAuth 2.0.

The following files are required locally but are intentionally excluded from the GitHub repository:

- credentials.json
- token.json

---

## Workflow

1. Authenticate with Gmail and Google Calendar.
2. Read recent Gmail messages.
3. Detect whether an email is a meeting request.
4. Extract the meeting date and proposed time(s).
5. Check Google Calendar availability.
6. Generate a suitable draft reply.

---

## Notes

This project demonstrates an end-to-end workflow for processing meeting requests using Gmail and Google Calendar APIs.

The current implementation focuses on meeting request detection, calendar availability checking, and draft reply generation, and can be extended in the future with more advanced LLM-based language understanding.
