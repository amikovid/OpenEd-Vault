#!/usr/bin/env python3
"""
Markdown to Webflow HTML Converter

Shared utility for converting markdown content to Webflow-compatible HTML.
Handles common patterns including:
- Headers (H1-H4)
- Bold/italic text
- Links (processed before bold so **[link](url)** works)
- Unordered and ordered lists
- Bold headers followed by lists (e.g., **Grant Programs:** followed by bullet points)
- Images with Webflow figure wrapper
- Blockquotes
- Horizontal rules

Usage:
    from markdown_to_webflow import markdown_to_html

    html = markdown_to_html(markdown_content)
"""

import re


def convert_inline(text):
    """
    Convert inline markdown to HTML.

    Order matters: Links FIRST, then bold/italic.
    This ensures **[link](url)** works correctly.
    """
    # Links first
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (* or _)
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    # Clean up escaped characters
    text = text.replace(r'\-', '-')
    return text


def convert_image(alt, src, cdn_lookup=None):
    """
    Convert markdown image to Webflow figure.

    Args:
        alt: Alt text for the image
        src: Source path or filename
        cdn_lookup: Optional dict mapping filenames to CDN URLs

    Returns:
        HTML figure element or empty string if CDN URL not found
    """
    cdn_url = src
    if cdn_lookup:
        cdn_url = cdn_lookup.get(src, src)
        if not cdn_url:
            return ""

    return f'''<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="{cdn_url}" alt="{alt}" loading="lazy">
  </div>
</figure>'''


def convert_list_items(lines, list_type='ul'):
    """
    Convert list item lines to HTML list.

    Args:
        lines: List of strings, each starting with '- ' or 'N. '
        list_type: 'ul' for unordered, 'ol' for ordered

    Returns:
        HTML list element
    """
    items = []
    for line in lines:
        line = line.strip()
        if list_type == 'ul' and line.startswith('- '):
            items.append(f'<li>{convert_inline(line[2:])}</li>')
        elif list_type == 'ol' and re.match(r'^\d+\.', line):
            content = re.sub(r'^\d+\.\s*', '', line)
            items.append(f'<li>{convert_inline(content)}</li>')

    if not items:
        return ''

    return f'<{list_type}>' + ''.join(items) + f'</{list_type}>'


def convert_block(block, cdn_lookup=None):
    """
    Convert a single paragraph block to HTML.

    Handles the special case of bold headers followed by list items:
    **Header:**
    - Item 1
    - Item 2

    This becomes: <p><strong>Header:</strong></p><ul>...</ul>
    """
    block = block.strip()
    if not block:
        return ''

    lines = block.split('\n')

    # Skip metadata blocks
    if block.startswith('**Meta Title:**') or block.startswith('**Meta Description:**') or block.startswith('**URL:**'):
        return ''

    # Images
    img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', block)
    if img_match:
        return convert_image(img_match.group(1), img_match.group(2), cdn_lookup)

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

    # Pure unordered list (all lines start with '- ')
    if all(line.strip().startswith('- ') for line in lines if line.strip()):
        return convert_list_items(lines, 'ul')

    # Pure ordered list (all lines start with 'N. ')
    if all(re.match(r'^\d+\.', line.strip()) for line in lines if line.strip()):
        return convert_list_items(lines, 'ol')

    # SPECIAL CASE: Bold header followed by list items
    # Pattern: **Header:**\n- item1\n- item2
    if lines[0].strip().startswith('**') and lines[0].strip().endswith(':'):
        header_line = lines[0].strip()
        remaining_lines = [l for l in lines[1:] if l.strip()]

        # Check if remaining lines are list items
        if remaining_lines and all(l.strip().startswith('- ') for l in remaining_lines):
            header_html = f'<p>{convert_inline(header_line)}</p>'
            list_html = convert_list_items(remaining_lines, 'ul')
            return header_html + '\n' + list_html
        elif remaining_lines and all(re.match(r'^\d+\.', l.strip()) for l in remaining_lines):
            header_html = f'<p>{convert_inline(header_line)}</p>'
            list_html = convert_list_items(remaining_lines, 'ol')
            return header_html + '\n' + list_html

    # SPECIAL CASE: Bold header followed by list items (colon inside bold)
    # Pattern: **Header:**\n- item1\n- item2
    bold_header_match = re.match(r'^\*\*[^*]+\*\*:?\s*$', lines[0].strip())
    if bold_header_match:
        remaining_lines = [l for l in lines[1:] if l.strip()]

        if remaining_lines and all(l.strip().startswith('- ') for l in remaining_lines):
            header_html = f'<p>{convert_inline(lines[0].strip())}</p>'
            list_html = convert_list_items(remaining_lines, 'ul')
            return header_html + '\n' + list_html

    # Blockquote
    if block.startswith('>'):
        quote_text = '\n'.join(line.lstrip('> ').strip() for line in lines)
        return f'<blockquote>{convert_inline(quote_text)}</blockquote>'

    # Strikethrough
    block = re.sub(r'~~(.+?)~~', r'<s>\1</s>', block)

    # Regular paragraph - join lines with space
    text = ' '.join(line.strip() for line in lines)
    return f'<p>{convert_inline(text)}</p>'


def markdown_to_html(content, skip_title=True, cdn_lookup=None):
    """
    Convert full markdown content to Webflow HTML.

    Args:
        content: Markdown string
        skip_title: If True, removes the first H1 (it becomes the post title field)
        cdn_lookup: Optional dict mapping image filenames to CDN URLs

    Returns:
        HTML string ready for Webflow rich text field
    """
    lines = content.split('\n')

    # Remove title if requested
    if skip_title and lines and lines[0].startswith('# '):
        content = '\n'.join(lines[1:])

    # Split by blank lines (paragraph boundaries)
    blocks = re.split(r'\n\s*\n', content)

    # Convert each block
    html_blocks = [convert_block(b, cdn_lookup) for b in blocks]

    # Filter empty blocks and join
    html = '\n\n'.join(b for b in html_blocks if b)

    return html


# Convenience function for common use case
def convert_article(markdown_path, output_path=None, cdn_lookup=None):
    """
    Convert a markdown file to HTML.

    Args:
        markdown_path: Path to markdown file
        output_path: Optional path for HTML output (defaults to same name with .html)
        cdn_lookup: Optional dict mapping image filenames to CDN URLs

    Returns:
        HTML string
    """
    with open(markdown_path, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown, cdn_lookup=cdn_lookup)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"Converted {len(markdown)} chars to {len(html)} chars HTML")
        print(f"Output saved to {output_path}")

    return html


if __name__ == '__main__':
    # Test with a sample
    test_md = """# Test Article

This is an intro paragraph with **bold** and *italic* text.

## Section One

Here's a [link](https://example.com) and some more text.

**Grant Programs:**
- HSLDA Curriculum Grants
- State-specific homeschool grants
- Special needs learning grants

**Community Resources:**
- Library services (free printing, educational platform access)
- Museum homeschool programs
- Community center educational spaces

## Section Two

1. First item
2. Second item
3. Third item

Regular paragraph to end.
"""

    html = markdown_to_html(test_md)
    print("=== Converted HTML ===")
    print(html)
