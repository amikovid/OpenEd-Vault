# HubSpot Email Draft Skill

Create ready-to-publish OpenEd Daily drafts in HubSpot from newsletter markdown.

---

## Working Approach: Clone-and-Swap

The proven pattern is to clone the working Gatto email and swap in new body HTML while preserving all widget metadata.

**Steps:**
1. Clone the Gatto source email (ID: `206886611767`)
2. GET the clone to extract full widget metadata (`module_id`, `type`, `order`, `label`, `css`, `styles`, `child_css`, `smart_type`)
3. Replace ONLY `body.html` in both `deep_dive_content` AND `hs_email_body` widgets
4. Preserve `deleted_at` on `hs_email_body`
5. PATCH with `name`, `subject`, and `content.widgets` in a single call

---

## Critical Style Rules

These are the EXACT style strings from the working Gatto email. Any deviation (extra CSS properties, different font sizes, `!important` on image margins) triggers HubSpot's CSS processor and breaks font sizing.

### Paragraph Style

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif !important; font-size: 18px !important; line-height: 1.65 !important; margin: 0 0 20px 0 !important; color: #333333 !important;
```

### Link Style (ONLY 3 properties - no font-family or line-height inherit)

```
color: #03a4ea !important; text-decoration: underline !important; font-size: inherit !important;
```

### H1 Style (wrap text in `<strong>` tag)

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif !important; font-weight: 700 !important; font-size: 32px !important; margin: 40px 0 20px 0 !important; text-align: center !important; color: #333333 !important; line-height: 1.25 !important;
```

Usage: `<h1 style="..."><strong>Title</strong></h1>`

### H2 Style

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif !important; font-weight: 700 !important; font-size: 24px !important; margin: 32px 0 16px 0 !important; color: #333333 !important; line-height: 1.3 !important;
```

### HR Style

```
border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;
```

### Image Style (max-width: 100% NOT 600px, NO !important on margin/display)

```
width: 600px !important; height: auto !important; max-width: 100% !important; margin-left: auto; margin-right: auto; display: block;
```

Image HTML format:
```html
<center><a href="{blog_post_url}"><img src="{image_url}" width="600" height="338" style="width: 600px !important; height: auto !important; max-width: 100% !important; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>
```

---

## NEVER DO

- Use `font-size: 16px` or any non-18px size on paragraphs (breaks HubSpot's CSS processor)
- Add extra properties on links beyond `color`, `text-decoration`, `font-size`
- Use `!important` on image `margin-left`, `margin-right`, or `display`
- Use a separate "byline" or "CTA" style - use standard paragraph style with `<em>` wrapper
- Omit the leading newline before the first `<p>` tag (HTML must start with `\n<p` not `<p`)
- Omit `<strong>` wrapper inside `<h1>`
- Send partial widget data - always preserve ALL metadata fields from the GET response

---

## When to Use

After the newsletter draft is complete and ready for HubSpot. This is the **last step** in the content workflow:

1. Draft social media assets
2. Publish blog post on Webflow
3. Share social media with blog link
4. **Newsletter via this skill**

---

## Input

A newsletter draft file with:
- **SUBJECT:** line
- **PREVIEW:** line
- Body content with H1 headers (# THOUGHT, # TOOL, # TREND)
- Dividers (---) between sections
- Sign-off: `-- Charlie (the OpenEd newsletter guy)`

---

## Complete Python Script

```python
import requests
import re
import json
import copy

# --- Config ---
TOKEN = os.environ.get("HUBSPOT_KEY")  # seomachine config .env token (has email scopes)
PORTAL = "45961901"
SOURCE_EMAIL_ID = "206886611767"  # Gatto - Version C (known working)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# --- Style Constants ---
FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"

