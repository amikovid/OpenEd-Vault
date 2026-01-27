#!/usr/bin/env python3
"""
OpenEd Lead Magnet PDF Generator (Playwright version)

Converts markdown files to branded PDFs using Playwright headless browser.

Usage:
    python generate_pdf_playwright.py input.md output.pdf
    python generate_pdf_playwright.py input.md  # outputs to input.pdf
"""

import asyncio
import re
import sys
from pathlib import Path

import markdown

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "template.html"


def extract_title_and_subtitle(md_content: str) -> tuple:
    lines = md_content.strip().split("\n")
    title = "OpenEd Guide"
    subtitle = ""
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("# ") and title == "OpenEd Guide":
            title = line[2:].strip()
            content_start = i + 1

            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j].strip()
                if (
                    next_line.startswith("*")
                    and next_line.endswith("*")
                    and not next_line.startswith("**")
                ):
                    subtitle = next_line.strip("*").strip()
                    content_start = j + 1
                    break
                elif next_line and not next_line.startswith("---"):
                    break
            break

    remaining_content = "\n".join(lines[content_start:])
    remaining_content = re.sub(r"^---+\s*\n", "", remaining_content.strip())

    return title, subtitle, remaining_content


def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    extensions = ["tables", "fenced_code", "nl2br"]
    html = markdown.markdown(md_content, extensions=extensions)
    return html


def create_cover_page(title: str, subtitle: str) -> str:
    """Create the cover page HTML."""
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""

    return f"""
    <div class="cover">
        <h1>{title}</h1>
        {subtitle_html}
        <div class="logo">
            <div class="logo-text">OpenEd</div>
            <div class="tagline">Design education that works for your family</div>
        </div>
    </div>
    """


def process_content(html_content: str) -> str:
    """Post-process the HTML content for better PDF rendering."""
    # Style special labels
    patterns = [
        (
            r"<strong>What they\'re really (asking|saying):</strong>",
            r"<h4>What they\'re really \1:</h4>",
        ),
        (r"<strong>Script:</strong>", r"<h4>Script:</h4>"),
        (r"<strong>If they push back:</strong>", r"<h4>If they push back:</h4>"),
        (r"<strong>Shorter version:</strong>", r"<h4>Shorter version:</h4>"),
        (r"<strong>Why this works:</strong>", r"<h4>Why this works:</h4>"),
        (r"<strong>Physical environment:</strong>", r"<h4>Physical environment:</h4>"),
        (r"<strong>Daily rhythms:</strong>", r"<h4>Daily rhythms:</h4>"),
        (r"<strong>This week:</strong>", r"<h4>This week:</h4>"),
        (r"<strong>This month:</strong>", r"<h4>This month:</h4>"),
        (r"<strong>Ongoing:</strong>", r"<h4>Ongoing:</h4>"),
    ]

    for pattern, replacement in patterns:
        html_content = re.sub(pattern, replacement, html_content)

    return html_content


async def generate_pdf_async(input_path: str, output_path: str = None):
    """Generate a branded PDF from a markdown file using Playwright."""
    from playwright.async_api import async_playwright

    input_file = Path(input_path)

    if output_path is None:
        output_path = input_file.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    # Read the markdown
    md_content = input_file.read_text(encoding="utf-8")

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
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Fill in template
    final_html = template.replace("{{TITLE}}", title)
    final_html = final_html.replace("{{CONTENT}}", full_content)

    # Generate PDF using Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.set_content(final_html, wait_until="networkidle")

        await page.pdf(
            path=str(output_path),
            format="Letter",
            margin={
                "top": "0.75in",
                "right": "0.875in",
                "bottom": "0.75in",
                "left": "0.875in",
            },
            print_background=True,
        )

        await browser.close()

    print(f"Generated: {output_path}")
    return output_path


def generate_pdf(input_path: str, output_path: str = None):
    """Wrapper to run async function."""
    return asyncio.run(generate_pdf_async(input_path, output_path))


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf_playwright.py input.md [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    generate_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
