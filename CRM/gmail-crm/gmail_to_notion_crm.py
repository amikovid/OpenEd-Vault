#!/usr/bin/env python3
"""
Gmail to Notion CRM

Extracts genuine correspondences from Gmail (2+ exchanges) and syncs to Notion database.
Filters out newsletters, automated emails, and one-off inquiries.

Usage:
    python gmail_to_notion_crm.py --extract      # Extract contacts from Gmail
    python gmail_to_notion_crm.py --sync         # Sync to Notion
    python gmail_to_notion_crm.py --full         # Extract + Sync

Requirements:
    pip install google-auth-oauthlib google-api-python-client notion-client python-dotenv
"""

import os
import json
import pickle
import re
import argparse
from datetime import datetime
from collections import defaultdict
from email.utils import parseaddr
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from notion_client import Client as NotionClient

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Paths
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.pickle"
CONTACTS_FILE = SCRIPT_DIR / "extracted_contacts.json"

# Notion config
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_CRM_DATABASE_ID")

# Filtering patterns
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

# Domains to always exclude (transactional)
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


class GmailCRM:
    def __init__(self):
        self.service = None
        self.contacts = defaultdict(
            lambda: {
                "name": None,
                "email": None,
                "sent_count": 0,
                "received_count": 0,
                "last_contact": None,
                "first_contact": None,
                "subjects": [],
                "snippets": [],
                "company": None,
                "tags": [],
                "potential_contributor": False,
            }
        )

    def authenticate(self):
        """Authenticate with Gmail API."""
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
        print("Authenticated with Gmail API")

    def is_noise(self, email: str) -> bool:
        """Check if email is from automated/noise source."""
        email_lower = email.lower()

        for pattern in NOISE_PATTERNS:
            if re.search(pattern, email_lower):
                return True

        domain = email_lower.split("@")[-1] if "@" in email_lower else ""
        if domain in EXCLUDED_DOMAINS:
            return True

        return False

    def has_unsubscribe(self, message_id: str) -> bool:
        """Check if message has unsubscribe header or link."""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="metadata",
                    metadataHeaders=["List-Unsubscribe"],
                )
                .execute()
            )
            headers = msg.get("payload", {}).get("headers", [])
            for header in headers:
                if header.get("name", "").lower() == "list-unsubscribe":
                    return True
        except Exception:
            pass
        return False

    def extract_contacts(self, max_results: int = 5000):
        """Extract contacts from Gmail."""
        print("Extracting sent emails...")
        self._process_folder("in:sent", "sent", max_results)

        print("Extracting received emails...")
        self._process_folder("in:inbox", "received", max_results)

        genuine = {}
        for email, data in self.contacts.items():
            total_exchanges = data["sent_count"] + data["received_count"]
            has_bidirectional = data["sent_count"] > 0 and data["received_count"] > 0
            if has_bidirectional or total_exchanges >= 2:
                genuine[email] = data

        print(
            f"\nExtracted {len(genuine)} genuine contacts from {len(self.contacts)} total addresses"
        )

        with open(CONTACTS_FILE, "w") as f:
            json.dump(genuine, f, indent=2, default=str)

        print(f"Saved to {CONTACTS_FILE}")
        return genuine

    def _process_folder(self, query: str, direction: str, max_results: int):
        """Process emails from a folder/query."""
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
            if i % 100 == 0:
                print(f"  Processing {i}/{len(messages)}...")

            try:
                self._process_message(msg["id"], direction)
            except Exception as e:
                continue

    def _process_message(self, message_id: str, direction: str):
        """Process a single message."""
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
            to_header = headers.get("To", "")
            name, email = parseaddr(to_header)
        else:
            from_header = headers.get("From", "")
            name, email = parseaddr(from_header)

        if not email:
            return

        email = email.lower()

        if self.is_noise(email):
            return

        contact = self.contacts[email]
        contact["email"] = email

        if name and not contact["name"]:
            contact["name"] = name

        if direction == "sent":
            contact["sent_count"] += 1
        else:
            contact["received_count"] += 1

        date_str = headers.get("Date", "")
        try:
            from email.utils import parsedate_to_datetime

            msg_date = parsedate_to_datetime(date_str)
        except Exception:
            msg_date = None

        if msg_date:
            if contact["last_contact"] is None or msg_date > contact["last_contact"]:
                contact["last_contact"] = msg_date
            if contact["first_contact"] is None or msg_date < contact["first_contact"]:
                contact["first_contact"] = msg_date

        subject = headers.get("Subject", "")
        if subject and len(contact["subjects"]) < 5:
            if subject not in contact["subjects"]:
                contact["subjects"].append(subject)

        if not contact["company"] and "@" in email:
            domain = email.split("@")[1]
            personal_domains = {
                "gmail.com",
                "yahoo.com",
                "hotmail.com",
                "outlook.com",
                "icloud.com",
                "me.com",
                "aol.com",
            }
            if domain not in personal_domains:
                contact["company"] = domain.split(".")[0].title()

    def infer_tags(self, contact: dict) -> list:
        """Infer tags based on email patterns and subjects."""
        tags = []
        email = contact.get("email", "").lower()
        subjects = " ".join(contact.get("subjects", [])).lower()

        contributor_signals = [
            "podcast",
            "guest",
            "article",
            "write",
            "contribute",
            "interview",
            "collaboration",
        ]
        if any(signal in subjects for signal in contributor_signals):
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
        if any(signal in subjects for signal in vendor_signals):
            tags.append("vendor")

        total = contact.get("sent_count", 0) + contact.get("received_count", 0)
        if total >= 10:
            tags.append("high-engagement")

        last = contact.get("last_contact")
        if last:
            if isinstance(last, str):
                last = datetime.fromisoformat(last.replace("Z", "+00:00"))
            days_ago = (datetime.now(last.tzinfo) - last).days
            if days_ago <= 30:
                tags.append("recent")
            elif days_ago > 365:
                tags.append("dormant")

        return tags


