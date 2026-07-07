# Gmail Calendar Meeting Agent

## Project Overview

The Gmail Calendar Meeting Agent is an AI-based assistant that automatically manages meeting requests received by email.

The agent connects to Gmail and Google Calendar using the Google APIs.

Its goal is to reduce manual work by reading incoming emails, identifying meeting requests, checking calendar availability, creating calendar events, or preparing an email reply when no suitable time is available.

---

## Functional Requirements

The agent shall:

1. Read recent Gmail messages.
2. Extract the email subject and body.
3. Identify whether the email contains a meeting request.
4. Extract meeting details:
   - Date
   - Time
   - Multiple optional times (if provided)
   - Duration (if specified)
5. Check Google Calendar availability.
6. Create a calendar event when an available time exists.
7. Prepare an email reply if no suitable time is available.

---

## Technologies

- Python
- Gmail API
- Google Calendar API
- AI / LLM
- VS Code

---

## Expected Output
---

## Edge Cases

The agent should handle the following situations:

- The email is not a meeting request.
- The email contains multiple optional meeting times.
- The email does not include a valid date.
- The email does not include a valid time.
- All requested meeting times are unavailable.
- The calendar API or Gmail API is temporarily unavailable.
- The email contains text in Hebrew or English.

The system should automatically assist the user in scheduling meetings with minimal manual intervention.