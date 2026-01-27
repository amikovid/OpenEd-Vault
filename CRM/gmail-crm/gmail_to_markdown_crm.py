#!/usr/bin/env python3
"""
Gmail to Markdown CRM

Extracts genuine correspondences from Gmail and creates Obsidian-compatible
markdown files with YAML frontmatter for Dataview queries.

Usage:
    python gmail_to_markdown_crm.py --extract
    python gmail_to_markdown_crm.py --extract --max-results 1000
"""

import os
import json
import pickle
import re
import argparse
from datetime import datetime
from collections import defaultdict
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.pickle"

CRM_OUTPUT_DIR = SCRIPT_DIR.parent.parent / "CRM" / "contacts"

NOISE_PATTERNS = [
    r"noreply@",
    r"no-reply@",
    r"donotreply@",
    r"notifications@",
    r"updates@",
    r"newsletter@",
    r"marketing@",
    r"support@.*\.zendesk\.com",
    r"@mail\.github\.com",
    r"@.*\.substack\.com",
    r"@amazonses\.com",
    r"@sendgrid\.net",
    r"@mailchimp\.com",
    r"@constantcontact\.com",
    r"calendar-notification@google\.com",
    r"@facebookmail\.com",
    r"@linkedin\.com",
    r"@twitter\.com",
    r"@x\.com",
]

EXCLUDED_DOMAINS = {
    "amazon.com",
    "paypal.com",
    "venmo.com",
    "square.com",
    "stripe.com",
    "uber.com",
    "lyft.com",
    "doordash.com",
    "grubhub.com",
    "netflix.com",
    "spotify.com",
    "apple.com",
    "google.com",
    "bankofamerica.com",
    "chase.com",
    "wellsfargo.com",
    "capitalone.com",
}

PERSONAL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "me.com",
    "aol.com",
    "protonmail.com",
    "hey.com",
}


def create_empty_contact() -> dict[str, Any]:
    return {
        "name": None,
        "email": None,
        "sent_count": 0,
        "received_count": 0,
        "last_contact": None,
        "first_contact": None,
        "subjects": [],
        "company": None,
        "tags": [],
        "potential_contributor": False,
    }


class GmailCRM:
    def __init__(self):
        self.service = None
        self.contacts: dict[str, dict[str, Any]] = {}

    def authenticate(self):
        creds = None

        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Missing {CREDENTIALS_FILE}\n"
                        "Download OAuth credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("gmail", "v1", credentials=creds)
        print("✓ Authenticated with Gmail API")

    def is_noise(self, email: str) -> bool:
        email_lower = email.lower()
        for pattern in NOISE_PATTERNS:
            if re.search(pattern, email_lower):
                return True
        domain = email_lower.split("@")[-1] if "@" in email_lower else ""
        return domain in EXCLUDED_DOMAINS

    def extract_contacts(self, max_results: int = 5000) -> dict:
        print("\n📤 Extracting sent emails...")
        self._process_folder("in:sent", "sent", max_results)

        print("\n📥 Extracting received emails...")
        self._process_folder("in:inbox", "received", max_results)

        genuine = {}
        for email, data in self.contacts.items():
            total = data["sent_count"] + data["received_count"]
            bidirectional = data["sent_count"] > 0 and data["received_count"] > 0
            if bidirectional or total >= 2:
                self._infer_tags(data)
                genuine[email] = data

        print(
            f"\n✓ Found {len(genuine)} genuine contacts from {len(self.contacts)} total addresses"
        )
        return genuine

    def _process_folder(self, query: str, direction: str, max_results: int):
        messages = []
        next_page_token = None

        while len(messages) < max_results:
            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=min(500, max_results - len(messages)),
                    pageToken=next_page_token,
                )
                .execute()
            )

            messages.extend(results.get("messages", []))
            next_page_token = results.get("nextPageToken")

            if not next_page_token:
                break

            print(f"  Fetched {len(messages)} message IDs...")

        print(f"  Processing {len(messages)} {direction} messages...")

        for i, msg in enumerate(messages):
            if i % 200 == 0 and i > 0:
                print(f"  {i}/{len(messages)}...")
            try:
                self._process_message(msg["id"], direction)
            except Exception:
                continue

    def _process_message(self, message_id: str, direction: str):
        msg = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"],
            )
            .execute()
        )

        headers = {
            h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])
        }

        if direction == "sent":
            name, email = parseaddr(headers.get("To", ""))
        else:
            name, email = parseaddr(headers.get("From", ""))

        if not email:
            return

        email = email.lower()
        if self.is_noise(email):
            return

        if email not in self.contacts:
            self.contacts[email] = create_empty_contact()

        contact = self.contacts[email]
        contact["email"] = email

        if name and not contact["name"]:
            contact["name"] = name

        if direction == "sent":
            contact["sent_count"] += 1
        else:
            contact["received_count"] += 1

        try:
            msg_date = parsedate_to_datetime(headers.get("Date", ""))
            if contact["last_contact"] is None or msg_date > contact["last_contact"]:
                contact["last_contact"] = msg_date
            if contact["first_contact"] is None or msg_date < contact["first_contact"]:
                contact["first_contact"] = msg_date
        except Exception:
            pass

        subject = headers.get("Subject", "")
        if (
            subject
            and len(contact["subjects"]) < 5
            and subject not in contact["subjects"]
        ):
            contact["subjects"].append(subject)

        if not contact["company"] and "@" in email:
            domain = email.split("@")[1]
            if domain not in PERSONAL_DOMAINS:
                contact["company"] = domain.split(".")[0].title()

    def _infer_tags(self, contact: dict):
        tags = []
        subjects_text = " ".join(contact.get("subjects", [])).lower()

        contributor_signals = [
            "podcast",
            "guest",
            "article",
            "write",
            "contribute",
            "interview",
            "collaboration",
        ]
        if any(s in subjects_text for s in contributor_signals):
            contact["potential_contributor"] = True
            tags.append("potential-contributor")

        vendor_signals = [
            "invoice",
            "payment",
            "contract",
            "proposal",
            "quote",
            "pricing",
        ]
        if any(s in vendor_signals for s in subjects_text):
            tags.append("vendor")

        total = contact["sent_count"] + contact["received_count"]
        if total >= 10:
            tags.append("high-engagement")
        elif total >= 5:
            tags.append("engaged")

        last = contact.get("last_contact")
        if last:
            days_ago = (datetime.now(last.tzinfo) - last).days
            if days_ago <= 30:
                tags.append("recent")
            elif days_ago <= 90:
                tags.append("active")
            elif days_ago > 365:
                tags.append("dormant")

        contact["tags"] = tags


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:50]


