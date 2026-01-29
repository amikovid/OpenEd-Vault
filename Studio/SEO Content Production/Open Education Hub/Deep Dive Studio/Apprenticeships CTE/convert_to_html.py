#!/usr/bin/env python3
"""Convert the CTE article markdown to Webflow HTML."""

import re
import json

# CDN URLs for uploaded images
IMAGES = {
    "header-first-dollar-workbench_20260122_143420_pro.png": "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6973b9d445a4dbfea6362bca_apprenticeship-first-dollar-workbench.png",
    # V3 infographic replaces the old watercolor version
    "infographic-opportunity-gap-watercolor_20260122_152949_pro.png": "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6973d1cbdf6b466efb03be85_apprenticeship-opportunity-gap-v3.png",
    "cartoon-unpaid-internship_20260122_143420_pro.png": "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6973ba00007f3144632add1d_apprenticeship-unpaid-internship-cartoon.png",
    # This one isn't uploaded yet - skip it for now
    "infographic_talent_doing_networks_1769119660738.png": None
}

def convert_inline(text):
    """Convert inline markdown to HTML - LINKS FIRST, then bold/italic."""
    # Links FIRST (so **[link](url)** works)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Then bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Then italic (including _text_)
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    # Clean up escaped characters
    text = text.replace(r'\-', '-')
    return text

def convert_image(match):
    """Convert markdown image to Webflow figure."""
    alt = match.group(1)
    src = match.group(2)

    # Look up the CDN URL
    cdn_url = IMAGES.get(src)
    if not cdn_url:
        # Skip images we don't have
        return ""

    return f'''<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="{cdn_url}" alt="{alt}" loading="lazy">
  </div>
</figure>'''

def convert_block(block):
    """Convert a single paragraph block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip metadata at the end
    if block.startswith('**Meta Title:**') or block.startswith('**Meta Description:**') or block.startswith('**URL:**'):
        return ''

    # Images
    img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', block)
    if img_match:
        return convert_image(img_match)

    # Headers
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:])}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:])}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:])}</h2>'
    elif block.startswith('# '):
        return f'<h1>{convert_inline(block[2:])}</h1>'

    # Horizontal rule
    if block == '---':
        return '<hr>'

    # Unordered list
    if block.startswith('- '):
        items = []
        for line in block.split('\n'):
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Blockquote
    if block.startswith('>'):
        return f'<blockquote>{convert_inline(block[1:].strip())}</blockquote>'

    # Strikethrough
    block = re.sub(r'~~(.+?)~~', r'<s>\1</s>', block)

    # Regular paragraph - JOIN LINES WITH SPACE
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'

def markdown_to_html(content):
    """Convert full markdown content to HTML."""
    # Remove the title (first line with #)
    lines = content.split('\n')
    if lines[0].startswith('# '):
        content = '\n'.join(lines[1:])

    # Split by blank lines (paragraph boundaries)
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    html = '\n\n'.join(b for b in html_blocks if b)

    return html

if __name__ == '__main__':
    # Read the markdown file
    with open('DRAFTv6.md', 'r') as f:
        markdown = f.read()

    # Convert to HTML
    html = markdown_to_html(markdown)

    # Write HTML output
    with open('content.html', 'w') as f:
        f.write(html)

    print(f"Converted {len(markdown)} chars markdown to {len(html)} chars HTML")
    print("Output saved to content.html")

    # Also output JSON-escaped version for the API call
    escaped = json.dumps(html)
    with open('content_escaped.json', 'w') as f:
        f.write(escaped)

    print("JSON-escaped version saved to content_escaped.json")
