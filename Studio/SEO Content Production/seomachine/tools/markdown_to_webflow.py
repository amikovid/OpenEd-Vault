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
- Images with Webflow figure wrapper (smart loading, dimensions, alt text validation)
- Blockquotes
- Horizontal rules

SEO features:
- First image gets loading="eager" fetchpriority="high" (LCP optimization)
- Remaining images get loading="lazy"
- Width/height attributes on <img> tags (CLS prevention)
- Alt text warnings when empty
- Meta description validation helper

Usage:
    from markdown_to_webflow import markdown_to_html, validate_meta_description

    html = markdown_to_html(markdown_content, image_meta={"hero.jpg": {"width": 1200, "height": 675}})
"""

import re
import sys
import json
from pathlib import Path


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


# Module-level counter for tracking image position within a conversion
_image_counter = 0


def _reset_image_counter():
    """Reset the image counter at the start of each document conversion."""
    global _image_counter
    _image_counter = 0


def convert_image(alt, src, cdn_lookup=None, image_meta=None):
    """
    Convert markdown image to Webflow figure with SEO attributes.

    Args:
        alt: Alt text for the image
        src: Source path or filename
        cdn_lookup: Optional dict mapping filenames to CDN URLs
        image_meta: Optional dict mapping filenames to {width, height} or
                    paths to .meta.json sidecar data

    Returns:
        HTML figure element or empty string if CDN URL not found
    """
    global _image_counter

    cdn_url = src
    if cdn_lookup:
        cdn_url = cdn_lookup.get(src, src)
        if not cdn_url:
            return ""

    # Warn on empty alt text
    if not alt or not alt.strip():
        print(f"  WARNING: Empty alt text for image: {src}", file=sys.stderr)

    # Smart loading: first image eager (LCP), rest lazy
    if _image_counter == 0:
        loading_attrs = 'loading="eager" fetchpriority="high"'
    else:
        loading_attrs = 'loading="lazy"'
    _image_counter += 1

    # Dimension attributes from image_meta
    dim_attrs = ""
    if image_meta:
        meta = image_meta.get(src, {})
        # Support both flat {width, height} and sidecar-style {dimensions: {width, height}}
        if 'dimensions' in meta:
            w = meta['dimensions'].get('width')
            h = meta['dimensions'].get('height')
        else:
            w = meta.get('width')
            h = meta.get('height')
        # Also check webp_dimensions (from optimizer)
        if not w and 'webp_dimensions' in meta:
            w = meta['webp_dimensions'].get('width')
            h = meta['webp_dimensions'].get('height')
        if w and h:
            dim_attrs = f' width="{w}" height="{h}"'

    return f'''<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="{cdn_url}" alt="{alt}" {loading_attrs}{dim_attrs}>
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


def convert_block(block, cdn_lookup=None, image_meta=None):
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
        return convert_image(img_match.group(1), img_match.group(2), cdn_lookup, image_meta)

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


def markdown_to_html(content, skip_title=True, cdn_lookup=None, image_meta=None):
    """
    Convert full markdown content to Webflow HTML.

    Args:
        content: Markdown string
        skip_title: If True, removes the first H1 (it becomes the post title field)
        cdn_lookup: Optional dict mapping image filenames to CDN URLs
        image_meta: Optional dict mapping image filenames to dimension/sidecar data.
                    Each value can be {width, height} or full sidecar JSON.

    Returns:
        HTML string ready for Webflow rich text field
    """
    _reset_image_counter()

    lines = content.split('\n')

    # Remove title if requested
    if skip_title and lines and lines[0].startswith('# '):
        content = '\n'.join(lines[1:])

    # Split by blank lines (paragraph boundaries)
    blocks = re.split(r'\n\s*\n', content)

    # Convert each block
    html_blocks = [convert_block(b, cdn_lookup, image_meta) for b in blocks]

    # Filter empty blocks and join
    html = '\n\n'.join(b for b in html_blocks if b)

    return html


def validate_meta_description(summary, keyword=None):
    """
    Validate a meta description for SEO best practices.

    Args:
        summary: The meta description text
        keyword: Optional target keyword to check for

    Returns:
        Tuple of (is_valid: bool, messages: list[str])
    """
    messages = []
    is_valid = True

    if not summary or not summary.strip():
        return False, ["Meta description is empty"]

    length = len(summary)
    if length < 120:
        messages.append(f"Too short ({length} chars, aim for 120-160)")
        is_valid = False
    elif length > 160:
        messages.append(f"Too long ({length} chars, aim for 120-160, will be truncated)")
        is_valid = False
    else:
        messages.append(f"Good length ({length} chars)")

    if keyword:
        if keyword.lower() in summary.lower():
            messages.append(f"Contains keyword '{keyword}'")
        else:
            messages.append(f"Missing keyword '{keyword}'")
            is_valid = False

    return is_valid, messages


def load_image_meta_from_sidecars(image_dir):
    """
    Load all .meta.json sidecars from a directory into an image_meta dict.

    Args:
        image_dir: Path to directory containing images and their .meta.json files

    Returns:
        Dict mapping image filenames to their sidecar metadata
    """
    image_dir = Path(image_dir)
    meta = {}
    for sidecar in image_dir.glob('*.meta.json'):
        image_stem = sidecar.stem  # e.g. "hero-gen" from "hero-gen.meta.json"
        with open(sidecar, 'r') as f:
            data = json.load(f)
        # Map both the original image name and webp name
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            meta[image_stem + ext] = data
        if 'webp_path' in data:
            meta[data['webp_path']] = data
    return meta


# Convenience function for common use case
def convert_article(markdown_path, output_path=None, cdn_lookup=None, image_meta=None):
    """
    Convert a markdown file to HTML.

    Args:
        markdown_path: Path to markdown file
        output_path: Optional path for HTML output (defaults to same name with .html)
        cdn_lookup: Optional dict mapping image filenames to CDN URLs
        image_meta: Optional dict mapping image filenames to dimension data

    Returns:
        HTML string
    """
    with open(markdown_path, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown, cdn_lookup=cdn_lookup, image_meta=image_meta)

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