P_STYLE = f"font-family: {FONT_STACK} !important; font-size: 18px !important; line-height: 1.65 !important; margin: 0 0 20px 0 !important; color: #333333 !important;"
H1_STYLE = f"font-family: {FONT_STACK} !important; font-weight: 700 !important; font-size: 32px !important; margin: 40px 0 20px 0 !important; text-align: center !important; color: #333333 !important; line-height: 1.25 !important;"
H2_STYLE = f"font-family: {FONT_STACK} !important; font-weight: 700 !important; font-size: 24px !important; margin: 32px 0 16px 0 !important; color: #333333 !important; line-height: 1.3 !important;"
LINK_STYLE = "color: #03a4ea !important; text-decoration: underline !important; font-size: inherit !important;"
HR_STYLE = "border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;"
IMG_STYLE = "width: 600px !important; height: auto !important; max-width: 100% !important; margin-left: auto; margin-right: auto; display: block;"


def markdown_to_html(md):
    """Convert newsletter markdown to HubSpot HTML with inline styles.

    CRITICAL: Uses exact Gatto style strings. Any deviation breaks mobile rendering.
    Output MUST start with a leading newline before the first <p> tag.
    """
    html = md

    # H1 headers - wrap text in <strong>
    html = re.sub(
        r'^# (.+)$',
        f'<h1 style="{H1_STYLE}"><strong>\\1</strong></h1>',
        html, flags=re.MULTILINE
    )

    # H2 headers
    html = re.sub(
        r'^## (.+)$',
        f'<h2 style="{H2_STYLE}">\\1</h2>',
        html, flags=re.MULTILINE
    )

    # Dividers
    html = re.sub(
        r'^---+$',
        f'<hr style="{HR_STYLE}">',
        html, flags=re.MULTILINE
    )

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links - ONLY 3 properties
    html = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        f'<a href="\\2" style="{LINK_STYLE}">\\1</a>',
        html
    )

    # Paragraphs (split on double newlines)
    paragraphs = re.split(r'\n\n+', html)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h1') or p.startswith('<h2') or p.startswith('<hr') or p.startswith('<center'):
            html_parts.append(p)
        else:
            html_parts.append(f'<p style="{P_STYLE}">{p}</p>')

    # Leading newline is REQUIRED
    return '\n' + '\n'.join(html_parts)


def create_email_draft(name, subject, preview, body_html):
    """Clone Gatto email, preserve widget metadata, swap body HTML.

    Steps:
    1. Clone source email
    2. GET the clone to extract full widget metadata
    3. Replace ONLY body.html in both widgets
    4. Preserve deleted_at on hs_email_body
    5. PATCH with name, subject, and content.widgets
    """

    # Step 1: Clone
    clone_resp = requests.post(
        "https://api.hubapi.com/marketing/v3/emails/clone",
        headers=HEADERS,
        json={"id": SOURCE_EMAIL_ID}
    )
    if clone_resp.status_code != 200:
        print(f"Clone failed: {clone_resp.status_code} {clone_resp.text}")
        return None
    clone_data = clone_resp.json()
    clone_id = clone_data['id']
    print(f"Cloned to {clone_id}")

    # Step 2: GET the clone to extract full widget metadata
    get_resp = requests.get(
        f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
        headers=HEADERS
    )
    if get_resp.status_code != 200:
        print(f"GET failed: {get_resp.status_code} {get_resp.text}")
        return None
    email_data = get_resp.json()
    widgets = email_data.get('content', {}).get('widgets', {})

    # Step 3: Build updated widgets preserving ALL metadata
    updated_widgets = {}

    # deep_dive_content - preserve all fields, replace body.html
    if 'deep_dive_content' in widgets:
        ddc = copy.deepcopy(widgets['deep_dive_content'])
        ddc['body']['html'] = body_html
        updated_widgets['deep_dive_content'] = ddc

    # hs_email_body - preserve all fields INCLUDING deleted_at, replace body.html
    if 'hs_email_body' in widgets:
        heb = copy.deepcopy(widgets['hs_email_body'])
        heb['body']['html'] = body_html
        # deleted_at MUST be preserved
        updated_widgets['hs_email_body'] = heb

    # preview_text
    if 'preview_text' in widgets:
        pt = copy.deepcopy(widgets['preview_text'])
        pt['body']['value'] = preview
        updated_widgets['preview_text'] = pt

    # Step 5: Single PATCH with name, subject, and content.widgets
    patch_resp = requests.patch(
        f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
        headers=HEADERS,
        json={
            "name": name,
            "subject": subject,
            "content": {
                "widgets": updated_widgets
            }
        }
    )

    if patch_resp.status_code != 200:
        print(f"PATCH failed: {patch_resp.status_code}")
        print(f"Response: {patch_resp.text[:500]}")
        return None

    edit_url = f"https://app.hubspot.com/email/{PORTAL}/edit/{clone_id}"
    print(f"Draft created: {edit_url}")
    return clone_id


