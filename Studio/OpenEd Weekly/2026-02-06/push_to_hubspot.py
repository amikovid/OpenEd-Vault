#!/usr/bin/env python3
"""Convert weekly newsletter markdown to HTML and push to HubSpot as draft."""

import requests
import re
import json
import copy
import os

# --- Config ---
TOKEN = os.environ.get("HUBSPOT_KEY")
PORTAL = "45961901"
SOURCE_EMAIL_ID = "206886611767"  # Gatto - Version C (known working)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# --- Style Constants (EXACT Gatto strings - do not modify) ---
FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"

P_STYLE = f"font-family: {FONT_STACK} !important; font-size: 18px !important; line-height: 1.65 !important; margin: 0 0 20px 0 !important; color: #333333 !important;"
H1_STYLE = f"font-family: {FONT_STACK} !important; font-weight: 700 !important; font-size: 32px !important; margin: 40px 0 20px 0 !important; text-align: center !important; color: #333333 !important; line-height: 1.25 !important;"
H2_STYLE = f"font-family: {FONT_STACK} !important; font-weight: 700 !important; font-size: 24px !important; margin: 32px 0 16px 0 !important; color: #333333 !important; line-height: 1.3 !important;"
LINK_STYLE = "color: #03a4ea !important; text-decoration: underline !important; font-size: inherit !important;"
HR_STYLE = "border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;"
IMG_STYLE = "width: 600px !important; height: auto !important; max-width: 100% !important; margin-left: auto; margin-right: auto; display: block;"


def markdown_to_html(md):
    """Convert newsletter markdown to HubSpot HTML with inline styles."""

    # Strip YAML frontmatter
    md = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.DOTALL)

    # Remove the top-level title (# OpenEd Weekly...) - it's in the subject line
    md = re.sub(r'^# OpenEd Weekly.*\n', '', md, flags=re.MULTILINE)

    # Convert images: ![](url) or ![alt](url)
    md = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        lambda m: f'<center><img src="{m.group(2)}" width="600" style="{IMG_STYLE}" align="center"></center>',
        md
    )

    # Convert H1 headers (wrap in strong) - all sections use H1 in weekly
    md = re.sub(
        r'^# (.+)$',
        lambda m: f'<h1 style="{H1_STYLE}"><strong>{m.group(1)}</strong></h1>',
        md, flags=re.MULTILINE
    )

    # Convert H2 headers (fallback, shouldn't be many in weekly)
    md = re.sub(
        r'^## (.+)$',
        lambda m: f'<h2 style="{H2_STYLE}">{m.group(1)}</h2>',
        md, flags=re.MULTILINE
    )

    # Convert dividers
    md = re.sub(
        r'^---+$',
        f'<hr style="{HR_STYLE}">',
        md, flags=re.MULTILINE
    )

    # Convert bold (before italic)
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)

    # Convert links
    md = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a href="{m.group(2)}" style="{LINK_STYLE}">{m.group(1)}</a>',
        md
    )

    # Convert italic (after bold and links to avoid false matches)
    md = re.sub(r'(?<![<\w/])\*([^*\n]+?)\*(?![>\w])', r'<em>\1</em>', md)

    # Split into paragraphs and wrap
    paragraphs = re.split(r'\n\n+', md)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # Skip block-level elements
        if any(p.startswith(tag) for tag in ['<h1', '<h2', '<hr', '<center']):
            html_parts.append(p)
        # Center CTA lines (paragraphs that are ONLY links with | separators)
        elif re.match(r'^(<a [^>]+>[^<]+</a>[\s|]*)+$', p.replace('\n', ' ')):
            html_parts.append(f'<p style="{P_STYLE} text-align: center !important;">{p}</p>')
        else:
            # Replace single newlines with <br> for line continuity within paragraphs
            p = p.replace('\n', '<br>')
            html_parts.append(f'<p style="{P_STYLE}">{p}</p>')

    # Leading newline is REQUIRED
    return '\n' + '\n'.join(html_parts)


def create_email_draft(name, subject, preview, body_html):
    """Clone Gatto email, preserve widget metadata, swap body HTML."""

    # Step 1: Clone
    print("Cloning source email...")
    clone_resp = requests.post(
        "https://api.hubapi.com/marketing/v3/emails/clone",
        headers=HEADERS,
        json={"id": SOURCE_EMAIL_ID}
    )
    if clone_resp.status_code != 200:
        print(f"Clone failed: {clone_resp.status_code} {clone_resp.text[:500]}")
        return None
    clone_data = clone_resp.json()
    clone_id = clone_data['id']
    print(f"Cloned to {clone_id}")

    # Step 2: GET the clone to extract full widget metadata
    print("Fetching widget metadata...")
    get_resp = requests.get(
        f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
        headers=HEADERS
    )
    if get_resp.status_code != 200:
        print(f"GET failed: {get_resp.status_code} {get_resp.text[:500]}")
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
        print("Updated deep_dive_content widget")

    # hs_email_body - preserve all fields INCLUDING deleted_at, replace body.html
    if 'hs_email_body' in widgets:
        heb = copy.deepcopy(widgets['hs_email_body'])
        heb['body']['html'] = body_html
        updated_widgets['hs_email_body'] = heb
        print(f"Updated hs_email_body widget (deleted_at: {heb.get('deleted_at', 'N/A')})")

    # preview_text
    if 'preview_text' in widgets:
        pt = copy.deepcopy(widgets['preview_text'])
        pt['body']['value'] = preview
        updated_widgets['preview_text'] = pt
        print("Updated preview_text widget")

    # Step 4: Single PATCH with name, subject, and content.widgets
    print("Patching email draft...")
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
        print(f"Response: {patch_resp.text[:1000]}")
        return None

    edit_url = f"https://app.hubspot.com/email/{PORTAL}/edit/{clone_id}"
    print(f"\nDraft created successfully!")
    print(f"Edit URL: {edit_url}")
    return clone_id


if __name__ == "__main__":
    # Read the newsletter draft
    with open("/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/Studio/OpenEd Weekly/2026-02-06/Weekly_Newsletter_COMBINED_DRAFT.md", "r") as f:
        md_content = f.read()

    # Convert to HTML
    body_html = markdown_to_html(md_content)

    # Save HTML for inspection
    html_path = "/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/Studio/OpenEd Weekly/2026-02-06/newsletter_preview.html"
    with open(html_path, "w") as f:
        f.write(f"<html><body style='max-width:600px;margin:0 auto;padding:20px;'>{body_html}</body></html>")
    print(f"HTML preview saved to {html_path}")

    # Push to HubSpot
    name = "2.6 OEW - Mason Ember + Gatto Weekly"
    subject = "A 16-year-old spent a year filming homeschoolers. Here's what he found."
    preview = "Plus: Gatto's hidden curriculum, the CHOICE framework, and voices from the community"

    draft_id = create_email_draft(name, subject, preview, body_html)

    if draft_id:
        print(f"\nOpen in HubSpot: https://app.hubspot.com/email/{PORTAL}/edit/{draft_id}")
