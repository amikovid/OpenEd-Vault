#!/usr/bin/env python3
"""
OpenEd Lead Magnet PDF Generator

Converts markdown files to branded PDFs using WeasyPrint.

Usage:
    python generate_pdf.py input.md output.pdf
    python generate_pdf.py input.md  # outputs to input.pdf
"""

import sys
import re
import markdown
from pathlib import Path
from weasyprint import HTML, CSS

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "template.html"


def extract_title_and_subtitle(md_content: str) -> tuple[str, str, str]:
    """Extract title (H1) and subtitle (italic line after) from markdown."""
    lines = md_content.strip().split('\n')
    title = "OpenEd Guide"
    subtitle = ""
    content_start = 0

    for i, line in enumerate(lines):
        # Find the first H1
        if line.startswith('# ') and not title.startswith('OpenEd'):
            title = line[2:].strip()
            content_start = i + 1

            # Check if next non-empty line is italic (subtitle)
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('*') and next_line.endswith('*') and not next_line.startswith('**'):
                    subtitle = next_line.strip('*').strip()
                    content_start = j + 1
                    break
                elif next_line and not next_line.startswith('---'):
                    break
            break

    # Remove the title and subtitle from content
    remaining_content = '\n'.join(lines[content_start:])

    # Clean up leading horizontal rules
    remaining_content = re.sub(r'^---+\s*\n', '', remaining_content.strip())

    return title, subtitle, remaining_content


def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    extensions = [
        'tables',
        'fenced_code',
        'nl2br',
    ]

    html = markdown.markdown(md_content, extensions=extensions)
    return html


def create_cover_page(title: str, subtitle: str) -> str:
    """Create the cover page HTML."""
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ''

    return f'''
    <div class="cover">
        <h1>{title}</h1>
        {subtitle_html}
        <div class="logo">
            <div class="logo-text">OpenEd</div>
            <div class="tagline">Design education that works for your family</div>
        </div>
    </div>
    '''


def process_content(html_content: str) -> str:
    """Post-process the HTML content for better PDF rendering."""

    # Wrap "What they're really asking/saying" in a styled span
    html_content = re.sub(
        r'<strong>What they\'re really (asking|saying):</strong>',
        r'<h4>What they\'re really \1:</h4>',
        html_content
    )

    # Style "Script:" labels
    html_content = re.sub(
        r'<strong>Script:</strong>',
        r'<h4>Script:</h4>',
        html_content
    )

    # Style "If they push back:" labels
    html_content = re.sub(
        r'<strong>If they push back:</strong>',
        r'<h4>If they push back:</h4>',
        html_content
    )

    # Style "Shorter version:" labels
    html_content = re.sub(
        r'<strong>Shorter version:</strong>',
        r'<h4>Shorter version:</h4>',
        html_content
    )

    # Style "Why this works:" labels
    html_content = re.sub(
        r'<strong>Why this works:</strong>',
        r'<h4>Why this works:</h4>',
        html_content
    )

    return html_content


def generate_pdf(input_path: str, output_path: str = None):
    """Generate a branded PDF from a markdown file."""

    input_file = Path(input_path)

    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path)

    # Read the markdown
    md_content = input_file.read_text(encoding='utf-8')

    # Extract title and subtitle
    title, subtitle, content = extract_title_and_subtitle(md_content)

    # Convert content to HTML
    content_html = markdown_to_html(content)
    content_html = process_content(content_html)

    # Create cover page
    cover_html = create_cover_page(title, subtitle)

    # Combine cover and content
    full_content = cover_html + content_html

    # Read template
    template = TEMPLATE_PATH.read_text(encoding='utf-8')

    # Fill in template
    final_html = template.replace('{{TITLE}}', title)
    final_html = final_html.replace('{{CONTENT}}', full_content)

    # Generate PDF
    HTML(string=final_html).write_pdf(str(output_path))

    print(f"Generated: {output_path}")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf.py input.md [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    generate_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
