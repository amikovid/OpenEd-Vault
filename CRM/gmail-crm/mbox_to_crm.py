#!/usr/bin/env python3
"""
MBOX to Markdown CRM

Parses Google Takeout MBOX files and creates Obsidian-compatible
markdown contact files with YAML frontmatter.

Usage:
    python mbox_to_crm.py --mbox-dir "/path/to/Mail" --output "/path/to/CRM/contacts"
"""

import mailbox
import re
import argparse
from datetime import datetime
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from collections import defaultdict
from typing import Any
import sys


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
    r"@bounce\.",
    r"mailer-daemon@",
    r"postmaster@",
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
    "youtube.com",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "tiktok.com",
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
    "live.com",
    "msn.com",
    "ymail.com",
    "rocketmail.com",
}


def is_noise(email: str) -> bool:
    email_lower = email.lower()
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, email_lower):
            return True
    domain = email_lower.split("@")[-1] if "@" in email_lower else ""
    return domain in EXCLUDED_DOMAINS


def parse_mbox(mbox_path: Path, direction: str, contacts: dict) -> int:
    """Parse an MBOX file and update contacts dict."""
    print(f"  Opening {mbox_path.name}...")

    try:
        mbox = mailbox.mbox(str(mbox_path))
    except Exception as e:
        print(f"  Error opening {mbox_path}: {e}")
        return 0

    count = 0
    total = len(mbox)

    for i, message in enumerate(mbox):
        if i % 1000 == 0 and i > 0:
            print(f"  Processed {i}/{total} messages...")

        try:
            if direction == "sent":
                header = message.get("To", "") or message.get("to", "")
            else:
                header = message.get("From", "") or message.get("from", "")

            if not header:
                continue

            # Handle multiple recipients
            for addr_part in header.split(","):
                name, email = parseaddr(addr_part.strip())

                if not email or "@" not in email:
                    continue

                email = email.lower().strip()

                if is_noise(email):
                    continue

                if email not in contacts:
                    contacts[email] = {
                        "name": None,
                        "email": email,
                        "sent_count": 0,
                        "received_count": 0,
                        "last_contact": None,
                        "first_contact": None,
                        "subjects": [],
                        "company": None,
                        "tags": [],
                        "potential_contributor": False,
                    }

                contact = contacts[email]

                if name and not contact["name"]:
                    # Clean up name
                    name = name.strip().strip('"').strip("'")
                    if name and name.lower() != email.split("@")[0]:
                        contact["name"] = name

                if direction == "sent":
                    contact["sent_count"] += 1
                else:
                    contact["received_count"] += 1

                # Parse date
                date_str = message.get("Date", "") or message.get("date", "")
                if date_str:
                    try:
                        msg_date = parsedate_to_datetime(date_str)
                        if (
                            contact["last_contact"] is None
                            or msg_date > contact["last_contact"]
                        ):
                            contact["last_contact"] = msg_date
                        if (
                            contact["first_contact"] is None
                            or msg_date < contact["first_contact"]
                        ):
                            contact["first_contact"] = msg_date
                    except Exception:
                        pass

                # Get subject
                subject = message.get("Subject", "") or message.get("subject", "")
                if subject and len(contact["subjects"]) < 5:
                    # Decode subject if needed
                    if isinstance(subject, bytes):
                        subject = subject.decode("utf-8", errors="ignore")
                    subject = subject.strip()
                    if subject and subject not in contact["subjects"]:
                        contact["subjects"].append(subject[:100])  # Limit length

                # Infer company from domain
                if not contact["company"] and "@" in email:
                    domain = email.split("@")[1]
                    if domain not in PERSONAL_DOMAINS:
                        contact["company"] = domain.split(".")[0].title()

                count += 1

        except Exception as e:
            continue

    mbox.close()
    return count


def infer_tags(contact: dict) -> list:
    """Infer tags based on patterns."""
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
        "speaking",
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
        "subscription",
    ]
    if any(s in subjects_text for s in vendor_signals):
        tags.append("vendor")

    total = contact["sent_count"] + contact["received_count"]
    if total >= 20:
        tags.append("high-engagement")
    elif total >= 10:
        tags.append("engaged")
    elif total >= 5:
        tags.append("familiar")

    last = contact.get("last_contact")
    if last:
        try:
            now = datetime.now(last.tzinfo) if last.tzinfo else datetime.now()
            days_ago = (now - last).days
            if days_ago <= 30:
                tags.append("recent")
            elif days_ago <= 90:
                tags.append("active")
            elif days_ago > 365:
                tags.append("dormant")
        except Exception:
            pass

    return tags


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:50]


