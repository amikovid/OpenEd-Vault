# Gmail to Notion CRM

Extracts genuine correspondences from Gmail and syncs to a Notion database.

## What It Does

1. **Extracts** all email addresses from your Sent and Inbox folders
2. **Filters** out noise (newsletters, noreply, transactional emails)
3. **Identifies** genuine contacts (2+ exchanges OR bidirectional communication)
4. **Infers** tags based on email patterns and subjects
5. **Syncs** to Notion with full metadata

## Filtering Logic

**Excluded automatically:**
- `noreply@`, `no-reply@`, `notifications@`, `newsletter@`
- Major transactional domains (Amazon, PayPal, banks, streaming services)
- Emails with `List-Unsubscribe` headers
- Substack, GitHub notifications, social media emails

**Included if:**
- You've sent AND received from the address, OR
- Total exchanges >= 2

## Setup

### 1. Google Cloud (Gmail API)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create project → Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download JSON → save as `credentials.json` in this folder

### 2. Notion Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create new integration
3. Copy the token to `.env`:
   ```
   NOTION_TOKEN=secret_xxx
   ```
4. Share a Notion page with your integration (click Share → Add integration)

### 3. Install Dependencies

```bash
cd agents/gmail-crm
pip install -r requirements.txt
```

### 4. Create Notion Database

```bash
# Get the page ID from the page URL (the 32-char ID after the page name)
python gmail_to_notion_crm.py --create-db YOUR_PAGE_ID
```

Add the resulting database ID to `.env`.

## Usage

```bash
# Extract contacts from Gmail (first run opens browser for auth)
python gmail_to_notion_crm.py --extract

# Sync extracted contacts to Notion
python gmail_to_notion_crm.py --sync

# Full pipeline
python gmail_to_notion_crm.py --full

# Limit messages processed (default 5000)
python gmail_to_notion_crm.py --full --max-results 1000
```

## Notion Database Fields

| Field | Type | Description |
|-------|------|-------------|
| Name | Title | Contact name (or email if no name) |
| Email | Email | Email address |
| Company | Text | Inferred from domain |
| Last Contact | Date | Most recent email |
| First Contact | Date | Earliest email |
| Sent Count | Number | Emails you sent to them |
| Received Count | Number | Emails you received from them |
| Total Exchanges | Formula | Sent + Received |
| Tags | Multi-select | Auto-inferred tags |
| Potential Contributor | Checkbox | Signals for content collaboration |
| Notes | Text | Manual notes (preserved on sync) |
| Recent Subjects | Text | Last 5 subject lines for context |

## Auto-Inferred Tags

- `potential-contributor` - Email subjects mention podcast, guest, article, write, interview
- `vendor` - Subjects mention invoice, payment, contract, proposal
- `high-engagement` - 10+ total exchanges
- `recent` - Contact within last 30 days
- `dormant` - No contact in over a year

## Re-running

The script is idempotent:
- New contacts are created
- Existing contacts (by email) are updated
- Manual edits to Notes field are preserved