# --- Usage Example ---
if __name__ == "__main__":
    # 1. Read your newsletter draft and extract fields
    subject = "Why The Minimalists pulled their daughter out of school"
    preview = "Joshua's daughter had stomach aches every morning..."
    name = "2.6 OED - Why The Minimalists Pulled Their Daughter"

    body_md = """Greetings Eddies!

Opening content here.

-- Charlie (the OpenEd newsletter guy)

---

# THOUGHT: A JOB SHE'D DO FOR FREE

Thought content here with a [link](https://example.com) inline.

---

# TOOL: BEPRESENT

Tool content here.

---

# TREND: WORD OF THE DAY

Trend content here.

---

That's all for today!
"""

    # 2. Convert and create
    body_html = markdown_to_html(body_md)
    draft_id = create_email_draft(name, subject, preview, body_html)

    if draft_id:
        print(f"Edit: https://app.hubspot.com/email/{PORTAL}/edit/{draft_id}")
```

---

## API Reference

**Token:** Use key from `Studio/SEO Content Production/seomachine/data_sources/config/.env` (has email scopes)
**Note:** The root `.env` token does NOT have email scopes - use the seomachine config token.
**Portal:** 45961901
**Source email:** 206886611767 (Gatto - Version C)

| Endpoint | Purpose |
|----------|---------|
| POST `/marketing/v3/emails/clone` | Clone Gatto source email |
| GET `/marketing/v3/emails/{id}` | Extract widget metadata from clone |
| PATCH `/marketing/v3/emails/{id}` | Update name, subject, and widgets |
| POST `/filemanager/api/v3/files/upload` | Upload images |

---

## Formatting Rules (Weekly Newsletter)

### Images Above Titles
Thumbnail images ALWAYS go ABOVE the H1 section title. This is critical for the weekly format.

### H1 for Section Headers
Weekly newsletter sections (Featured Podcast, Deep Dive, Trends, Tools, etc.) use H1 (`#`), not H2 (`##`).

### Opening Letter Has No Header
The opening letter has no `## OPENING LETTER` header or divider before it. It starts right after the frontmatter.

### Source Attribution
Source goes in italics right after the link text: `[**Headline**](url) *(Source)* - Description`

## Uploading Thumbnail Images

Upload to HubSpot File Manager and place ABOVE the H1 title in the content.

```python
upload_url = "https://api.hubapi.com/filemanager/api/v3/files/upload"

with open(image_path, 'rb') as f:
    files = {'file': ('thumbnail.png', f, 'image/png')}
    data = {
        'folderPath': '/newsletters/2026-02',
        'options': '{"access": "PUBLIC_INDEXABLE"}'
    }
    auth_headers = {"Authorization": f"Bearer {TOKEN}"}

    resp = requests.post(upload_url, headers=auth_headers, files=files, data=data)
    file_url = resp.json().get('objects', [{}])[0].get('url', '')
```

Insert the image HTML after the opening letter divider and before the H1 title:

```html
<hr style="border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;">

<center><a href="{blog_post_url}"><img src="{file_url}" width="600" height="338" style="width: 600px !important; height: auto !important; max-width: 100% !important; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>

<h1 style="..."><strong>Article Title</strong></h1>
```

Folder convention: `/newsletters/YYYY-MM/`

---

## Output

Returns HubSpot edit URL. Draft includes:
- Name (e.g., "2.6 OED - Why The Minimalists Pulled Their Daughter")
- Subject line
- Preview text
- Full body HTML with correct styles
- Template styling and targeting from Gatto source

**Manual step:** Click publish in HubSpot (requires `marketing-email` scope to automate).

---

*Created: 2026-01-27*
*Updated: 2026-02-05 - Rewritten with proven clone-and-swap approach from Gatto email*