class NotionSync:
    def __init__(self):
        if not NOTION_TOKEN:
            raise ValueError("NOTION_TOKEN not set in environment")
        self.client = NotionClient(auth=NOTION_TOKEN)

    def create_database(self, parent_page_id: str) -> str:
        """Create CRM database in Notion."""
        database = self.client.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Gmail CRM"}}],
            properties={
                "Name": {"title": {}},
                "Email": {"email": {}},
                "Company": {"rich_text": {}},
                "Last Contact": {"date": {}},
                "First Contact": {"date": {}},
                "Sent Count": {"number": {}},
                "Received Count": {"number": {}},
                "Total Exchanges": {
                    "formula": {
                        "expression": 'prop("Sent Count") + prop("Received Count")'
                    }
                },
                "Tags": {
                    "multi_select": {
                        "options": [
                            {"name": "potential-contributor", "color": "green"},
                            {"name": "vendor", "color": "orange"},
                            {"name": "high-engagement", "color": "blue"},
                            {"name": "recent", "color": "purple"},
                            {"name": "dormant", "color": "gray"},
                            {"name": "collaborator", "color": "pink"},
                            {"name": "prospect", "color": "yellow"},
                            {"name": "guest", "color": "red"},
                        ]
                    }
                },
                "Potential Contributor": {"checkbox": {}},
                "Notes": {"rich_text": {}},
                "Recent Subjects": {"rich_text": {}},
            },
        )

        database_id = database["id"]
        print(f"Created Notion database: {database_id}")
        return database_id

    def sync_contacts(self, contacts: dict, database_id: str = None):
        """Sync contacts to Notion database."""
        db_id = database_id or NOTION_DATABASE_ID
        if not db_id:
            raise ValueError(
                "No database ID provided. Set NOTION_CRM_DATABASE_ID or pass database_id."
            )

        existing = self._get_existing_emails(db_id)

        crm = GmailCRM()

        synced = 0
        updated = 0

        for email, data in contacts.items():
            tags = crm.infer_tags(data)
            data["tags"] = tags

            if email in existing:
                self._update_contact(existing[email], data)
                updated += 1
            else:
                self._create_contact(db_id, data)
                synced += 1

            if (synced + updated) % 50 == 0:
                print(f"  Progress: {synced} created, {updated} updated...")

        print(f"\nSync complete: {synced} new contacts, {updated} updated")

    def _get_existing_emails(self, database_id: str) -> dict:
        """Get existing emails from Notion database."""
        existing = {}
        has_more = True
        start_cursor = None

        while has_more:
            response = self.client.databases.query(
                database_id=database_id, start_cursor=start_cursor
            )

            for page in response.get("results", []):
                email_prop = page.get("properties", {}).get("Email", {})
                email = email_prop.get("email")
                if email:
                    existing[email.lower()] = page["id"]

            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

        return existing

    def _create_contact(self, database_id: str, data: dict):
        """Create a new contact in Notion."""
        properties = self._build_properties(data)

        self.client.pages.create(
            parent={"database_id": database_id}, properties=properties
        )

    def _update_contact(self, page_id: str, data: dict):
        """Update existing contact in Notion."""
        properties = self._build_properties(data)

        self.client.pages.update(page_id=page_id, properties=properties)

    def _build_properties(self, data: dict) -> dict:
        """Build Notion properties from contact data."""
        props = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": data.get("name") or data.get("email", "Unknown")
                        }
                    }
                ]
            },
            "Email": {"email": data.get("email")},
            "Sent Count": {"number": data.get("sent_count", 0)},
            "Received Count": {"number": data.get("received_count", 0)},
            "Potential Contributor": {
                "checkbox": data.get("potential_contributor", False)
            },
        }

        if data.get("company"):
            props["Company"] = {"rich_text": [{"text": {"content": data["company"]}}]}

        if data.get("last_contact"):
            last = data["last_contact"]
            if hasattr(last, "isoformat"):
                last = last.isoformat()
            props["Last Contact"] = {"date": {"start": last[:10]}}

        if data.get("first_contact"):
            first = data["first_contact"]
            if hasattr(first, "isoformat"):
                first = first.isoformat()
            props["First Contact"] = {"date": {"start": first[:10]}}

        if data.get("tags"):
            props["Tags"] = {"multi_select": [{"name": tag} for tag in data["tags"]]}

        if data.get("subjects"):
            subjects_text = " | ".join(data["subjects"][:5])
            if len(subjects_text) > 2000:
                subjects_text = subjects_text[:2000] + "..."
            props["Recent Subjects"] = {
                "rich_text": [{"text": {"content": subjects_text}}]
            }

        return props


