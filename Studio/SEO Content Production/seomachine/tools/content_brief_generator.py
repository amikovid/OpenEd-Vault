#!/usr/bin/env python3
"""Content Brief Generator (OpenEd SEO workflow)

Generates a structured content brief for a seed topic/keyword using DataForSEO
and lightweight competitor page scraping.

Usage:
  python content_brief_generator.py "topic keyword"

This script is designed to live in:
  seomachine/tools/

It loads credentials from:
  seomachine/data_sources/config/.env

Notes:
- Scraping is best-effort; some sites may block requests.
- Output is always written to a markdown file in this tools/ directory unless
  overridden via --output-dir.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _safe_imports() -> Tuple[Any, Any, Any]:
    """Import optional dependencies with friendly errors."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: python-dotenv. Install with: pip install python-dotenv"
        ) from e

    try:
        import requests  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: requests. Install with: pip install requests"
        ) from e

    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: beautifulsoup4. Install with: pip install beautifulsoup4"
        ) from e

    return load_dotenv, requests, BeautifulSoup


def _project_root_from_tools_dir(tools_dir: Path) -> Path:
    """tools/ -> project root (parent of tools)."""
    return tools_dir.parent


def _load_env(project_root: Path) -> None:
    load_dotenv, _, _ = _safe_imports()

    env_path = project_root / "data_sources" / "config" / ".env"
    if not env_path.exists():
        raise FileNotFoundError(
            f".env file not found at {env_path}. Expected DataForSEO credentials there."
        )

    load_dotenv(env_path)


def _import_dataforseo(project_root: Path):
    """Import DataForSEO using the existing seomachine/data_sources layout."""
    data_sources_path = project_root / "data_sources"
    sys.path.insert(0, str(data_sources_path))

    try:
        from modules.dataforseo import DataForSEO  # type: ignore

        return DataForSEO
    except Exception as e:
        raise ImportError(
            "Could not import DataForSEO. Expected module at data_sources/modules/dataforseo.py"
        ) from e


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "brief"


