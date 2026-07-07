# Gmail Calendar Agent - Development Plan

## Phase 1 - Authentication

- Connect to Gmail API.
- Connect to Google Calendar API.
- Authenticate using OAuth2.

---

## Phase 2 - Email Processing

- Read recent Gmail messages.
- Extract the email subject.
- Extract the email body.

---

## Phase 3 - Meeting Detection

- Detect whether the email contains a meeting request.
- Extract:
  - Date
  - Time
  - Multiple optional meeting times (if available)
  - Meeting duration (if available)

---

## Phase 4 - Calendar Management

- Check Google Calendar availability.
- Create a calendar event if an available slot exists.
- Prepare an email reply if no suitable time is available.

---

## Phase 5 - Testing

- Test emails with one meeting time.
- Test emails with multiple meeting time options.
- Test emails without meeting information.
- Test calendar conflicts.
- Verify Gmail draft creation.
- Verify calendar event creation.