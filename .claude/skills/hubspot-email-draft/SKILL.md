# HubSpot Email Draft Skill

Create ready-to-publish OpenEd Daily drafts in HubSpot from newsletter markdown.

---

## When to Use

After the newsletter draft is complete and ready for HubSpot. This is the **last step** in the content workflow:

1. Draft social media assets
2. Publish blog post on Webflow
3. Share social media with blog link
4. **Newsletter via this skill** ← You are here

---

## Input

A newsletter draft file with:
- **SUBJECT:** line
- **PREVIEW:** line
- Body content with H1 headers (# THOUGHT, # TOOL, # TREND)
- Dividers (---) between sections
- Sign-off: `– Charlie (the OpenEd newsletter guy)`

Example structure:
```markdown
# Newsletter Draft - 2026-01-27 (Monday)

**SUBJECT:** Why The Minimalists pulled their daughter out of school
**PREVIEW:** Joshua's daughter had stomach aches every morning...

---

Greetings Eddies!

Opening letter content here.

– Charlie (the OpenEd newsletter guy)

---

# THOUGHT: A JOB SHE'D DO FOR FREE

Thought content...

---

# TOOL: BEPRESENT

Tool content...

---

# TREND: WORD OF THE DAY

Trend content...

---

That's all for today!
```

---

## Process

1. Read the newsletter draft
2. Extract subject, preview, and body
3. Convert markdown to HTML:
   - `# HEADER` → `<h1>HEADER</h1>`
   - `---` → `<hr>`
   - `**bold**` → `<strong>`
   - `[link](url)` → `<a href="url">`
   - Paragraphs → `<p>` tags
4. Clone most recent OED email (keeps template + targeting)
5. Update name, subject, preview, body HTML
6. Return HubSpot edit link

---

## Run

```bash
cd "OpenEd Vault/Studio/SEO Content Production/seomachine"

python3 << 'PYEOF'
import requests
import re
import sys

TOKEN = "HUBSPOT_API_KEY_REDACTED"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def markdown_to_html(md):
    """Convert newsletter markdown to HubSpot HTML"""
    html = md

    # H1 headers (# THOUGHT: Title → <h1>THOUGHT: Title</h1>)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # H2 headers
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    # Dividers
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Paragraphs (double newlines)
    paragraphs = re.split(r'\n\n+', html)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h1>') or p.startswith('<h2>') or p.startswith('<hr'):
            html_parts.append(p)
        else:
            html_parts.append(f'<p>{p}</p>')

    return '\n'.join(html_parts)

def find_recent_oed_email():
    """Find most recent OED campaign to clone"""
    resp = requests.get(
        "https://api.hubapi.com/email/public/v1/campaigns",
        headers=headers,
        params={"limit": 100}
    )
    campaigns = resp.json().get('campaigns', [])

    for c in campaigns:
        detail = requests.get(
            f"https://api.hubapi.com/email/public/v1/campaigns/{c['id']}",
            headers=headers
        ).json()
        name = detail.get('name', '')
        if 'OED' in name or name.startswith('1.') or 'Daily' in name:
            return detail.get('contentId')
    return None

def create_draft(name, subject, preview, body_html):
    """Clone OED template and update with new content"""

    # Find template
    content_id = find_recent_oed_email()
    if not content_id:
        return None, "No OED email found to clone"

    # Clone
    clone_resp = requests.post(
        "https://api.hubapi.com/marketing/v3/emails/clone",
        headers=headers,
        json={"id": str(content_id)}
    )
    if clone_resp.status_code != 200:
        return None, f"Clone failed: {clone_resp.text}"

    clone_id = clone_resp.json()['id']

    # Update metadata
    requests.patch(
        f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
        headers=headers,
        json={"name": name, "subject": subject}
    )

    # Update content
    requests.patch(
        f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
        headers=headers,
        json={
            "content": {
                "widgets": {
                    "deep_dive_content": {"body": {"html": body_html}},
                    "preview_text": {"body": {"value": preview}}
                }
            }
        }
    )

    return clone_id, None

# Usage: Pass file path as argument or edit inline
# draft_path = sys.argv[1] if len(sys.argv) > 1 else "path/to/draft.md"
PYEOF
```

---

## Example Usage

```python
# After reading the draft file:
subject = "Why The Minimalists pulled their daughter out of school"
preview = "Joshua's daughter had stomach aches every morning..."
name = "1.27 OED - Scrolling Is The New Smoking"
body_md = """Greetings Eddies!

Opening content...

– Charlie (the OpenEd newsletter guy)

---

# THOUGHT: A JOB SHE'D DO FOR FREE

Content...
"""

body_html = markdown_to_html(body_md)
draft_id, error = create_draft(name, subject, preview, body_html)

if draft_id:
    print(f"✅ https://app.hubspot.com/email/{draft_id}/edit")
```

---

## Output

Returns HubSpot edit URL. Draft includes:
- ✅ Name (e.g., "1.27 OED - Scrolling Is The New Smoking")
- ✅ Subject line
- ✅ Preview text
- ✅ Full body HTML with H1 headers and dividers
- ✅ Template styling and targeting from most recent OED

**Manual step:** Click publish in HubSpot (requires `marketing-email` scope to automate).

---

## Formatting Notes

The **newsletter drafting skill** should output drafts with:
- H1 headers for THOUGHT, TOOL, TREND sections
- Dividers (---) between opening letter and first section
- Dividers between each section
- Sign-off: `– Charlie (the OpenEd newsletter guy)`

This skill converts that structure to HTML - it doesn't add formatting.

---

## API Reference

**Token:** `HUBSPOT_API_KEY_REDACTED`
**Portal:** 45961901

| Endpoint | Purpose |
|----------|---------|
| GET `/email/public/v1/campaigns` | Find OED emails to clone |
| POST `/marketing/v3/emails/clone` | Clone template |
| PATCH `/marketing/v3/emails/{id}` | Update content |

---

*Created: 2026-01-27*