def _fmt_num(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        if isinstance(value, (int,)):
            return f"{value:,}"
        if isinstance(value, (float,)):
            # DataForSEO CPC/competition may be floats
            return f"{value:.2f}".rstrip("0").rstrip(".")
        return str(value)
    except Exception:
        return str(value)


def _normalize_heading(text: str) -> str:
    cleaned = text.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    cleaned = cleaned.strip()
    return cleaned


@dataclass
class PageAnalysis:
    url: str
    domain: str
    title: Optional[str]
    word_count: Optional[int]
    h2: List[str]
    h3: List[str]


def _extract_domain(url: str) -> str:
    # Minimal, dependency-free domain extraction.
    m = re.match(r"^https?://([^/]+)", url.strip(), flags=re.IGNORECASE)
    if not m:
        return ""
    host = m.group(1)
    return host.replace("www.", "", 1)


def _pick_main_content(soup: Any) -> Any:
    # Best-effort selection similar to ContentLengthComparator.
    selectors = [
        "article",
        "main",
        '[role="main"]',
        ".content",
        "#content",
        ".post",
        ".entry-content",
        ".article-content",
        ".post-content",
    ]
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            return node
    return soup.find("body") or soup


def _scrape_page(
    url: str,
    timeout_seconds: int,
    user_agent: str,
    delay_seconds: float,
    requests_mod: Any,
    BeautifulSoup: Any,
) -> PageAnalysis:
    headers = {"User-Agent": user_agent}

    # Polite crawling rate.
    if delay_seconds > 0:
        time.sleep(delay_seconds)

    resp = requests_mod.get(
        url, headers=headers, timeout=timeout_seconds, allow_redirects=True
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")

    # Remove common non-content blocks
    for element in soup(
        ["script", "style", "nav", "footer", "header", "aside", "noscript"]
    ):
        try:
            element.decompose()
        except Exception:
            pass

    main = _pick_main_content(soup)

    title = None
    try:
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
    except Exception:
        title = None

    headings_h2: List[str] = []
    headings_h3: List[str] = []

    for tag in main.find_all(["h2", "h3"]):
        try:
            text = tag.get_text(separator=" ", strip=True)
        except Exception:
            continue
        if not text:
            continue

        if tag.name == "h2":
            headings_h2.append(text)
        elif tag.name == "h3":
            headings_h3.append(text)

    word_count = None
    try:
        text = main.get_text(separator=" ", strip=True)
        words = re.findall(r"\b[a-zA-Z]{2,}\b", text)
        if words:
            word_count = len(words)
    except Exception:
        word_count = None

    return PageAnalysis(
        url=url,
        domain=_extract_domain(url),
        title=title,
        word_count=word_count,
        h2=headings_h2,
        h3=headings_h3,
    )


def _percentile_75(values: List[int]) -> int:
    if not values:
        return 0
    values_sorted = sorted(values)
    if len(values_sorted) < 4:
        return values_sorted[-1]
    # Nearest-rank method
    k = int(round(0.75 * (len(values_sorted) - 1)))
    return values_sorted[k]


def _recommend_word_count(values: List[int]) -> Dict[str, int]:
    if not values:
        return {"recommended_min": 0, "recommended_optimal": 0, "recommended_max": 0}

    values_sorted = sorted(values)
    median = values_sorted[len(values_sorted) // 2]
    p75 = _percentile_75(values_sorted)

    recommended_min = median
    recommended_optimal = max(p75, int(median * 1.2))
    recommended_max = int(recommended_optimal * 1.2)

    return {
        "recommended_min": recommended_min,
        "recommended_optimal": recommended_optimal,
        "recommended_max": recommended_max,
    }


def _top_common_headings(
    pages: List[PageAnalysis],
    heading_level: str,
    top_n: int,
) -> List[Tuple[str, int, float]]:
    """Return tuples of (heading_text, freq, avg_position)."""
    if heading_level not in {"h2", "h3"}:
        raise ValueError("heading_level must be 'h2' or 'h3'")

    occurrences: Dict[str, List[int]] = defaultdict(list)
    display_text: Dict[str, Counter] = defaultdict(Counter)

    for page in pages:
        headings = page.h2 if heading_level == "h2" else page.h3
        for idx, heading in enumerate(headings):
            norm = _normalize_heading(heading)
            if not norm:
                continue
            occurrences[norm].append(idx)
            display_text[norm][heading.strip()] += 1

    scored: List[Tuple[str, int, float]] = []
    for norm, positions in occurrences.items():
        freq = len(positions)
        avg_pos = sum(positions) / len(positions)
        best_text = display_text[norm].most_common(1)[0][0]
        scored.append((best_text, freq, avg_pos))

    scored.sort(key=lambda x: (-x[1], x[2], x[0].lower()))
    return scored[:top_n]


def _structure_patterns(pages: List[PageAnalysis]) -> Dict[str, int]:
    patterns = Counter()

    markers = {
        "definition/what-is": ["what is", "definition"],
        "how-to/steps": ["how to", "steps", "step-by-step"],
        "benefits": ["benefits", "advantages"],
        "examples": ["examples", "case study", "case studies"],
        "tips/best-practices": ["tips", "best practices"],
        "mistakes": ["mistakes", "common mistakes"],
        "faq": ["faq", "frequently asked"],
        "conclusion": ["conclusion", "final thoughts", "wrap up"],
    }

    for page in pages:
        combined = " ".join(page.h2 + page.h3).lower()
        for label, needles in markers.items():
            if any(n in combined for n in needles):
                patterns[label] += 1

    return dict(patterns)


def _keyword_coverage_opportunities(
    secondary_keywords: List[Dict[str, Any]],
    pages: List[PageAnalysis],
    max_items: int,
) -> List[Dict[str, Any]]:
    """Find related keywords that do NOT appear in competitor headings."""
    if not secondary_keywords:
        return []

    heading_text = " ".join([" ".join(p.h2 + p.h3) for p in pages]).lower()

    opportunities = []
    for item in secondary_keywords:
        kw = (item.get("keyword") or "").strip()
        if not kw:
            continue
        # Simple containment check (best-effort).
        if kw.lower() in heading_text:
            continue
        opportunities.append(item)

    # Prefer higher volume first.
    opportunities.sort(key=lambda x: x.get("search_volume") or 0, reverse=True)
    return opportunities[:max_items]


def _render_markdown_brief(
    topic: str,
    primary_metrics: Dict[str, Any],
    serp: Dict[str, Any],
    secondary_keywords: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
    pages: List[PageAnalysis],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    organic = serp.get("organic_results", []) or []

    scraped_count = len(pages)
    word_counts = [p.word_count for p in pages if p.word_count]
    word_counts_int = [int(x) for x in word_counts if isinstance(x, int)]

    avg_wc = int(sum(word_counts_int) / len(word_counts_int)) if word_counts_int else 0
    rec_wc = _recommend_word_count(word_counts_int)

    common_h2 = _top_common_headings(pages, "h2", top_n=12) if pages else []
    common_h3 = _top_common_headings(pages, "h3", top_n=15) if pages else []

    patterns = _structure_patterns(pages) if pages else {}

    opportunities = _keyword_coverage_opportunities(
        secondary_keywords=secondary_keywords,
        pages=pages,
        max_items=6,
    )

    lines: List[str] = []

    lines.append(f"# Content Brief: {topic}")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")

    lines.append("## Primary Keyword + Metrics")
    lines.append("")
    lines.append(f"- **Primary keyword:** {topic}")
    lines.append(
        f"- **Search volume:** {_fmt_num(primary_metrics.get('search_volume'))}"
    )
    lines.append(f"- **CPC:** {_fmt_num(primary_metrics.get('cpc'))}")
    lines.append(f"- **Competition:** {_fmt_num(primary_metrics.get('competition'))}")
    lines.append(
        f"- **SERP features:** {', '.join(serp.get('features') or []) or 'N/A'}"
    )
    lines.append("")

    lines.append("## SERP Top Results (Top 10)")
    lines.append("")
    if organic:
        for r in organic[:10]:
            pos = r.get("position")
            title = r.get("title") or "(no title)"
            url = r.get("url") or ""
            domain = r.get("domain") or _extract_domain(url)
            lines.append(f"- {pos}. **{domain}** — {title}")
            if url:
                lines.append(f"  - {url}")
    else:
        lines.append("- No organic results returned.")
    lines.append("")

    lines.append("## Secondary Keyword Cluster (Top 20)")
    lines.append("")
    if secondary_keywords:
        lines.append("| Keyword | Volume | CPC | Competition |")
        lines.append("|---|---:|---:|---:|")
        for item in secondary_keywords[:20]:
            lines.append(
                "| "
                + str(item.get("keyword") or "")
                + " | "
                + _fmt_num(item.get("search_volume"))
                + " | "
                + _fmt_num(item.get("cpc"))
                + " | "
                + _fmt_num(item.get("competition"))
                + " |"
            )
    else:
        lines.append("- No related keywords returned.")
    lines.append("")

    lines.append("## Suggested H2 Structure (Competitor-Informed)")
    lines.append("")
    if common_h2:
        lines.append("Suggested H2s (ranked by frequency across top pages):")
        lines.append("")
        for heading, freq, avg_pos in common_h2:
            lines.append(f"- {heading}  _(seen {freq}x, avg order {avg_pos:.1f})_")
    else:
        lines.append("- Could not extract H2 headings from competitor pages.")
    lines.append("")

    lines.append("## Common H3 Themes")
    lines.append("")
    if common_h3:
        for heading, freq, _avg_pos in common_h3:
            lines.append(f"- {heading} _(seen {freq}x)_")
    else:
        lines.append("- Could not extract H3 headings from competitor pages.")
    lines.append("")

    lines.append("## FAQ Questions To Answer")
    lines.append("")
    if questions:
        for q in questions[:15]:
            question = q.get("question") or ""
            vol = q.get("search_volume")
            lines.append(
                f"- {question}" + (f" _(vol: {_fmt_num(vol)})_" if vol else "")
            )
    else:
        lines.append("- No questions returned.")
    lines.append("")

    lines.append("## Target Word Count")
    lines.append("")
    if word_counts_int:
        lines.append(f"- Pages successfully scraped: {scraped_count}")
        lines.append(f"- Average competitor word count: {avg_wc:,}")
        lines.append(
            "- Recommended range: "
            f"{rec_wc['recommended_min']:,}–{rec_wc['recommended_max']:,} "
            f"(optimal ~{rec_wc['recommended_optimal']:,})"
        )
    else:
        lines.append(f"- Pages successfully scraped: {scraped_count}")
        lines.append("- Word count analysis unavailable (scraping blocked or failed).")
    lines.append("")

    lines.append("## Content Structure Patterns")
    lines.append("")
    if patterns:
        for name, count in sorted(patterns.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {name}: {count}/{max(1, scraped_count)} pages")
    else:
        lines.append("- Not enough scraped data to infer patterns.")
    lines.append("")

    lines.append("## Differentiation Opportunities")
    lines.append("")
    lines.append(
        "Use this section to intentionally cover gaps or add unique value beyond the top-ranking pages."
    )
    lines.append("")

    if opportunities:
        lines.append(
            "Potential missing angles (related keywords not reflected in competitor headings):"
        )
        lines.append("")
        for item in opportunities:
            kw = item.get("keyword")
            vol = item.get("search_volume")
            lines.append(f"- {kw}" + (f" _(vol: {_fmt_num(vol)})_" if vol else ""))
        lines.append("")

    lines.append("Other practical differentiators to consider:")
    lines.append("")
    lines.append("- Add a clear definition + quick summary at top (snippet-friendly).")
    lines.append("- Include a worked example, template, or checklist readers can copy.")
    lines.append("- Address common misconceptions and edge cases competitors skip.")
    lines.append(
        "- Add an FAQ section mapped directly to People Also Ask-style questions."
    )
    lines.append("")

    lines.append("## Notes / Limitations")
    lines.append("")
    lines.append(
        "- Competitor scraping is best-effort and may miss headings on JS-heavy sites."
    )
    lines.append("- Metrics come from DataForSEO and may vary by location/device.")

    return "\n".join(lines).rstrip() + "\n"


def generate_brief(
    topic: str,
    location_code: int,
    keyword_ideas_limit: int,
    serp_depth: int,
    scrape_top_n: int,
    delay_seconds: float,
    timeout_seconds: int,
    user_agent: str,
) -> Tuple[str, Dict[str, Any]]:
    tools_dir = Path(__file__).resolve().parent
    project_root = _project_root_from_tools_dir(tools_dir)

    _load_env(project_root)
    DataForSEO = _import_dataforseo(project_root)

    # DataForSEO calls
    dfs = DataForSEO()

    # Light API pacing (cost control + politeness)
    if delay_seconds > 0:
        time.sleep(delay_seconds)
    serp = dfs.get_serp_data(topic, location_code=location_code, limit=serp_depth)

    if delay_seconds > 0:
        time.sleep(delay_seconds)
    keyword_ideas = dfs.get_keyword_ideas(
        topic, location_code=location_code, limit=keyword_ideas_limit
    )

    if delay_seconds > 0:
        time.sleep(delay_seconds)
    questions = dfs.get_questions(topic, location_code=location_code, limit=50)

    primary_metrics = {
        "search_volume": serp.get("search_volume"),
        "cpc": serp.get("cpc"),
        "competition": serp.get("competition"),
    }

    organic = serp.get("organic_results", []) or []
    top_urls = [r.get("url") for r in organic if r.get("url")]
    top_urls = [u for u in top_urls if isinstance(u, str) and u.startswith("http")]
    top_urls = top_urls[:scrape_top_n]

    # Scrape competitor pages
    _, requests_mod, BeautifulSoup = _safe_imports()

    pages: List[PageAnalysis] = []
    scrape_errors: List[Tuple[str, str]] = []

    for url in top_urls:
        try:
            pages.append(
                _scrape_page(
                    url=url,
                    timeout_seconds=timeout_seconds,
                    user_agent=user_agent,
                    delay_seconds=delay_seconds,
                    requests_mod=requests_mod,
                    BeautifulSoup=BeautifulSoup,
                )
            )
        except Exception as e:
            scrape_errors.append((url, str(e)))

    # Reduce secondary cluster to top 20 (already sorted by volume in module)
    secondary_top = (keyword_ideas or [])[:20]

    markdown = _render_markdown_brief(
        topic=topic,
        primary_metrics=primary_metrics,
        serp=serp,
        secondary_keywords=secondary_top,
        questions=questions or [],
        pages=pages,
    )

    metadata = {
        "topic": topic,
        "location_code": location_code,
        "serp_results": len(organic[:10]),
        "scraped_pages": len(pages),
        "scrape_errors": scrape_errors,
    }

    return markdown, metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an SEO content brief using DataForSEO + competitor scraping"
    )
    parser.add_argument("topic", help="Seed topic / keyword, wrap in quotes")
    parser.add_argument(
        "--location-code",
        type=int,
        default=2840,
        help="DataForSEO location code (default: 2840 = USA)",
    )
    parser.add_argument(
        "--keyword-ideas-limit",
        type=int,
        default=100,
        help="How many keyword ideas to request from DataForSEO",
    )
    parser.add_argument(
        "--serp-depth",
        type=int,
        default=20,
        help="How many SERP results to request from DataForSEO",
    )
    parser.add_argument(
        "--scrape-top-n",
        type=int,
        default=10,
        help="How many top ranking URLs to scrape",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=1.0,
        help="Delay between API/scrape requests",
    )
    parser.add_argument(
        "--timeout-seconds", type=int, default=12, help="HTTP timeout for scraping"
    )
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        help="User-Agent used for competitor scraping",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to write the markdown brief (default: this script's tools/ directory)",
    )

    args = parser.parse_args()

    try:
        markdown, metadata = generate_brief(
            topic=args.topic,
            location_code=args.location_code,
            keyword_ideas_limit=args.keyword_ideas_limit,
            serp_depth=args.serp_depth,
            scrape_top_n=args.scrape_top_n,
            delay_seconds=args.delay_seconds,
            timeout_seconds=args.timeout_seconds,
            user_agent=args.user_agent,
        )

        tools_dir = Path(__file__).resolve().parent
        output_dir = (
            Path(args.output_dir).expanduser().resolve()
            if args.output_dir
            else tools_dir
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        slug = _slugify(args.topic)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = output_dir / f"content_brief_{slug}_{timestamp}.md"
        out_path.write_text(markdown, encoding="utf-8")

        print(f"Wrote brief: {out_path}")

        if metadata.get("scrape_errors"):
            print("\nSome competitor pages could not be scraped:")
            for url, err in metadata["scrape_errors"][:5]:
                print(f"- {url} ({err})")
            if len(metadata["scrape_errors"]) > 5:
                print(f"- ...and {len(metadata['scrape_errors']) - 5} more")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