def write_markdown_files(contacts: dict, output_dir: Path):
    """Write contact markdown files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Writing markdown files to {output_dir}")

    written = 0
    for email, data in contacts.items():
        name = (
            data.get("name")
            or email.split("@")[0].replace(".", " ").replace("_", " ").title()
        )
        filename = slugify(name) + ".md"
        filepath = output_dir / filename

        # Handle duplicates
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

        tags = data.get("tags", [])
        tags_yaml = ", ".join(tags) if tags else ""
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
        written += 1

    print(f"✓ Created {written} contact files")

    # Create dashboard
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
LIMIT 25
```

## High Engagement (20+ exchanges)
```dataview
TABLE email, company, total_exchanges
FROM "CRM/contacts"
WHERE total_exchanges >= 20
SORT total_exchanges DESC
```

## Potential Contributors
```dataview
TABLE email, company, last_contact
FROM "CRM/contacts"
WHERE potential_contributor = true
SORT last_contact DESC
```

## By Company
```dataview
TABLE WITHOUT ID company as Company, length(rows) as Contacts
FROM "CRM/contacts"
WHERE company != ""
GROUP BY company
SORT length(rows) DESC
LIMIT 20
```

## Dormant (1+ year)
```dataview
TABLE email, last_contact, total_exchanges
FROM "CRM/contacts"
WHERE contains(tags, "dormant")
SORT total_exchanges DESC
LIMIT 25
```
"""
    index_path.write_text(index_content)
    print(f"✓ Created dashboard at {index_path.name}")


def main():
    parser = argparse.ArgumentParser(description="MBOX to Markdown CRM")
    parser.add_argument(
        "--mbox-dir", type=str, required=True, help="Directory containing .mbox files"
    )
    parser.add_argument(
        "--output", type=str, help="Output directory for markdown files"
    )
    parser.add_argument(
        "--min-exchanges",
        type=int,
        default=2,
        help="Minimum exchanges to include (default: 2)",
    )

    args = parser.parse_args()

    mbox_dir = Path(args.mbox_dir)
    if not mbox_dir.exists():
        print(f"Error: {mbox_dir} does not exist")
        sys.exit(1)

    output_dir = (
        Path(args.output)
        if args.output
        else mbox_dir.parent.parent / "CRM" / "contacts"
    )

    contacts: dict[str, dict[str, Any]] = {}

    print("\n📧 Parsing MBOX files...")

    # Process Sent first (most valuable)
    sent_path = mbox_dir / "Sent.mbox"
    if sent_path.exists():
        print(f"\n📤 Processing Sent.mbox (this may take a while for large files)...")
        n = parse_mbox(sent_path, "sent", contacts)
        print(f"  ✓ Extracted {n} email addresses from sent messages")

    # Process Inbox
    inbox_path = mbox_dir / "Inbox.mbox"
    if inbox_path.exists():
        print(f"\n📥 Processing Inbox.mbox...")
        n = parse_mbox(inbox_path, "received", contacts)
        print(f"  ✓ Extracted {n} email addresses from received messages")

    # Process any other mbox files
    for mbox_file in mbox_dir.glob("*.mbox"):
        if mbox_file.name not in ["Sent.mbox", "Inbox.mbox"]:
            print(f"\n📁 Processing {mbox_file.name}...")
            n = parse_mbox(mbox_file, "received", contacts)
            print(f"  ✓ Extracted {n} email addresses")

    # Filter to genuine contacts
    print(f"\n🔍 Filtering contacts (min {args.min_exchanges} exchanges)...")
    genuine = {}
    for email, data in contacts.items():
        total = data["sent_count"] + data["received_count"]
        bidirectional = data["sent_count"] > 0 and data["received_count"] > 0

        if total >= args.min_exchanges or bidirectional:
            data["tags"] = infer_tags(data)
            genuine[email] = data

    print(f"✓ {len(genuine)} genuine contacts from {len(contacts)} total addresses")

    # Write markdown files
    write_markdown_files(genuine, output_dir)

    print(f"\n✅ Done!")
    print(f"   Dashboard: {output_dir.parent / '_CRM Dashboard.md'}")
    print(f"   Contacts:  {output_dir}/")


if __name__ == "__main__":
    main()
