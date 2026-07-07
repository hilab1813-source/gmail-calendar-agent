from __future__ import annotations

import base64
import re
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import parseaddr
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_credentials() -> Credentials:
    creds = None

    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        Path(TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")

    return creds


def decode_base64_urlsafe(data: str) -> str:
    if not data:
        return ""

    padding = "=" * (-len(data) % 4)
    decoded_bytes = base64.urlsafe_b64decode(data + padding)
    return decoded_bytes.decode("utf-8", errors="ignore")


def extract_text_from_payload(payload: dict) -> str:
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        return decode_base64_urlsafe(data)

    parts = payload.get("parts", [])
    for part in parts:
        text = extract_text_from_payload(part)
        if text:
            return text

    data = payload.get("body", {}).get("data", "")
    return decode_base64_urlsafe(data)


def read_recent_emails(gmail_service, max_results=5):
    results = gmail_service.users().messages().list(
        userId="me",
        q="newer_than:2d -in:drafts",
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        msg = gmail_service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full",
        ).execute()

        headers = msg.get("payload", {}).get("headers", [])
        body = extract_text_from_payload(msg.get("payload", {}))

        subject = ""
        sender = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]
            elif header["name"] == "From":
                sender = header["value"]

        emails.append(
            {
                "id": message["id"],
                "from": sender,
                "sender_email": parseaddr(sender)[1],
                "subject": subject,
                "body": body.strip(),
            }
        )

    return emails


def extract_meeting_with_llm(email_body: str):
    """
    LLM/Skill analysis step.
    This function follows the Skill document and extracts meeting intent,
    date, optional times, and missing fields from the email body.
    """

    meeting_keywords = [
        "פגישה",
        "להיפגש",
        "לתאם",
        "ייעוץ",
        "זום",
        "פנויה",
        "פנוי",
        "זמינה",
        "זמין",
        "לקבוע",
        "אפשר",
    ]

    is_meeting = any(keyword in email_body for keyword in meeting_keywords)

    date_match = re.search(r"\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b", email_body)
    times = re.findall(r"\b\d{1,2}:\d{2}\b", email_body)

    date_value = None

    if date_match:
        day, month, year = date_match.groups()

        if len(year) == 2:
            year = "20" + year

        date_value = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    missing_fields = []

    if is_meeting and not date_value:
        missing_fields.append("date")

    if is_meeting and not times:
        missing_fields.append("time")

    return {
        "is_meeting": is_meeting,
        "date": date_value,
        "times": times,
        "location": None,
        "participants": [],
        "missing_fields": missing_fields,
    }


def create_gmail_draft(gmail_service, to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    draft = gmail_service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw}},
    ).execute()

    return draft["id"]


def generate_missing_info_reply(meeting: dict) -> str:
    if "date" in meeting["missing_fields"] and "time" in meeting["missing_fields"]:
        return (
            "שלום,\n\n"
            "תודה על ההודעה.\n"
            "אשמח לדעת באיזה תאריך ובאיזו שעה תרצי לקבוע את הפגישה.\n\n"
            "תודה!"
        )

    if "date" in meeting["missing_fields"]:
        return (
            "שלום,\n\n"
            "תודה על ההודעה.\n"
            "אשמח לדעת באיזה תאריך תרצי לקבוע את הפגישה.\n\n"
            "תודה!"
        )

    if "time" in meeting["missing_fields"]:
        return (
            "שלום,\n\n"
            "תודה על ההודעה.\n"
            "אשמח לדעת באיזו שעה תרצי לקבוע את הפגישה.\n\n"
            "תודה!"
        )

    return ""


def build_datetime(date_value: str, time_value: str) -> datetime:
    return datetime.fromisoformat(f"{date_value}T{time_value}:00").astimezone()


def is_calendar_available(calendar_service, start: datetime, end: datetime) -> bool:
    events = calendar_service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return len(events.get("items", [])) == 0


def create_calendar_event(calendar_service, email: dict, meeting: dict, time_value: str):
    start = build_datetime(meeting["date"], time_value)
    end = start + timedelta(hours=1)

    event = {
        "summary": f"Meeting from email: {email['subject']}",
        "description": (
            "Created automatically by Gmail Calendar Meeting Agent.\n\n"
            f"Original sender: {email['from']}\n"
            f"Original email body:\n{email['body']}"
        ),
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": end.isoformat()},
    }

    created = calendar_service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    return created["id"], created.get("htmlLink")


def process_email(gmail_service, calendar_service, email: dict):
    print("------")
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Body: {email['body']}")

    meeting = extract_meeting_with_llm(email["body"])

    print("Meeting analysis:")
    print(meeting)

    if not meeting["is_meeting"]:
        print("Result: Not a meeting request.")
        return

    if meeting["missing_fields"]:
        reply = generate_missing_info_reply(meeting)

        draft_id = create_gmail_draft(
            gmail_service,
            email["sender_email"],
            f"Re: {email['subject']}",
            reply,
        )

        print(f"Missing information draft created: {draft_id}")
        return

    for time_value in meeting["times"]:
        start = build_datetime(meeting["date"], time_value)
        end = start + timedelta(hours=1)

        if is_calendar_available(calendar_service, start, end):
            event_id, event_link = create_calendar_event(
                calendar_service,
                email,
                meeting,
                time_value,
            )

            print(f"Calendar event created: {event_id}")
            print(f"Event link: {event_link}")
            return

    reply = (
        "שלום,\n\n"
        "תודה על ההודעה.\n"
        "בדקתי את המועדים שהוצעו, אך הם אינם פנויים ביומן.\n"
        "אשמח לקבל מועדים נוספים.\n\n"
        "תודה!"
    )

    draft_id = create_gmail_draft(
        gmail_service,
        email["sender_email"],
        f"Re: {email['subject']}",
        reply,
    )

    print(f"Unavailable time draft created: {draft_id}")


def main():
    creds = get_credentials()

    gmail_service = build("gmail", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)

    emails = read_recent_emails(gmail_service, max_results=5)

    if not emails:
        print("No recent emails found.")
        return

    for email in emails:
        process_email(gmail_service, calendar_service, email)


if __name__ == "__main__":
    main()