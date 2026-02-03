# HubSpot Email Draft Skill

Create ready-to-publish OpenEd Daily drafts in HubSpot from newsletter markdown.

---

## CRITICAL: Image Format

**Images MUST use this exact HTML format or they will render as broken links:**

```html
<center><a href="{blog_post_url}"><img src="{image_url}" width="600" height="338" style="width: 600px; height: auto; max-width: 600px; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>
```

**Required elements:**
- `<center>` wrapper tags
- `<a href>` wrapper linking to the blog post (makes image clickable)
- Explicit `width` and `height` attributes
- `align="center"` attribute
- Full inline styles

**DO NOT use:** Simple `<img>` tags or markdown `![alt](url)` syntax - these will NOT render.

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
    """Convert newsletter markdown to HubSpot HTML with inline styles"""
    html = md

    # Inline style definitions
    FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    P_STYLE = f"font-family: {FONT_STACK}; font-size: 18px; line-height: 1.65; margin: 0 0 20px 0; color: #333333;"
    H1_STYLE = f"font-family: {FONT_STACK}; font-weight: 700; font-size: 32px; margin: 40px 0 20px 0; text-align: center; color: #333333; line-height: 1.25;"
    H2_STYLE = f"font-family: {FONT_STACK}; font-weight: 600; font-size: 26px; margin: 32px 0 12px 0; text-align: center; color: #333333; line-height: 1.3;"
    LINK_STYLE = "color: #03a4ea !important; text-decoration: underline; font-size: 18px; font-family: inherit; line-height: inherit;"

    # H1 headers (# THOUGHT: Title → <h1 style="...">THOUGHT: Title</h1>)
    html = re.sub(r'^# (.+)$', f'<h1 style="{H1_STYLE}">\\1</h1>', html, flags=re.MULTILINE)

    # H2 headers
    html = re.sub(r'^## (.+)$', f'<h2 style="{H2_STYLE}">\\1</h2>', html, flags=re.MULTILINE)

    # Dividers
    html = re.sub(r'^---+$', '<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links - add inline styles
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', f'<a href="\\2" style="{LINK_STYLE}">\\1</a>', html)

    # Paragraphs (double newlines)
    paragraphs = re.split(r'\n\n+', html)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h1') or p.startswith('<h2') or p.startswith('<hr'):
            html_parts.append(p)
        else:
            html_parts.append(f'<p style="{P_STYLE}">{p}</p>')

    return '\n'.join(html_parts)

def find_recent_oed_email():
    """Find most recent OED newsletter (BATCH_EMAIL type) to clone.

    IMPORTANT: Must find actual newsletters, not automated emails like 'OpenEd Daily Opt In'.
    Look for emails matching pattern: '1.29 OED', '2.3 OED', etc. (date prefix + OED)
    """
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
        email_type = detail.get('type', '')

        # Must be BATCH_EMAIL (not AUTOMATED_EMAIL) and match OED naming pattern
        # Pattern: "1.29 OED - Title" or "2.3 OED - Title" (month.day OED)
        is_batch = email_type == 'BATCH_EMAIL'
        is_oed_newsletter = ' OED ' in name or ' OED -' in name or ' OEW ' in name

        if is_batch and is_oed_newsletter:
            print(f"Found: {name} (type: {email_type})")
            return detail.get('contentId')

    print("WARNING: No OED newsletter found. Searched for BATCH_EMAIL with 'OED' in name.")
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

    # Update content - MUST include BOTH widgets in same call
    # deep_dive_content = main body HTML
    # preview_text = email preview/preheader text
    content_resp = requests.patch(
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

    if content_resp.status_code != 200:
        print(f"WARNING: Content update returned {content_resp.status_code}")
        print(f"Response: {content_resp.text[:500]}")

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

**Token:** Use key from `Studio/SEO Content Production/seomachine/data_sources/config/.env` (has email scopes)
**Note:** The root `.env` token does NOT have email scopes - use the seomachine config token.
**Portal:** 45961901

| Endpoint | Purpose |
|----------|---------|
| GET `/email/public/v1/campaigns` | Find OED emails to clone |
| POST `/marketing/v3/emails/clone` | Clone template |
| PATCH `/marketing/v3/emails/{id}` | Update content |
| POST `/filemanager/api/v3/files/upload` | Upload images |

---

## Uploading Thumbnail Images

**IMPORTANT:** Thumbnails must be uploaded to HubSpot File Manager and placed ABOVE the H1 title in the content.

### Step 1: Upload to File Manager

```python
upload_url = "https://api.hubapi.com/filemanager/api/v3/files/upload"

with open(image_path, 'rb') as f:
    files = {'file': ('thumbnail.png', f, 'image/png')}
    data = {
        'folderPath': '/newsletters/2026-01',
        'options': '{"access": "PUBLIC_INDEXABLE"}'
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}

    resp = requests.post(upload_url, headers=headers, files=files, data=data)
    file_url = resp.json().get('objects', [{}])[0].get('url', '')
```

### Step 2: Place in Content

Insert the image HTML **after the opening letter divider** and **before the H1 title**.

**IMPORTANT:** Use `<center>` wrapper, `<a href>` link wrapper, and explicit `width`/`height` attributes - this is the format that works in HubSpot emails:

```html
<hr>

<center><a href="{blog_post_url}"><img src="{file_url}" width="600" height="338" style="width: 600px; height: auto; max-width: 600px; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>

<h1>Article Title</h1>
```

**Key format requirements:**
- Wrap in `<center>` tags
- Wrap `<img>` in `<a href>` linking to the blog post (makes thumbnail clickable)
- Include explicit `width` and `height` attributes
- Use `align="center"` attribute
- Full inline styles for margin and display

### Folder Convention

Use `/newsletters/YYYY-MM/` for organization (e.g., `/newsletters/2026-01/`).

---

*Created: 2026-01-27*
*Updated: 2026-01-29 - Added thumbnail upload workflow*
