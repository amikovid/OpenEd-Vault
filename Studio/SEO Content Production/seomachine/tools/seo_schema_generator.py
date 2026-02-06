#!/usr/bin/env python3
"""
SEO Schema Generator - BlogPosting + FAQ JSON-LD

Generates structured data markup for OpenEd blog posts.

Usage:
    from seo_schema_generator import generate_blog_schema, generate_faq_schema

    blog_json = generate_blog_schema(
        headline="John Taylor Gatto: The Teacher Who Quit",
        description="NYC's Teacher of the Year quit...",
        date_published="2026-02-04",
        slug="john-taylor-gatto",
        image_url="https://cdn.prod.website-files.com/...",
        image_width=1200,
        image_height=675,
    )

    faq_json = generate_faq_schema(html_content)
"""

import json
import re


def generate_blog_schema(
    headline: str,
    description: str,
    date_published: str,
    slug: str,
    image_url: str = None,
    image_width: int = None,
    image_height: int = None,
    author_name: str = "OpenEd",
    author_url: str = "https://opened.co",
) -> str:
    """
    Generate BlogPosting JSON-LD schema.

    Args:
        headline: Article title
        description: Meta description / summary
        date_published: ISO date string (YYYY-MM-DD or full ISO 8601)
        slug: URL slug for the article
        image_url: Full CDN URL of the thumbnail/hero image
        image_width: Image width in pixels
        image_height: Image height in pixels
        author_name: Author name (default: OpenEd)
        author_url: Author URL (default: https://opened.co)

    Returns:
        JSON-LD string (without <script> wrapper - for CMS field storage)
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": description,
        "datePublished": date_published,
        "author": {
            "@type": "Organization",
            "name": author_name,
            "url": author_url,
        },
        "publisher": {
            "@type": "Organization",
            "name": "OpenEd",
            "url": "https://opened.co",
        },
        "mainEntityOfPage": f"https://opened.co/blog/{slug}",
    }

    if image_url:
        image_obj = {
            "@type": "ImageObject",
            "url": image_url,
        }
        if image_width and image_height:
            image_obj["width"] = image_width
            image_obj["height"] = image_height
        schema["image"] = image_obj

    return json.dumps(schema, indent=2)


def extract_faq_pairs(html_content: str) -> list:
    """
    Extract FAQ question-answer pairs from HTML content.

    Looks for:
    1. H3 headers ending with '?' followed by paragraph content
    2. A section with "FAQ" in the header, containing Q&A patterns

    Args:
        html_content: The article HTML

    Returns:
        List of {"question": str, "answer": str} dicts
    """
    pairs = []

    # Pattern 1: H3s ending with question mark
    # Match <h3>Question here?</h3> followed by content until next header or end
    h3_pattern = re.compile(
        r'<h3[^>]*>([^<]*\?)\s*</h3>\s*(.*?)(?=<h[23]|$)',
        re.DOTALL
    )

    for match in h3_pattern.finditer(html_content):
        question = match.group(1).strip()
        # Extract text from answer HTML (strip tags for schema)
        answer_html = match.group(2).strip()
        answer_text = re.sub(r'<[^>]+>', '', answer_html).strip()
        # Take first meaningful paragraph (up to ~500 chars)
        answer_text = answer_text[:500].strip()
        if answer_text:
            pairs.append({"question": question, "answer": answer_text})

    # Pattern 2: FAQ section with explicit Q&A
    # Look for a section starting with an FAQ header
    faq_section = re.search(
        r'<h[23][^>]*>[^<]*FAQ[^<]*</h[23]>\s*(.*?)(?=<h[23]|$)',
        html_content,
        re.DOTALL | re.IGNORECASE
    )
    if faq_section:
        faq_html = faq_section.group(1)
        # Look for bold questions followed by answers
        bold_qa = re.findall(
            r'<strong>([^<]*\?)\s*</strong>\s*(.*?)(?=<strong>|<h[23]|$)',
            faq_html,
            re.DOTALL
        )
        for q, a in bold_qa:
            answer_text = re.sub(r'<[^>]+>', '', a).strip()[:500]
            if answer_text and q.strip() not in [p['question'] for p in pairs]:
                pairs.append({"question": q.strip(), "answer": answer_text})

    return pairs


def generate_faq_schema(html_content: str) -> str:
    """
    Generate FAQPage JSON-LD from article HTML.

    Scans for question-pattern H3s and FAQ sections, extracts Q&A pairs,
    and generates schema markup.

    Args:
        html_content: The article HTML content

    Returns:
        JSON-LD string, or empty string if no FAQ pairs found
    """
    pairs = extract_faq_pairs(html_content)

    if not pairs:
        return ""

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": pair["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": pair["answer"],
                },
            }
            for pair in pairs
        ],
    }

    return json.dumps(schema, indent=2)


def generate_all_schema(
    headline: str,
    description: str,
    date_published: str,
    slug: str,
    html_content: str,
    image_url: str = None,
    image_width: int = None,
    image_height: int = None,
) -> dict:
    """
    Generate both BlogPosting and FAQ schemas for an article.

    Returns:
        Dict with 'blog_posting' and 'faq' keys (faq may be empty string)
    """
    blog = generate_blog_schema(
        headline=headline,
        description=description,
        date_published=date_published,
        slug=slug,
        image_url=image_url,
        image_width=image_width,
        image_height=image_height,
    )

    faq = generate_faq_schema(html_content)

    return {
        "blog_posting": blog,
        "faq": faq,
    }


if __name__ == "__main__":
    # Quick test
    test_html = """
    <h2>About John Taylor Gatto</h2>
    <p>He was a famous teacher in NYC.</p>

    <h3>Why did Gatto leave teaching?</h3>
    <p>Gatto resigned because he felt the system was designed to produce conformity rather than thinking citizens. He published his resignation letter in the Wall Street Journal.</p>

    <h3>What are Gatto's 7 lessons?</h3>
    <p>Gatto identified seven hidden lessons that schools teach: confusion, class position, indifference, emotional dependency, intellectual dependency, provisional self-esteem, and surveillance.</p>

    <h3>Is Gatto still relevant today?</h3>
    <p>Yes. His critiques of institutional schooling resonate even more strongly in the post-pandemic era as families explore homeschooling and alternative education.</p>

    <h2>Conclusion</h2>
    <p>Gatto's work remains essential reading.</p>
    """

    print("=== Blog Schema ===")
    print(generate_blog_schema(
        headline="John Taylor Gatto: The Teacher Who Quit",
        description="NYC's Teacher of the Year quit to expose the hidden curriculum.",
        date_published="2026-02-04",
        slug="john-taylor-gatto",
        image_url="https://cdn.prod.website-files.com/example.webp",
        image_width=1200,
        image_height=675,
    ))

    print("\n=== FAQ Schema ===")
    faq = generate_faq_schema(test_html)
    if faq:
        print(faq)
    else:
        print("No FAQ pairs found")
