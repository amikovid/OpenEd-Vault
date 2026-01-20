#!/usr/bin/env python3
"""Competitor Gap Finder (OpenEd SEO workflow)

Finds high-value keywords a competitor ranks for that `opened.co` does NOT rank for
(within a configurable SERP depth), then prioritizes opportunities.

Core idea:
- Pull competitor's ranked keywords (DataForSEO Labs domain analysis)
- For each keyword, check whether opened.co appears in top N Google organic results
- Keep the gaps, filter by min volume, sort by opportunity score (volume / competition)

Examples:
  python tools/competitor_gap_finder.py --competitor cathyduffy.com --min-volume 200
  python tools/competitor_gap_finder.py --competitor cathyduffy.com --competitor hslda.org --min-volume 200
  python tools/competitor_gap_finder.py --batch --min-volume 200

Outputs:
- Markdown report (prioritized roadmap)
- CSV export (easy to sort/filter)

Notes:
- Uses DataForSEO creds from: seomachine/data_sources/config/.env
- "Not ranking" means not found within `--serp-depth`.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


OPENED_DOMAIN = "opened.co"
DEFAULT_COMPETITORS = [
    "cathyduffy.com",
    "thehomeschoolmom.com",
    "hslda.org",
    "simplycharlottemason.com",
    "welltrainedmind.com",
]


class DataForSEOApiError(RuntimeError):
    pass


def _safe_imports() -> Tuple[Any, Any]:
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

    return load_dotenv, requests


def _tools_dir() -> Path:
    return Path(__file__).resolve().parent


def _project_root(tools_dir: Path) -> Path:
    return tools_dir.parent


def _load_env(project_root: Path) -> None:
    load_dotenv, _ = _safe_imports()

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


def _normalize_domain(domain: str) -> str:
    domain = domain.strip().lower()
    domain = domain.replace("https://", "").replace("http://", "")
    domain = domain.strip("/")
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def _chunked(items: Sequence[str], size: int) -> Iterable[List[str]]:
    if size <= 0:
        raise ValueError("chunk size must be > 0")
    for i in range(0, len(items), size):
        yield list(items[i : i + size])


def _parse_competitors(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []

    out: List[str] = []
    for v in values:
        for part in v.split(","):
            d = _normalize_domain(part)
            if d and d not in out:
                out.append(d)
    return out


def _suggest_content_type(keyword: str) -> str:
    k = keyword.strip().lower()

    # Comparison intent
    if " vs " in f" {k} " or " versus " in k or "compare" in k or "comparison" in k:
        return "comparison"

    # How-to intent
    if re.match(r"^(how|what|why|when|where|who|can|should|is|are|do|does)\b", k):
        return "how-to"

    # Default: evergreen guide
    return "guide"


def _difficulty_from_competition(competition: Optional[Any]) -> Optional[int]:
    if competition is None:
        return None
    try:
        c = float(competition)
    except Exception:
        return None

    # DataForSEO often returns competition in 0..1 range.
    if 0 <= c <= 1:
        return int(round(c * 100))

    # If a provider returns 0..100, keep it.
    if 0 <= c <= 100:
        return int(round(c))

    return None


def _opportunity_score(search_volume: int, competition: Optional[Any]) -> float:
    try:
        c = float(competition) if competition is not None else 1.0
    except Exception:
        c = 1.0

    # Guard division-by-zero; still reward low-competition terms.
    denom = c if c and c > 0 else 0.01
    return float(search_volume) / denom


def _dfs_post_with_retries(
    dfs: Any,
    endpoint: str,
    payload: List[Dict[str, Any]],
    *,
    max_retries: int,
    base_delay_seconds: float,
    extra_delay_seconds: float,
) -> Dict[str, Any]:
    _, requests = _safe_imports()

    attempt = 0
    while True:
        attempt += 1
        try:
            if extra_delay_seconds > 0:
                time.sleep(extra_delay_seconds)
            response = dfs._post(endpoint, payload)  # type: ignore[attr-defined]
            return response
        except requests.exceptions.HTTPError as e:  # type: ignore[attr-defined]
            status_code = None
            try:
                status_code = e.response.status_code if e.response is not None else None
            except Exception:
                status_code = None

            is_retryable = status_code in {408, 409, 425, 429, 500, 502, 503, 504}
            if attempt > max_retries or not is_retryable:
                raise

            sleep_s = base_delay_seconds * (2 ** (attempt - 1))
            time.sleep(min(sleep_s, 60.0))
        except requests.exceptions.RequestException:  # type: ignore[attr-defined]
            if attempt > max_retries:
                raise
            sleep_s = base_delay_seconds * (2 ** (attempt - 1))
            time.sleep(min(sleep_s, 60.0))


def _extract_items_from_labs_response(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    if resp.get("status_code") != 20000:
        raise DataForSEOApiError(
            f"DataForSEO error: status_code={resp.get('status_code')} message={resp.get('status_message')}"
        )

    tasks = resp.get("tasks") or []
    if not tasks:
        return []

    task = tasks[0]
    if task.get("status_code") != 20000:
        raise DataForSEOApiError(
            f"DataForSEO task error: status_code={task.get('status_code')} message={task.get('status_message')}"
        )

    results = task.get("result") or []
    if not results:
        return []

    # For labs endpoints, result is typically a list with one object
    first = results[0] or {}
    items = first.get("items") or []
    if isinstance(items, list):
        return items
    return []


def fetch_competitor_ranked_keywords(
    dfs: Any,
    competitor_domain: str,
    *,
    location_code: int,
    language_code: str,
    limit: int,
    max_retries: int,
    base_delay_seconds: float,
    delay_seconds: float,
) -> List[Dict[str, Any]]:
    payload = [
        {
            "target": competitor_domain,
            "location_code": location_code,
            "language_code": language_code,
            "limit": limit,
        }
    ]

    resp = _dfs_post_with_retries(
        dfs,
        "/v3/dataforseo_labs/google/ranked_keywords/live",
        payload,
        max_retries=max_retries,
        base_delay_seconds=base_delay_seconds,
        extra_delay_seconds=delay_seconds,
    )
    return _extract_items_from_labs_response(resp)


def fetch_serp_positions(
    dfs: Any,
    keywords: List[str],
    *,
    domains: List[str],
    location_code: int,
    language_code: str,
    serp_depth: int,
    max_retries: int,
    base_delay_seconds: float,
    delay_seconds: float,
) -> Dict[str, Dict[str, Optional[int]]]:
    """Return positions per keyword for each domain (None if not found)."""

    tasks = [
        {
            "keyword": kw,
            "location_code": location_code,
            "language_code": language_code,
            "device": "desktop",
            "os": "windows",
            "depth": serp_depth,
        }
        for kw in keywords
    ]

    resp = _dfs_post_with_retries(
        dfs,
        "/v3/serp/google/organic/live/advanced",
        tasks,
        max_retries=max_retries,
        base_delay_seconds=base_delay_seconds,
        extra_delay_seconds=delay_seconds,
    )

    if resp.get("status_code") != 20000:
        raise DataForSEOApiError(
            f"DataForSEO error: status_code={resp.get('status_code')} message={resp.get('status_message')}"
        )

    out: Dict[str, Dict[str, Optional[int]]] = {}

    for task in resp.get("tasks") or []:
        if task.get("status_code") != 20000:
            continue

        keyword = (task.get("data") or {}).get("keyword")
        if not keyword:
            continue

        result_list = task.get("result") or []
        result0 = result_list[0] if result_list else {}
        items = result0.get("items") or []

        positions: Dict[str, Optional[int]] = {d: None for d in domains}
        for item in items:
            if item.get("type") != "organic":
                continue

            item_domain = (item.get("domain") or "").lower()
            if not item_domain:
                continue

            pos = item.get("rank_absolute")
            if pos is None:
                # Fallback: best-effort based on ordering
                try:
                    pos = int(item.get("rank_group"))
                except Exception:
                    pos = None

            for d in domains:
                if positions.get(d) is not None:
                    continue
                if d in item_domain:
                    try:
                        positions[d] = int(pos) if pos is not None else None
                    except Exception:
                        positions[d] = None

            if all(positions.get(d) is not None for d in domains):
                break

        out[keyword] = positions

    return out


def _fmt_int(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{int(value):,}"
    except Exception:
        return str(value)


def _fmt_float(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.2f}".rstrip("0").rstrip(".")
    except Exception:
        return str(value)


@dataclass
class GapRow:
    keyword: str
    search_volume: int
    competitor_position: Optional[int]
    our_position: Optional[int]
    competition: Optional[float]
    difficulty_estimate: Optional[int]
    suggested_content_type: str
    opportunity_score: float
    competitor_domains: List[str]


def _dedupe_rows(rows: List[GapRow]) -> List[GapRow]:
    by_keyword: Dict[str, GapRow] = {}

    for row in rows:
        key = row.keyword.strip().lower()
        if not key:
            continue

        if key not in by_keyword:
            by_keyword[key] = row
            continue

        existing = by_keyword[key]
        existing_domains = set(existing.competitor_domains)
        for d in row.competitor_domains:
            existing_domains.add(d)
        existing.competitor_domains = sorted(existing_domains)

        # Keep best (lowest) competitor position if available.
        if existing.competitor_position is None:
            existing.competitor_position = row.competitor_position
        elif row.competitor_position is not None:
            existing.competitor_position = min(
                existing.competitor_position, row.competitor_position
            )

        # Keep max opportunity score (should typically be same).
        if row.opportunity_score > existing.opportunity_score:
            existing.opportunity_score = row.opportunity_score
            existing.search_volume = row.search_volume
            existing.competition = row.competition
            existing.difficulty_estimate = row.difficulty_estimate
            existing.suggested_content_type = row.suggested_content_type

    return list(by_keyword.values())


def _sort_rows(rows: List[GapRow]) -> List[GapRow]:
    def key(r: GapRow) -> Tuple[float, int, int]:
        competitor_pos = (
            r.competitor_position if r.competitor_position is not None else 10_000
        )
        return (r.opportunity_score, r.search_volume, -competitor_pos)

    return sorted(rows, key=key, reverse=True)


def _write_csv(path: Path, rows: List[GapRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "keyword",
        "search_volume",
        "competition",
        "opportunity_score",
        "competitor_position",
        "our_position",
        "difficulty_estimate",
        "suggested_content_type",
        "competitors",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "keyword": r.keyword,
                    "search_volume": r.search_volume,
                    "competition": "" if r.competition is None else r.competition,
                    "opportunity_score": round(r.opportunity_score, 4),
                    "competitor_position": ""
                    if r.competitor_position is None
                    else r.competitor_position,
                    "our_position": "" if r.our_position is None else r.our_position,
                    "difficulty_estimate": ""
                    if r.difficulty_estimate is None
                    else r.difficulty_estimate,
                    "suggested_content_type": r.suggested_content_type,
                    "competitors": ", ".join(r.competitor_domains),
                }
            )


def _write_markdown(
    path: Path,
    *,
    rows: List[GapRow],
    competitors: List[str],
    min_volume: int,
    location_code: int,
    language_code: str,
    serp_depth: int,
    max_competitor_position: int,
    keyword_limit_per_competitor: int,
    errors: List[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(rows)

    lines: List[str] = []
    lines.append("# Competitor Gap Finder")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")

    lines.append("## Configuration")
    lines.append("")
    lines.append(f"- Our domain: `{OPENED_DOMAIN}`")
    lines.append(f"- Competitors: {', '.join(f'`{c}`' for c in competitors)}")
    lines.append(f"- Min search volume: `{min_volume}`")
    lines.append(f"- SERP depth checked: `{serp_depth}`")
    lines.append(f"- Max competitor position (filter): `{max_competitor_position}`")
    lines.append(
        f"- Ranked keywords pulled per competitor: `{keyword_limit_per_competitor}`"
    )
    lines.append(f"- Location code: `{location_code}`")
    lines.append(f"- Language code: `{language_code}`")
    lines.append("")

    lines.append("## How to Read This")
    lines.append("")
    lines.append(
        "- **Opportunity score** = `search_volume / competition` (competition is typically 0–1)."
    )
    lines.append(
        "- **Not ranking** means `opened.co` was not found in the top `--serp-depth` organic results."
    )
    lines.append(
        "- **Suggested content type** is a heuristic (guide / comparison / how-to)."
    )
    lines.append("")

    if errors:
        lines.append("## Warnings")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.append(f"## Prioritized Opportunities ({total})")
    lines.append("")

    if not rows:
        lines.append("No gaps found with current filters.")
    else:
        lines.append(
            "| Keyword | Volume | Competitor pos | Our pos | Difficulty | Competition | Opp. score | Content type | Competitors |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|---:|---|---|")
        for r in rows[:300]:
            lines.append(
                "| "
                + r.keyword.replace("|", "\\|")
                + " | "
                + _fmt_int(r.search_volume)
                + " | "
                + ("" if r.competitor_position is None else str(r.competitor_position))
                + " | "
                + ("" if r.our_position is None else str(r.our_position))
                + " | "
                + ("" if r.difficulty_estimate is None else str(r.difficulty_estimate))
                + " | "
                + _fmt_float(r.competition)
                + " | "
                + _fmt_float(r.opportunity_score)
                + " | "
                + r.suggested_content_type
                + " | "
                + ", ".join(r.competitor_domains)
                + " |"
            )

        if total > 300:
            lines.append("")
            lines.append(
                f"_Showing top 300 rows. CSV contains all {total} opportunities._"
            )

    lines.append("")
    lines.append("## Next Step: Turn This Into a Roadmap")
    lines.append("")
    lines.append(
        "A practical workflow is to take the top 25–50 keywords and group them into 6–12 topic clusters (one pillar + supporting posts each)."
    )
    lines.append(
        "Then run `tools/content_brief_generator.py` for the top pillar topics to generate detailed briefs."
    )
    lines.append("")

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def build_gaps_for_competitor(
    dfs: Any,
    competitor: str,
    *,
    min_volume: int,
    max_competitor_position: int,
    keyword_limit_per_competitor: int,
    location_code: int,
    language_code: str,
    serp_depth: int,
    serp_batch_size: int,
    max_retries: int,
    base_delay_seconds: float,
    delay_seconds: float,
) -> Tuple[List[GapRow], List[str]]:
    """Returns (gap_rows, warnings)."""

    warnings: List[str] = []
    competitor = _normalize_domain(competitor)

    items: List[Dict[str, Any]] = []
    try:
        items = fetch_competitor_ranked_keywords(
            dfs,
            competitor,
            location_code=location_code,
            language_code=language_code,
            limit=keyword_limit_per_competitor,
            max_retries=max_retries,
            base_delay_seconds=base_delay_seconds,
            delay_seconds=delay_seconds,
        )
    except Exception as e:
        warnings.append(f"Failed to fetch ranked keywords for {competitor}: {e}")
        return [], warnings

    # Extract keywords + metrics from labs response.
    keyword_records: List[Tuple[str, int, Optional[float]]] = []
    for item in items:
        keyword = (item.get("keyword_data") or {}).get("keyword") or (
            item.get("keyword") or ""
        )
        keyword = (keyword or "").strip()
        if not keyword:
            continue

        kw_info = (item.get("keyword_data") or {}).get("keyword_info") or {}
        volume = kw_info.get("search_volume")
        competition = kw_info.get("competition")

        try:
            volume_int = int(volume) if volume is not None else 0
        except Exception:
            volume_int = 0

        if volume_int < min_volume:
            continue

        try:
            competition_float = float(competition) if competition is not None else None
        except Exception:
            competition_float = None

        keyword_records.append((keyword, volume_int, competition_float))

    if not keyword_records:
        return [], warnings

    # SERP-check batches to confirm competitor position and detect our position.
    domains = [_normalize_domain(competitor), _normalize_domain(OPENED_DOMAIN)]

    gaps: List[GapRow] = []

    keywords = [k for (k, _, _) in keyword_records]
    volume_by_keyword = {k: v for (k, v, _) in keyword_records}
    competition_by_keyword = {k: c for (k, _, c) in keyword_records}

    for batch in _chunked(keywords, serp_batch_size):
        try:
            positions = fetch_serp_positions(
                dfs,
                batch,
                domains=domains,
                location_code=location_code,
                language_code=language_code,
                serp_depth=serp_depth,
                max_retries=max_retries,
                base_delay_seconds=base_delay_seconds,
                delay_seconds=delay_seconds,
            )
        except Exception as e:
            warnings.append(
                f"SERP position fetch failed for {competitor} batch (size {len(batch)}): {e}"
            )
            continue

        for kw in batch:
            pos = positions.get(kw)
            if not pos:
                continue

            competitor_pos = pos.get(domains[0])
            our_pos = pos.get(domains[1])

            # Filter: competitor should be ranking.
            if competitor_pos is None:
                continue

            # Filter: competitor must be within max position ("top ranking").
            if competitor_pos > max_competitor_position:
                continue

            # Keep only gaps where we do NOT rank.
            if our_pos is not None:
                continue

            search_volume = volume_by_keyword.get(kw, 0)
            competition = competition_by_keyword.get(kw)

            gaps.append(
                GapRow(
                    keyword=kw,
                    search_volume=search_volume,
                    competitor_position=competitor_pos,
                    our_position=our_pos,
                    competition=competition,
                    difficulty_estimate=_difficulty_from_competition(competition),
                    suggested_content_type=_suggest_content_type(kw),
                    opportunity_score=_opportunity_score(search_volume, competition),
                    competitor_domains=[competitor],
                )
            )

    return gaps, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Competitor Gap Finder (OpenEd SEO workflow)",
    )
    parser.add_argument(
        "--competitor",
        action="append",
        help="Competitor domain (repeatable, or comma-separated)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Run against default competitor list and dedupe",
    )
    parser.add_argument(
        "--our-domain",
        default=OPENED_DOMAIN,
        help=f"Our domain to compare against (default: {OPENED_DOMAIN})",
    )
    parser.add_argument(
        "--min-volume",
        type=int,
        default=100,
        help="Minimum monthly search volume (default: 100)",
    )
    parser.add_argument(
        "--max-competitor-position",
        type=int,
        default=20,
        help="Only consider keywords competitor ranks within this position (default: 20)",
    )
    parser.add_argument(
        "--keyword-limit",
        type=int,
        default=500,
        help="How many ranked keywords to pull per competitor (default: 500)",
    )
    parser.add_argument(
        "--serp-depth",
        type=int,
        default=100,
        help="How deep to check Google organic results (default: 100)",
    )
    parser.add_argument(
        "--serp-batch-size",
        type=int,
        default=50,
        help="How many keywords per SERP request batch (default: 50)",
    )
    parser.add_argument(
        "--location-code",
        type=int,
        default=2840,
        help="DataForSEO location code (default: 2840 = USA)",
    )
    parser.add_argument(
        "--language-code",
        default="en",
        help="DataForSEO language code (default: en)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(_tools_dir()),
        help="Directory to write markdown + CSV (default: tools/)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Max retries for retryable API errors (default: 5)",
    )
    parser.add_argument(
        "--base-delay-seconds",
        type=float,
        default=1.0,
        help="Base delay for exponential backoff (default: 1.0)",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0.0,
        help="Extra delay between API calls (default: 0)",
    )

    args = parser.parse_args()

    global OPENED_DOMAIN
    OPENED_DOMAIN = _normalize_domain(args.our_domain)

    competitors = _parse_competitors(args.competitor)
    if args.batch:
        for c in DEFAULT_COMPETITORS:
            d = _normalize_domain(c)
            if d and d not in competitors:
                competitors.append(d)

    if not competitors:
        parser.error("Provide --competitor or use --batch")

    tools_dir = _tools_dir()
    project_root = _project_root(tools_dir)

    _load_env(project_root)
    DataForSEO = _import_dataforseo(project_root)

    dfs = DataForSEO()

    all_rows: List[GapRow] = []
    all_warnings: List[str] = []

    for competitor in competitors:
        rows, warnings = build_gaps_for_competitor(
            dfs,
            competitor,
            min_volume=args.min_volume,
            max_competitor_position=args.max_competitor_position,
            keyword_limit_per_competitor=args.keyword_limit,
            location_code=args.location_code,
            language_code=args.language_code,
            serp_depth=args.serp_depth,
            serp_batch_size=args.serp_batch_size,
            max_retries=args.max_retries,
            base_delay_seconds=args.base_delay_seconds,
            delay_seconds=args.delay_seconds,
        )
        all_rows.extend(rows)
        all_warnings.extend(warnings)

    # Batch mode should dedupe; single competitor output can still dedupe safely.
    deduped = _dedupe_rows(all_rows)
    sorted_rows = _sort_rows(deduped)

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.batch or len(competitors) > 1:
        base_name = f"competitor_gap_batch_{timestamp}"
    else:
        base_name = f"competitor_gap_{competitors[0]}_{timestamp}".replace(".", "_")

    md_path = output_dir / f"{base_name}.md"
    csv_path = output_dir / f"{base_name}.csv"

    _write_markdown(
        md_path,
        rows=sorted_rows,
        competitors=competitors,
        min_volume=args.min_volume,
        location_code=args.location_code,
        language_code=args.language_code,
        serp_depth=args.serp_depth,
        max_competitor_position=args.max_competitor_position,
        keyword_limit_per_competitor=args.keyword_limit,
        errors=all_warnings,
    )
    _write_csv(csv_path, sorted_rows)

    print(f"Wrote markdown: {md_path}")
    print(f"Wrote CSV:      {csv_path}")
    print(f"Opportunities:  {len(sorted_rows)}")
    if all_warnings:
        print(f"Warnings:       {len(all_warnings)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
