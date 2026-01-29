#!/usr/bin/env python3
"""
Fix Webflow posts:
1. Remove metadata from body content
2. Fix table conversion
3. Fix em dashes
4. Update slugs from /compare/ to /blog/
"""

import os
import re
import requests
from pathlib import Path

# Load API key
ENV_PATH = Path(__file__).parent.parent.parent / ".env"
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("WEBFLOW_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break

POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
BASE_PATH = Path(__file__).parent

# Posts to fix
POSTS = [
    {
        "post_id": "697bbf1e05a9f64dbf85e913",
        "name": "Waldorf vs Montessori: A Parent's Guide",
        "slug": "waldorf-vs-montessori",  # Already correct
        "draft_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Waldorf vs Montessori/DRAFT_v1.md",
    },
    {
        "post_id": "697bbf1fc80c845945e64a37",
        "name": "Montessori vs Reggio Emilia: What Parents Should Know",
        "slug": "montessori-vs-reggio-emilia",  # Already correct
        "draft_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Montessori vs Reggio Emilia/DRAFT_v1.md",
    },
    {
        "post_id": "697bbf203c348338e9a993e7",
        "name": "Khan Academy vs IXL: Honest Comparison for Homeschool Math",
        "slug": "khan-academy-vs-ixl",  # Change from compare to blog
        "draft_path": BASE_PATH / "Versus/khan-academy-vs-ixl/draft-v1.md",
    },
    {
        "post_id": "697bbf213a058d27011d1027",
        "name": "Saxon Math vs Math-U-See: Which Is Right for Your Family?",
        "slug": "saxon-math-vs-math-u-see",  # Change from compare to blog
        "draft_path": BASE_PATH / "Versus/saxon-vs-math-u-see/draft-v1.md",
    },
    {
        "post_id": "697bbf23681286546825ecdc",
        "name": "IXL vs Exact Path: What OpenEd Teachers Actually Recommend",
        "slug": "ixl-vs-exact-path",  # Change from compare to blog
        "draft_path": BASE_PATH / "Versus/ixl-vs-exact-path/draft-v2.md",
    },
]


def convert_inline(text):
    """Convert inline markdown to HTML. Links first, then bold/italic."""
    # Replace em dashes with spaced hyphens
    text = text.replace('—', ' - ')
    text = text.replace('–', ' - ')

    # Links first (so **[link](url)** works)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)

    return text


def convert_table(block):
    """Convert markdown table to HTML table."""
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return ''

    html = '<table>'

    for i, line in enumerate(lines):
        # Skip separator line (contains ---)
        if re.match(r'^[\|\s\-:]+$', line):
            continue

        # Split cells, removing empty first/last from leading/trailing |
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]  # Remove empty strings

        if not cells:
            continue

        # First row is header
        tag = 'th' if i == 0 else 'td'
        row_html = ''.join(f'<{tag}>{convert_inline(c)}</{tag}>' for c in cells)
        html += f'<tr>{row_html}</tr>'

    html += '</table>'
    return html


def is_metadata_line(line):
    """Check if line is metadata that should be stripped."""
    line = line.strip()
    patterns = [
        r'^\*\*Meta Title:\*\*',
        r'^\*\*Meta Description:\*\*',
        r'^\*\*URL:\*\*',
        r'^\*Meta Title:',
        r'^\*Meta Description:',
        r'^\*URL:',
        r'^Meta Title:',
        r'^Meta Description:',
        r'^URL:',
        r'^\*Word count:',
        r'^Word count:',
    ]
    for pattern in patterns:
        if re.match(pattern, line, re.IGNORECASE):
            return True
    return False


def convert_block(block):
    """Convert a markdown block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip metadata lines
    if is_metadata_line(block):
        return ''

    # Skip blocks that are just metadata
    lines = block.split('\n')
    if all(is_metadata_line(l) or not l.strip() for l in lines):
        return ''

    # Headers - skip H1 (becomes name field)
    if block.startswith('# ') and not block.startswith('## '):
        return ''
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:])}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:])}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:])}</h2>'

    # Horizontal rule - skip
    if block == '---':
        return ''

    # Table detection - has | and multiple rows
    if '|' in block and block.count('\n') >= 1 and block.count('|') > 3:
        return convert_table(block)

    # Unordered list
    if block.startswith('- '):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Ordered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            match = re.match(r'^\d+\.\s*(.+)', line.strip())
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        return '<ol>' + ''.join(items) + '</ol>'

    # Blockquote
    if block.startswith('>'):
        quote_lines = []
        for line in block.split('\n'):
            if line.startswith('>'):
                quote_lines.append(line[1:].strip())
            else:
                quote_lines.append(line.strip())
        quote_text = ' '.join(quote_lines)
        return f'<blockquote>{convert_inline(quote_text)}</blockquote>'

    # Regular paragraph - join lines
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'


def markdown_to_html(content):
    """Convert full markdown to clean HTML."""
    # Replace em dashes globally first
    content = content.replace('—', ' - ')
    content = content.replace('–', ' - ')

    # Remove title line (H1)
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        content = '\n'.join(lines[1:])

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)

    # Convert each block
    html_blocks = []
    for block in blocks:
        converted = convert_block(block)
        if converted:
            html_blocks.append(converted)

    return '\n\n'.join(html_blocks)


def update_post(post_id, slug, html_content):
    """Update an existing Webflow post."""
    resp = requests.patch(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items/{post_id}",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "fieldData": {
                "slug": slug,
                "content": html_content
            }
        }
    )
    return resp


def main():
    print("=" * 60)
    print("Fixing Webflow Posts")
    print("=" * 60)
    print("\nIssues being fixed:")
    print("  - Remove metadata from body (Meta Title, Description, URL)")
    print("  - Fix table conversion")
    print("  - Replace em dashes with spaced hyphens")
    print("  - Slugs already correct (/blog/ prefix in Webflow)")
    print()

    for post in POSTS:
        print(f"\n{post['name']}")
        print("-" * 40)

        if not post["draft_path"].exists():
            print(f"  ERROR: Draft not found")
            continue

        # Read and convert
        with open(post["draft_path"], 'r') as f:
            markdown = f.read()

        html = markdown_to_html(markdown)

        # Quick validation
        if '**Meta Title:**' in html or 'Meta Title:' in html:
            print("  WARNING: Metadata may still be in content")
        if '—' in html:
            print("  WARNING: Em dash may still be in content")

        print(f"  HTML length: {len(html)} chars")

        # Update post
        print(f"  Updating post...")
        resp = update_post(post["post_id"], post["slug"], html)

        if resp.status_code in [200, 201, 202]:
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED: {resp.status_code}")
            print(f"  {resp.text[:300]}")

    print("\n" + "=" * 60)
    print("Done! Review posts in Webflow CMS.")


if __name__ == "__main__":
    main()