def write_markdown_files(contacts: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Writing markdown files to {output_dir}")

    for email, data in contacts.items():
        name = data.get("name") or email.split("@")[0].replace(".", " ").title()
        filename = slugify(name) + ".md"
        filepath = output_dir / filename

        if filepath.exists():
            base = slugify(name)
            counter = 2
            while (output_dir / f"{base}-{counter}.md").exists():
                counter += 1
            filepath = output_dir / f"{base}-{counter}.md"

        last_contact = data.get("last_contact")
        first_contact = data.get("first_contact")
        last_str = last_contact.strftime("%Y-%m-%d") if last_contact else ""
        first_str = first_contact.strftime("%Y-%m-%d") if first_contact else ""

        tags_yaml = ", ".join(data.get("tags", []))
        subjects = data.get("subjects", [])

        content = f"""---
name: "{name}"
email: "{email}"
company: "{data.get("company") or ""}"
sent_count: {data.get("sent_count", 0)}
received_count: {data.get("received_count", 0)}
total_exchanges: {data.get("sent_count", 0) + data.get("received_count", 0)}
first_contact: {first_str}
last_contact: {last_str}
tags: [{tags_yaml}]
potential_contributor: {str(data.get("potential_contributor", False)).lower()}
type: contact
---

# {name}

**Email:** {email}
**Company:** {data.get("company") or "Personal"}
**Exchanges:** {data.get("sent_count", 0)} sent, {data.get("received_count", 0)} received

## Recent Subjects
{chr(10).join(f"- {s}" for s in subjects) if subjects else "_No subjects captured_"}

## Notes

_Add notes about this contact here._

## History

- First contact: {first_str or "Unknown"}
- Last contact: {last_str or "Unknown"}
"""

        filepath.write_text(content)

    print(f"✓ Created {len(contacts)} contact files")

    index_path = output_dir.parent / "_CRM Dashboard.md"
    index_content = f"""---
type: crm-dashboard
updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---

# CRM Dashboard

## Quick Stats
- **Total Contacts:** {len(contacts)}
- **Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Recent Contacts
```dataview
TABLE email, company, last_contact, total_exchanges
FROM "CRM/contacts"
WHERE type = "contact"
SORT last_contact DESC
LIMIT 20
```

## High Engagement
```dataview
TABLE email, company, total_exchanges
FROM "CRM/contacts"
WHERE contains(tags, "high-engagement") OR contains(tags, "engaged")
SORT total_exchanges DESC
```

## Potential Contributors
```dataview
TABLE email, company, last_contact
FROM "CRM/contacts"
WHERE potential_contributor = true
SORT last_contact DESC
```

## Dormant (1+ year)
```dataview
TABLE email, company, last_contact
FROM "CRM/contacts"
WHERE contains(tags, "dormant")
SORT last_contact DESC
LIMIT 20
```

## By Company
```dataview
TABLE WITHOUT ID company as Company, length(rows) as Contacts
FROM "CRM/contacts"
WHERE company != ""
GROUP BY company
SORT length(rows) DESC
LIMIT 15
```
"""
    index_path.write_text(index_content)
    print(f"✓ Created dashboard at {index_path}")


def main():
    parser = argparse.ArgumentParser(description="Gmail to Markdown CRM")
    parser.add_argument(
        "--extract", action="store_true", help="Extract and create markdown files"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5000,
        help="Max messages to process per folder",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory (default: OpenEd Vault/CRM/contacts)",
    )

    args = parser.parse_args()

    if args.extract:
        output_dir = Path(args.output) if args.output else CRM_OUTPUT_DIR

        crm = GmailCRM()
        crm.authenticate()
        contacts = crm.extract_contacts(max_results=args.max_results)
        write_markdown_files(contacts, output_dir)

        print("\n✅ Done! Open Obsidian to see your CRM.")
        print(f"   Dashboard: CRM/_CRM Dashboard.md")
        print(f"   Contacts:  CRM/contacts/")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
