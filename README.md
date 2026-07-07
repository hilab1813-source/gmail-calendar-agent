# Gmail Calendar Meeting Agent

## Project Description

This project implements an AI-based Gmail and Google Calendar meeting assistant developed in Python.

The agent reads recent Gmail messages, identifies meeting requests, extracts meeting information such as dates and proposed times, checks Google Calendar availability, and automatically generates Gmail draft replies when additional information is required or when the requested meeting time is unavailable.

The project was developed as part of an AI Agent assignment using Gmail API and Google Calendar API.

---

## Features

### Gmail Integration

- Gmail OAuth authentication
- Read the 5 most recent Gmail messages
- Extract email subject
- Extract email body

### Meeting Detection

- Detect meeting requests
- Extract meeting dates
- Extract one or more proposed meeting times
- Identify missing meeting information
- Ignore emails that are not meeting requests

### Google Calendar Integration

- Google Calendar OAuth authentication
- Check calendar availability
- Detect scheduling conflicts
- Handle full-day events

### Automatic Gmail Replies

The agent automatically creates Gmail draft replies when:

- The meeting date is missing
- The meeting time is missing
- The requested meeting time is unavailable

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
├── README.md
├── PRD.md
├── PLAN.md
├── TODO.md
├── gmail_calendar_meeting_skill_prd.md
└── pyproject.toml
```

---

## Authentication

The project uses Google OAuth 2.0 authentication.

The following files are required locally but are intentionally excluded from the public GitHub repository:

- credentials.json
- token.json

---

## Workflow

1. Authenticate with Gmail.
2. Authenticate with Google Calendar.
3. Read the five most recent Gmail messages.
4. Detect whether each email is a meeting request.
5. Extract meeting dates and proposed meeting times.
6. Check Google Calendar availability.
7. If a suitable time is available, create a calendar event.
8. If information is missing or the requested time is unavailable, generate a Gmail draft reply.

---

## System Architecture

```
                 Gmail API
                     │
                     ▼
            Read Recent Emails
                     │
                     ▼
        Meeting Request Detection
                     │
                     ▼
      Extract Date & Time Information
                     │
                     ▼
      Google Calendar Availability Check
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 Available Time        Time Not Available
          │                     │
          ▼                     ▼
 Create Calendar Event   Generate Gmail Draft
```

---

## Repository Contents

The repository includes:

- Python source code
- Gmail Calendar Meeting Skill
- PRD document
- PLAN document
- TODO document
- Project README

---

## Security

Sensitive authentication files are intentionally excluded from the public repository.

The following files are **NOT** included:

- credentials.json
- token.json

This follows Google OAuth security recommendations.

---

## Screenshots

The repository includes screenshots demonstrating:

1. Reading Gmail messages.
2. Meeting request detection.
3. Google Calendar availability check.
4. Gmail draft generation.
5. Program execution in Visual Studio Code.

---

## Notes

This project demonstrates a complete AI Agent workflow for meeting management using Gmail API and Google Calendar API.

The agent reads incoming emails, detects meeting requests, extracts meeting information, checks calendar availability, and automatically generates Gmail draft replies when appropriate.

The current implementation provides a complete working prototype and can be extended in the future with more advanced LLM-based language understanding.