def main():
    parser = argparse.ArgumentParser(description="Gmail to Notion CRM")
    parser.add_argument(
        "--extract", action="store_true", help="Extract contacts from Gmail"
    )
    parser.add_argument("--sync", action="store_true", help="Sync contacts to Notion")
    parser.add_argument(
        "--full", action="store_true", help="Full pipeline: extract + sync"
    )
    parser.add_argument(
        "--create-db", type=str, help="Create Notion database under this page ID"
    )
    parser.add_argument(
        "--max-results", type=int, default=5000, help="Max messages to process"
    )

    args = parser.parse_args()

    if args.create_db:
        notion = NotionSync()
        db_id = notion.create_database(args.create_db)
        print(f"\nAdd this to your .env file:")
        print(f"NOTION_CRM_DATABASE_ID={db_id}")
        return

    if args.extract or args.full:
        crm = GmailCRM()
        crm.authenticate()
        contacts = crm.extract_contacts(max_results=args.max_results)

    if args.sync or args.full:
        if not (args.extract or args.full):
            if not CONTACTS_FILE.exists():
                print(f"No contacts file found. Run with --extract first.")
                return
            with open(CONTACTS_FILE) as f:
                contacts = json.load(f)

        notion = NotionSync()
        notion.sync_contacts(contacts)

    if not any([args.extract, args.sync, args.full, args.create_db]):
        parser.print_help()


if __name__ == "__main__":
    main()
