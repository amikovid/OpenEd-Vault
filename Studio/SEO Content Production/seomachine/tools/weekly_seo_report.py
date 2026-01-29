#!/usr/bin/env python3
"""
Weekly SEO Report Generator

Generates a formatted report with:
- Quick wins (keywords ranking 11-20)
- Content decay alerts (traffic drops)
- Competitor gap opportunities
- Top performing content

Usage:
  python weekly_seo_report.py --domain opened.co
  python weekly_seo_report.py --domain opened.co --competitors cathyduffy.com,hslda.org
  python weekly_seo_report.py --domain opened.co --output slack
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from seo_history import SEOHistory


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        env_path = _project_root() / "data_sources" / "config" / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        pass


def _import_modules():
    data_sources = _project_root() / "data_sources"
    sys.path.insert(0, str(data_sources))

    modules = {}

    try:
        from modules.dataforseo import DataForSEO

        modules["dataforseo"] = DataForSEO
    except Exception as e:
        modules["dataforseo"] = None
        modules["dataforseo_error"] = str(e)

    try:
        from modules.google_search_console import GoogleSearchConsole

        modules["gsc"] = GoogleSearchConsole
    except Exception as e:
        modules["gsc"] = None
        modules["gsc_error"] = str(e)

    try:
        from modules.google_analytics import GoogleAnalytics

        modules["ga4"] = GoogleAnalytics
    except Exception as e:
        modules["ga4"] = None
        modules["ga4_error"] = str(e)

    return modules


class WeeklyReport:
    """Weekly SEO report tailored for OpenEd's content strategy."""

    # OpenEd's priority keywords from content plan (OpenEd_MTH_SEO.xlsx)
    PRIORITY_KEYWORDS = {
        # High-volume pedagogy targets
        "montessori": {"volume": 63000, "category": "Pedagogy"},
        "homeschool": {"volume": 21000, "category": "Pedagogy"},
        "homeschool curriculum": {"volume": 15000, "category": "Curriculum"},
        "homeschool programs": {"volume": 8300, "category": "Programs"},
        "virtual school": {"volume": 4100, "category": "Pedagogy"},
        "classical education": {"volume": 4100, "category": "Pedagogy"},
        "charlotte mason": {"volume": 3100, "category": "Pedagogy"},
        "waldorf education": {"volume": 2400, "category": "Pedagogy"},
        # State pages (Q1 priority)
        "how to homeschool in oregon": {"volume": 320, "category": "State"},
        "how to homeschool in nevada": {"volume": 260, "category": "State"},
        "how to homeschool in indiana": {"volume": 260, "category": "State"},
        # Curriculum by grade
        "kindergarten homeschool curriculum": {
            "volume": 1600,
            "category": "Curriculum",
        },
        "1st grade homeschool curriculum": {"volume": 1300, "category": "Curriculum"},
        "middle school homeschool curriculum": {
            "volume": 880,
            "category": "Curriculum",
        },
        "high school homeschool curriculum": {"volume": 880, "category": "Curriculum"},
        # Programs/Tools
        "online homeschool programs": {"volume": 4100, "category": "Programs"},
        "accredited homeschool programs": {"volume": 2400, "category": "Programs"},
        "free homeschool curriculum": {"volume": 3500, "category": "Curriculum"},
    }

    # Content categories to filter quick wins
    CONTENT_CATEGORIES = [
        "homeschool",
        "curriculum",
        "education",
        "school",
        "learning",
        "montessori",
        "classical",
        "charlotte mason",
        "waldorf",
        "oregon",
        "nevada",
        "indiana",  # Priority states
        "grade",
        "kindergarten",
        "elementary",
        "middle school",
        "high school",
    ]

    def __init__(self, domain: str, competitors: List[str] = None, track_history: bool = True):
        self.domain = domain
        self.competitors = competitors or []
        self.modules = _import_modules()
        self.track_history = track_history
        self.history = SEOHistory() if track_history else None
        self.changes = {}  # Week-over-week changes
        self.data = {
            "quick_wins": [],
            "declining_content": [],
            "priority_tracking": [],  # NEW: Track our target keywords
            "keyword_opportunities": [],
            "top_content": [],
            "errors": [],
            "warnings": [],
        }

    def _is_relevant_keyword(self, keyword: str) -> bool:
        """Check if keyword is relevant to OpenEd's content categories."""
        keyword_lower = keyword.lower()
        return any(cat in keyword_lower for cat in self.CONTENT_CATEGORIES)

    def _try_priority_tracking(self) -> List[Dict]:
        """Track rankings for OpenEd's priority keywords."""
        if not self.modules.get("gsc"):
            return []

        try:
            gsc = self.modules["gsc"]()
            rankings = gsc.get_keyword_positions(days=30)

            # Create lookup of current rankings
            ranking_lookup = {}
            for kw in rankings:
                keyword = (kw.get("keyword") or kw.get("query") or "").lower()
                ranking_lookup[keyword] = {
                    "position": kw.get("position", 0),
                    "impressions": kw.get("impressions", 0),
                    "clicks": kw.get("clicks", 0),
                }

            # Check our priority keywords
            priority_results = []
            for keyword, meta in self.PRIORITY_KEYWORDS.items():
                data = ranking_lookup.get(keyword.lower(), {})
                pos = data.get("position", 0)
                priority_results.append(
                    {
                        "keyword": keyword,
                        "target_volume": meta["volume"],
                        "category": meta["category"],
                        "current_position": round(pos, 1) if pos else "Not ranking",
                        "impressions": data.get("impressions", 0),
                        "clicks": data.get("clicks", 0),
                        "status": self._get_position_status(pos),
                    }
                )

            # Sort by target volume (highest potential first)
            priority_results.sort(key=lambda x: x["target_volume"], reverse=True)
            return priority_results

        except Exception as e:
            self.data["warnings"].append(f"Priority tracking failed: {e}")
            return []

    def _get_position_status(self, position: float) -> str:
        """Categorize position for quick scanning."""
        if not position or position == 0:
            return "🔴 Not ranking"
        elif position <= 3:
            return "🟢 Top 3"
        elif position <= 10:
            return "🟡 Page 1"
        elif position <= 20:
            return "🟠 Page 2"
        else:
            return "🔴 Page 3+"

    def _try_gsc_quick_wins(self) -> List[Dict]:
        """Find keywords ranking 11-20 with good impressions, filtered for relevance."""
        if not self.modules.get("gsc"):
            self.data["warnings"].append(
                f"GSC not available: {self.modules.get('gsc_error', 'Not configured')}"
            )
            return []

        try:
            gsc = self.modules["gsc"]()
            rankings = gsc.get_keyword_positions(days=30)

            quick_wins = []
            for kw in rankings:
                pos = kw.get("position", 0)
                impressions = kw.get("impressions", 0)
                keyword = kw.get("keyword") or kw.get("query") or "unknown"

                # Filter: position 11-20, good impressions, AND relevant to our content
                if 11 <= pos <= 20 and impressions >= 100:
                    is_relevant = self._is_relevant_keyword(keyword)
                    quick_wins.append(
                        {
                            "keyword": keyword,
                            "position": round(pos, 1),
                            "impressions": impressions,
                            "clicks": kw.get("clicks", 0),
                            "url": kw.get("page", ""),
                            "relevant": is_relevant,
                        }
                    )

            # Sort: relevant keywords first, then by impressions
            quick_wins.sort(key=lambda x: (not x["relevant"], -x["impressions"]))
            return quick_wins[:10]

        except Exception as e:
            # Simplify permission errors
            err_str = str(e)
            if "403" in err_str or "permission" in err_str.lower():
                self.data["warnings"].append(
                    "GSC: No access (need Search Console permissions)"
                )
            else:
                self.data["errors"].append(f"GSC quick wins failed: {e}")
            return []

    def _try_ga4_declining(self) -> List[Dict]:
        """Find content with declining traffic."""
        if not self.modules.get("ga4"):
            self.data["warnings"].append(
                f"GA4 not available: {self.modules.get('ga4_error', 'Not configured')}"
            )
            return []

        try:
            ga4 = self.modules["ga4"]()

            # Use the built-in declining pages method - blog only
            declining_pages = ga4.get_declining_pages(
                comparison_days=30, path_filter="/blog/"
            )

            declining = []
            for page in declining_pages[:5]:
                declining.append(
                    {
                        "url": page.get("path", ""),
                        "title": page.get("title", "")[:50],
                        "current_views": page.get("pageviews", 0),
                        "previous_views": page.get("previous_pageviews", 0),
                        "change_pct": page.get("change_percent", 0),
                    }
                )

            return declining

        except Exception as e:
            self.data["errors"].append(f"GA4 declining content failed: {e}")
            return []

    # REMOVED: _try_competitor_gaps()
    # The previous implementation was misleading - it was just keyword expansion
    # on hardcoded topics, NOT actual competitor analysis.
    #
    # Real competitor gap analysis would require:
    # 1. DataForSEO SERP analysis for competitor domains
    # 2. Comparing their ranking keywords vs ours
    # 3. Finding keywords they rank for that we don't
    #
    # That's expensive and complex. For now, we focus on:
    # - Priority keyword tracking (our actual targets)
    # - Quick wins from GSC (what we're close to ranking for)
    # - Keyword opportunities from seed research

    def _try_keyword_opportunities(self) -> List[Dict]:
        """Get keyword opportunities using DataForSEO."""
        if not self.modules.get("dataforseo"):
            return []

        try:
            dfs = self.modules["dataforseo"]()

            seed_keywords = [
                "homeschool curriculum",
                "online school",
                "education savings account",
            ]

            opportunities = []
            for seed in seed_keywords:
                try:
                    ideas = dfs.get_keyword_ideas(seed, limit=15)
                    if ideas:
                        for kw in ideas:
                            vol = kw.get("search_volume", 0)
                            if vol and vol >= 100:
                                opportunities.append(
                                    {
                                        "keyword": kw.get("keyword"),
                                        "volume": vol,
                                        "cpc": kw.get("cpc", 0),
                                        "competition": kw.get("competition", 0),
                                        "seed": seed,
                                    }
                                )
                except Exception as e:
                    self.data["warnings"].append(
                        f"Keyword search for '{seed}' failed: {e}"
                    )

            seen = set()
            unique = []
            for opp in opportunities:
                if opp["keyword"] not in seen:
                    seen.add(opp["keyword"])
                    unique.append(opp)

            unique.sort(key=lambda x: x["volume"], reverse=True)
            return unique[:15]

        except Exception as e:
            self.data["errors"].append(f"Keyword opportunities failed: {e}")
            return []

    def generate(self, save_snapshot: bool = True) -> Dict:
        """Generate the full report."""
        print(f"Generating weekly SEO report for {self.domain}...")
        print()

        print("  Tracking priority keywords...")
        self.data["priority_tracking"] = self._try_priority_tracking()

        print("  Checking GSC for quick wins...")
        self.data["quick_wins"] = self._try_gsc_quick_wins()

        print("  Checking GA4 for declining content...")
        self.data["declining_content"] = self._try_ga4_declining()

        print("  Getting keyword opportunities...")
        self.data["keyword_opportunities"] = self._try_keyword_opportunities()

        self.data["generated_at"] = datetime.now().isoformat()
        self.data["domain"] = self.domain

        # Save to history and get week-over-week changes
        if self.track_history and self.history and save_snapshot:
            print("  Saving to history...")
            self.changes = self.history.add_snapshot(self.data)
            self.data["changes"] = self.changes

        return self.data

    def export_history(self, output_path: Optional[Path] = None) -> str:
        """Export historical tracking as markdown."""
        if not self.history:
            return "History tracking not enabled."
        return self.history.export_markdown(output_path)

    def get_history_summary(self) -> Dict:
        """Get summary of historical data."""
        if not self.history:
            return {"status": "History tracking not enabled"}
        return self.history.get_summary()

    def format_console(self) -> str:
        """Format report for console output."""
        lines = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines.append("=" * 60)
        lines.append(f"📊 WEEKLY SEO REPORT - {self.domain}")
        lines.append(f"Generated: {now}")
        lines.append("=" * 60)
        lines.append("")

        # Priority Keyword Tracking (NEW)
        if self.data.get("priority_tracking"):
            lines.append("📍 PRIORITY KEYWORD TRACKING")
            lines.append("-" * 50)
            for kw in self.data["priority_tracking"][:8]:
                pos = kw.get("current_position", "N/A")
                pos_str = f"#{pos}" if isinstance(pos, (int, float)) else pos
                lines.append(f"  {kw['status']} {kw['keyword'][:35]:<35} | {pos_str}")
            lines.append("")

        if self.data["quick_wins"]:
            lines.append("🎯 QUICK WINS (Position 11-20, Relevant to Content Strategy)")
            lines.append("-" * 50)
            for kw in self.data["quick_wins"][:5]:
                relevant = "✓" if kw.get("relevant") else " "
                lines.append(
                    f"  {relevant} #{kw['position']:<5} {kw['keyword'][:38]:<38}"
                )
                lines.append(
                    f"         Impressions: {kw['impressions']:,} | Clicks: {kw['clicks']}"
                )
            lines.append("")

        if self.data["declining_content"]:
            lines.append("📉 DECLINING CONTENT (Action Required)")
            lines.append("-" * 50)
            for page in self.data["declining_content"][:5]:
                lines.append(f"  {page['change_pct']:+.1f}% | {page['url'][:50]}")
                lines.append(
                    f"         {page['previous_views']:,} → {page['current_views']:,} views"
                )
            lines.append("")

        if self.data.get("keyword_opportunities"):
            lines.append("💡 KEYWORD OPPORTUNITIES")
            lines.append("-" * 50)
            for opp in self.data["keyword_opportunities"][:5]:
                lines.append(f"  {opp['keyword'][:45]:<45} | Vol: {opp['volume']:,}")
            lines.append("")

        # Week-over-week changes
        if self.changes:
            has_changes = any([
                self.changes.get("improved"),
                self.changes.get("declined"),
                self.changes.get("new_rankings"),
                self.changes.get("lost_rankings")
            ])
            if has_changes:
                lines.append("📈 WEEK-OVER-WEEK CHANGES")
                lines.append("-" * 50)
                if self.changes.get("improved"):
                    for item in self.changes["improved"][:3]:
                        lines.append(f"  ↑ {item['keyword'][:30]}: #{item['from']:.0f} → #{item['to']:.0f}")
                if self.changes.get("declined"):
                    for item in self.changes["declined"][:3]:
                        lines.append(f"  ↓ {item['keyword'][:30]}: #{item['from']:.0f} → #{item['to']:.0f}")
                if self.changes.get("new_rankings"):
                    for item in self.changes["new_rankings"][:2]:
                        lines.append(f"  🆕 {item['keyword'][:30]}: Now #{item['position']:.0f}")
                lines.append("")

        if self.data["warnings"]:
            lines.append("⚠️  WARNINGS")
            lines.append("-" * 50)
            for warning in self.data["warnings"]:
                lines.append(f"  • {warning}")
            lines.append("")

        if self.data["errors"]:
            lines.append("❌ ERRORS")
            lines.append("-" * 50)
            for error in self.data["errors"]:
                lines.append(f"  • {error}")
            lines.append("")

        if not any(
            [
                self.data.get("priority_tracking"),
                self.data["quick_wins"],
                self.data["declining_content"],
                self.data.get("keyword_opportunities"),
            ]
        ):
            lines.append(
                "ℹ️  No data available. Configure GSC/GA4 credentials for full report."
            )
            lines.append("")
            lines.append("   To set up:")
            lines.append("   1. Add GA4_PROPERTY_ID and GA4_CREDENTIALS_PATH to .env")
            lines.append("   2. Add GSC_SITE_URL and GSC_CREDENTIALS_PATH to .env")
            lines.append("   3. Ensure DataForSEO credentials are valid")
            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def format_markdown(self) -> str:
        """Format report as readable markdown with plain English analysis."""
        now = datetime.now().strftime("%B %d, %Y")

        md = []
        md.append(f"# Weekly SEO Report: {self.domain}")
        md.append(f"**Generated:** {now}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## About This Report")
        md.append("")
        md.append(
            "This report pulls data from three sources to surface actionable SEO opportunities:"
        )
        md.append("")
        md.append("| Source | What It Tells Us |")
        md.append("|--------|------------------|")
        md.append(
            "| **Google Search Console** | Keywords we're ranking for, positions, impressions |"
        )
        md.append(
            "| **Google Analytics 4** | Traffic trends, which pages are declining |"
        )
        md.append("| **DataForSEO** | Keyword research, search volumes |")
        md.append("")
        md.append("---")
        md.append("")

        # Priority Keyword Tracking (NEW - most important section)
        if self.data.get("priority_tracking"):
            md.append("## 📍 Priority Keyword Tracking")
            md.append("")
            md.append(
                "How we're ranking for OpenEd's target keywords from the content plan. These are the keywords we're actively trying to rank for."
            )
            md.append("")
            md.append("| Keyword | Target Volume | Current Position | Status |")
            md.append("|---------|---------------|------------------|--------|")
            for kw in self.data["priority_tracking"][:12]:
                keyword = kw.get("keyword", "")[:35]
                vol = kw.get("target_volume", 0)
                pos = kw.get("current_position", "N/A")
                pos_str = f"#{pos}" if isinstance(pos, (int, float)) else pos
                status = kw.get("status", "")
                md.append(f"| {keyword} | {vol:,} | {pos_str} | {status} |")
            md.append("")

            # Summary by category
            categories = {}
            for kw in self.data["priority_tracking"]:
                cat = kw.get("category", "Other")
                if cat not in categories:
                    categories[cat] = {"ranking": 0, "total": 0}
                categories[cat]["total"] += 1
                if (
                    isinstance(kw.get("current_position"), (int, float))
                    and kw["current_position"] > 0
                ):
                    categories[cat]["ranking"] += 1

            md.append("**By Category:**")
            for cat, counts in categories.items():
                md.append(f"- {cat}: {counts['ranking']}/{counts['total']} ranking")
            md.append("")
            md.append("---")
            md.append("")

        # Quick Wins Section
        if self.data["quick_wins"]:
            md.append("## 🎯 Quick Wins: Almost Page 1")
            md.append("")
            md.append(
                "These keywords rank positions 11-20 (page 2). With some optimization, they could reach page 1 where the real traffic is. Focus on the ones with highest impressions - that's how many people are searching."
            )
            md.append("")
            md.append("| Keyword | Position | Impressions | Clicks |")
            md.append("|---------|----------|-------------|--------|")
            for kw in self.data["quick_wins"][:7]:
                keyword = kw.get("keyword", "unknown")[:40]
                pos = kw.get("position", 0)
                imp = kw.get("impressions", 0)
                clicks = kw.get("clicks", 0)
                md.append(f"| {keyword} | #{pos} | {imp:,} | {clicks} |")
            md.append("")

            # Analysis
            top_opp = self.data["quick_wins"][0] if self.data["quick_wins"] else None
            if top_opp:
                md.append(
                    f'**Top opportunity:** "{top_opp.get("keyword", "unknown")}" has {top_opp.get("impressions", 0):,} monthly impressions at position {top_opp.get("position", 0)}. Moving to position 5-10 could 3-5x the clicks.'
                )
            md.append("")
            md.append("---")
            md.append("")

        # Declining Content Section
        if self.data["declining_content"]:
            md.append("## 📉 Declining Content: Needs Refresh")
            md.append("")
            md.append(
                "These blog posts are losing traffic compared to last month. Some drops are seasonal (gift guides after holidays), but others might need content updates to stay competitive."
            )
            md.append("")
            md.append("| Page | Change | Views (before → after) |")
            md.append("|------|--------|------------------------|")
            for page in self.data["declining_content"][:5]:
                url = page.get("url", "")
                # Clean URL to just the slug
                slug = url.split("/")[-1] if "/" in url else url
                slug = slug[:35].replace("|", "-")  # Remove pipes, truncate
                change = page.get("change_pct", 0)
                prev = page.get("previous_views", 0)
                curr = page.get("current_views", 0)
                md.append(f"| {slug} | {change:+.0f}% | {prev:,} → {curr:,} |")
            md.append("")

            # Analysis
            md.append(
                "**What to do:** Review these pages. Are they outdated? Do competitors have fresher content? Consider updating with new information, better examples, or current data."
            )
            md.append("")
            md.append("---")
            md.append("")

        # Keyword Opportunities Section
        if self.data.get("keyword_opportunities"):
            md.append("## 💡 Keyword Opportunities")
            md.append("")
            md.append(
                "High-volume keywords in your space. These are competitive, so they're better for long-term content planning than quick wins."
            )
            md.append("")
            md.append("| Keyword | Monthly Volume |")
            md.append("|---------|----------------|")
            for opp in self.data["keyword_opportunities"][:7]:
                keyword = opp.get("keyword", "")[:45]
                vol = opp.get("volume", 0)
                md.append(f"| {keyword} | {vol:,} |")
            md.append("")
            md.append("---")
            md.append("")

        # Week-over-Week Changes (from history)
        if self.changes:
            md.append("## 📈 Week-over-Week Changes")
            md.append("")

            if self.changes.get("improved"):
                md.append("**Improved (moved up 3+ positions):**")
                for item in self.changes["improved"][:5]:
                    md.append(f"- **{item['keyword']}**: #{item['from']:.0f} → #{item['to']:.0f} (+{item['change']:.0f})")
                md.append("")

            if self.changes.get("declined"):
                md.append("**Declined (dropped 3+ positions):**")
                for item in self.changes["declined"][:5]:
                    md.append(f"- **{item['keyword']}**: #{item['from']:.0f} → #{item['to']:.0f} ({item['change']:.0f})")
                md.append("")

            if self.changes.get("new_rankings"):
                md.append("**New Rankings:**")
                for item in self.changes["new_rankings"][:5]:
                    md.append(f"- **{item['keyword']}**: Now ranking #{item['position']:.0f}")
                md.append("")

            if self.changes.get("lost_rankings"):
                md.append("**Lost Rankings:**")
                for item in self.changes["lost_rankings"][:5]:
                    md.append(f"- **{item['keyword']}**: Was #{item['was']:.0f}, no longer ranking")
                md.append("")

            if not any([self.changes.get("improved"), self.changes.get("declined"),
                       self.changes.get("new_rankings"), self.changes.get("lost_rankings")]):
                md.append("No significant position changes since last report.")
                md.append("")

            md.append("---")
            md.append("")

        # Footer
        md.append("## Data Sources Status")
        md.append("")
        gsc_status = "✅ Connected" if self.data["quick_wins"] else "❌ No data"
        ga4_status = "✅ Connected" if self.data["declining_content"] else "❌ No data"
        dfs_status = (
            "✅ Connected" if self.data.get("keyword_opportunities") else "❌ No data"
        )
        md.append(f"- Google Search Console: {gsc_status}")
        md.append(f"- Google Analytics 4: {ga4_status}")
        md.append(f"- DataForSEO: {dfs_status}")
        md.append("")

        if self.data["warnings"]:
            md.append("**Warnings:**")
            for w in self.data["warnings"]:
                md.append(f"- {w}")
            md.append("")

        if self.data["errors"]:
            md.append("**Errors:**")
            for e in self.data["errors"]:
                md.append(f"- {e}")
            md.append("")

        return "\n".join(md)

    def format_slack(self) -> Dict:
        """Format report for Slack webhook."""
        blocks = []
        now = datetime.now().strftime("%Y-%m-%d")

        blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Weekly SEO Report - {self.domain}",
                },
            }
        )

        blocks.append(
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"Generated: {now}"}],
            }
        )

        blocks.append({"type": "divider"})

        # Priority Tracking
        if self.data.get("priority_tracking"):
            ranking_count = sum(
                1
                for kw in self.data["priority_tracking"]
                if isinstance(kw.get("current_position"), (int, float))
                and kw["current_position"] > 0
            )
            total = len(self.data["priority_tracking"])
            text = f"*📍 Priority Keywords: {ranking_count}/{total} ranking*\n"
            for kw in self.data["priority_tracking"][:3]:
                pos = kw.get("current_position", "N/A")
                pos_str = f"#{pos}" if isinstance(pos, (int, float)) else pos
                text += f"• `{kw['keyword'][:30]}` → {pos_str}\n"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

        if self.data["quick_wins"]:
            text = "*🎯 Quick Wins (Position 11-20)*\n"
            for kw in self.data["quick_wins"][:3]:
                text += f"• #{kw['position']} `{kw['keyword'][:35]}` ({kw['impressions']:,} imp)\n"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

        if self.data["declining_content"]:
            text = "*📉 Declining Content*\n"
            for page in self.data["declining_content"][:3]:
                text += f"• {page['change_pct']:+.0f}% `{page['url'][:40]}`\n"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

        if self.data.get("keyword_opportunities"):
            text = "*💡 Keyword Opportunities*\n"
            for opp in self.data["keyword_opportunities"][:3]:
                text += f"• `{opp['keyword'][:35]}` (vol: {opp['volume']:,})\n"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

        if self.data["warnings"] and not any(
            [
                self.data.get("priority_tracking"),
                self.data["quick_wins"],
                self.data["declining_content"],
            ]
        ):
            text = "*⚠️ Setup Required*\n"
            text += "Configure GSC/GA4 credentials for full report.\n"
            text += "DataForSEO: " + (
                "✅ Connected"
                if self.modules.get("dataforseo")
                else "❌ Not configured"
            )
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

        return {"blocks": blocks}

    def send_to_slack(self, webhook_url: str) -> bool:
        """Send report to Slack via webhook."""
        payload = self.format_slack()

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                webhook_url, data=data, headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    print("✅ Report sent to Slack successfully!")
                    return True
                else:
                    print(f"❌ Slack returned status {response.status}")
                    return False

        except urllib.error.HTTPError as e:
            print(f"❌ Slack webhook error: {e.code} - {e.reason}")
            return False
        except urllib.error.URLError as e:
            print(f"❌ Network error: {e.reason}")
            return False
        except Exception as e:
            print(f"❌ Error sending to Slack: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Generate weekly SEO report")
    parser.add_argument("--domain", required=True, help="Your domain (e.g., opened.co)")
    parser.add_argument(
        "--competitors", default="", help="Comma-separated competitor domains"
    )
    parser.add_argument(
        "--output", choices=["console", "slack", "json", "markdown", "history"], default="console"
    )
    parser.add_argument("--save", help="Save output to file")
    parser.add_argument(
        "--slack-webhook", help="Slack webhook URL (or set SLACK_WEBHOOK_URL env var)"
    )
    parser.add_argument(
        "--no-history", action="store_true", help="Don't save to history (dry run)"
    )
    parser.add_argument(
        "--history-only", action="store_true", help="Just export history without running report"
    )

    args = parser.parse_args()

    _load_env()

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]

    # History-only mode - just export existing data
    if args.history_only:
        report = WeeklyReport(domain=args.domain, competitors=competitors)
        output = report.export_history()
        print(output)
        if args.save:
            Path(args.save).write_text(output)
            print(f"\nSaved to: {args.save}")
        return 0

    report = WeeklyReport(domain=args.domain, competitors=competitors, track_history=not args.no_history)
    report.generate(save_snapshot=not args.no_history)

    # Handle Slack delivery
    webhook_url = args.slack_webhook or os.environ.get("SLACK_WEBHOOK_URL")

    if args.output == "slack" and webhook_url:
        # Send to Slack and also print to console
        report.send_to_slack(webhook_url)
        output = report.format_console()
        print(output)
    elif args.output == "slack" and not webhook_url:
        # Just print Slack JSON format (for testing)
        output = json.dumps(report.format_slack(), indent=2)
        print(output)
        print("\n💡 To send to Slack, set SLACK_WEBHOOK_URL or use --slack-webhook")
    elif args.output == "console":
        output = report.format_console()
        print(output)
    elif args.output == "markdown":
        output = report.format_markdown()
        print(output)
    elif args.output == "json":
        output = json.dumps(report.data, indent=2, default=str)
        print(output)
    elif args.output == "history":
        # Show both current report and historical tracking
        output = report.format_markdown()
        print(output)
        print("\n" + "=" * 60 + "\n")
        history_output = report.export_history()
        print(history_output)
        output = output + "\n\n---\n\n" + history_output

    if args.save:
        save_output = output if isinstance(output, str) else json.dumps(output)
        Path(args.save).write_text(save_output)
        print(f"\nSaved to: {args.save}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
