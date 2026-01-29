#!/usr/bin/env python3
"""
SEO Historical Tracking

Maintains a running history of SEO data for week-over-week analysis.
Stores snapshots in JSON, exports to markdown tables.

Usage:
    from seo_history import SEOHistory

    history = SEOHistory()
    history.add_snapshot(report_data)  # Add current week's data
    history.export_markdown()          # Generate progress tables
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SEOHistory:
    """Track SEO metrics over time for progress evaluation."""

    def __init__(self, history_file: Optional[Path] = None):
        """Initialize with path to history file."""
        self.history_file = history_file or (
            Path(__file__).parent.parent / "data" / "seo_history.json"
        )
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict:
        """Load existing history or create new."""
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text())
            except json.JSONDecodeError:
                return self._new_history()
        return self._new_history()

    def _new_history(self) -> Dict:
        """Create empty history structure."""
        return {
            "domain": "",
            "created_at": datetime.now().isoformat(),
            "snapshots": [],
            "priority_keywords": {}  # keyword -> [{date, position, impressions, clicks}]
        }

    def _save(self) -> None:
        """Persist history to disk."""
        self.history_file.write_text(json.dumps(self.data, indent=2, default=str))

    def add_snapshot(self, report_data: Dict) -> Dict:
        """
        Add a weekly snapshot from a WeeklyReport.

        Returns dict with changes from last snapshot.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Store domain
        if report_data.get("domain"):
            self.data["domain"] = report_data["domain"]

        # Create snapshot
        snapshot = {
            "date": today,
            "quick_wins_count": len(report_data.get("quick_wins", [])),
            "declining_content_count": len(report_data.get("declining_content", [])),
            "priority_ranking_count": 0,
            "priority_total": 0,
        }

        # Track priority keywords individually
        changes = {"improved": [], "declined": [], "new_rankings": [], "lost_rankings": []}

        for kw in report_data.get("priority_tracking", []):
            keyword = kw.get("keyword", "")
            position = kw.get("current_position")
            impressions = kw.get("impressions", 0)
            clicks = kw.get("clicks", 0)

            snapshot["priority_total"] += 1
            if isinstance(position, (int, float)) and position > 0:
                snapshot["priority_ranking_count"] += 1

            # Initialize keyword history if needed
            if keyword not in self.data["priority_keywords"]:
                self.data["priority_keywords"][keyword] = []

            # Get previous position for comparison
            history = self.data["priority_keywords"][keyword]
            prev_position = None
            if history:
                last_entry = history[-1]
                prev_pos = last_entry.get("position")
                if isinstance(prev_pos, (int, float)) and prev_pos > 0:
                    prev_position = prev_pos

            # Calculate change
            current_pos = position if isinstance(position, (int, float)) and position > 0 else None

            if prev_position and current_pos:
                change = prev_position - current_pos  # Positive = improved
                if change >= 3:
                    changes["improved"].append({
                        "keyword": keyword,
                        "from": prev_position,
                        "to": current_pos,
                        "change": change
                    })
                elif change <= -3:
                    changes["declined"].append({
                        "keyword": keyword,
                        "from": prev_position,
                        "to": current_pos,
                        "change": change
                    })
            elif current_pos and not prev_position:
                changes["new_rankings"].append({
                    "keyword": keyword,
                    "position": current_pos
                })
            elif prev_position and not current_pos:
                changes["lost_rankings"].append({
                    "keyword": keyword,
                    "was": prev_position
                })

            # Add new data point
            self.data["priority_keywords"][keyword].append({
                "date": today,
                "position": position if isinstance(position, (int, float)) else None,
                "impressions": impressions,
                "clicks": clicks
            })

            # Keep only last 12 weeks per keyword
            if len(self.data["priority_keywords"][keyword]) > 12:
                self.data["priority_keywords"][keyword] = \
                    self.data["priority_keywords"][keyword][-12:]

        # Add snapshot
        self.data["snapshots"].append(snapshot)

        # Keep only last 12 snapshots
        if len(self.data["snapshots"]) > 12:
            self.data["snapshots"] = self.data["snapshots"][-12:]

        self._save()

        return changes

    def get_keyword_trend(self, keyword: str, weeks: int = 4) -> List[Dict]:
        """Get position history for a specific keyword."""
        history = self.data["priority_keywords"].get(keyword, [])
        return history[-weeks:] if history else []

    def export_markdown(self, output_path: Optional[Path] = None) -> str:
        """
        Export historical data as markdown tables.

        Returns markdown string, optionally saves to file.
        """
        md = []
        md.append("# SEO Progress Tracking")
        md.append(f"**Domain:** {self.data.get('domain', 'Not set')}")
        md.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
        md.append("")
        md.append("---")
        md.append("")

        # Overview table - weekly snapshots
        if self.data["snapshots"]:
            md.append("## Weekly Overview")
            md.append("")
            md.append("| Week | Priority Ranking | Quick Wins | Declining |")
            md.append("|------|------------------|------------|-----------|")

            for snap in self.data["snapshots"][-8:]:  # Last 8 weeks
                date = snap.get("date", "")
                ranking = f"{snap.get('priority_ranking_count', 0)}/{snap.get('priority_total', 0)}"
                quick = snap.get("quick_wins_count", 0)
                declining = snap.get("declining_content_count", 0)
                md.append(f"| {date} | {ranking} | {quick} | {declining} |")

            md.append("")
            md.append("---")
            md.append("")

        # Priority keyword tracking table
        if self.data["priority_keywords"]:
            md.append("## Priority Keyword Positions")
            md.append("")
            md.append("Position history for target keywords (last 4 weeks).")
            md.append("")

            # Build header with last 4 dates
            all_dates = set()
            for history in self.data["priority_keywords"].values():
                for entry in history[-4:]:
                    all_dates.add(entry.get("date", ""))

            dates = sorted(all_dates)[-4:]  # Last 4 unique dates

            if dates:
                header = "| Keyword |"
                separator = "|---------|"
                for d in dates:
                    # Short date format
                    short_date = d[5:] if len(d) >= 10 else d  # MM-DD from YYYY-MM-DD
                    header += f" {short_date} |"
                    separator += "--------|"

                md.append(header)
                md.append(separator)

                # Sort keywords by most recent position (ranking first)
                sorted_keywords = []
                for keyword, history in self.data["priority_keywords"].items():
                    if history:
                        last_pos = history[-1].get("position")
                        if isinstance(last_pos, (int, float)) and last_pos > 0:
                            sorted_keywords.append((keyword, last_pos))
                        else:
                            sorted_keywords.append((keyword, 999))
                    else:
                        sorted_keywords.append((keyword, 999))

                sorted_keywords.sort(key=lambda x: x[1])

                for keyword, _ in sorted_keywords:
                    history = self.data["priority_keywords"][keyword]

                    # Create lookup by date
                    date_lookup = {}
                    for entry in history:
                        date_lookup[entry.get("date", "")] = entry.get("position")

                    row = f"| {keyword[:30]} |"
                    prev_pos = None

                    for d in dates:
                        pos = date_lookup.get(d)
                        if isinstance(pos, (int, float)) and pos > 0:
                            # Add trend indicator
                            if prev_pos:
                                if pos < prev_pos:
                                    row += f" #{pos:.0f} ↑ |"
                                elif pos > prev_pos:
                                    row += f" #{pos:.0f} ↓ |"
                                else:
                                    row += f" #{pos:.0f} |"
                            else:
                                row += f" #{pos:.0f} |"
                            prev_pos = pos
                        else:
                            row += " - |"
                            prev_pos = None

                    md.append(row)

            md.append("")
            md.append("---")
            md.append("")

        # Movers section
        md.append("## Recent Movers")
        md.append("")

        # Find biggest movers in last snapshot
        if len(self.data["snapshots"]) >= 2:
            movers = []
            for keyword, history in self.data["priority_keywords"].items():
                if len(history) >= 2:
                    last = history[-1].get("position")
                    prev = history[-2].get("position")
                    if isinstance(last, (int, float)) and isinstance(prev, (int, float)):
                        if last > 0 and prev > 0:
                            change = prev - last
                            if abs(change) >= 2:
                                movers.append({
                                    "keyword": keyword,
                                    "from": prev,
                                    "to": last,
                                    "change": change
                                })

            if movers:
                movers.sort(key=lambda x: x["change"], reverse=True)

                improved = [m for m in movers if m["change"] > 0]
                declined = [m for m in movers if m["change"] < 0]

                if improved:
                    md.append("**Improved:**")
                    for m in improved[:5]:
                        md.append(f"- {m['keyword']}: #{m['from']:.0f} → #{m['to']:.0f} (+{m['change']:.0f})")
                    md.append("")

                if declined:
                    md.append("**Declined:**")
                    for m in declined[:5]:
                        md.append(f"- {m['keyword']}: #{m['from']:.0f} → #{m['to']:.0f} ({m['change']:.0f})")
                    md.append("")
            else:
                md.append("No significant position changes since last report.")
                md.append("")
        else:
            md.append("Need at least 2 snapshots to show movers. Run report again next week.")
            md.append("")

        result = "\n".join(md)

        if output_path:
            output_path.write_text(result)
            print(f"Saved history to: {output_path}")

        return result

    def get_summary(self) -> Dict:
        """Get summary stats for quick display."""
        if not self.data["snapshots"]:
            return {"status": "No data yet", "snapshots": 0}

        latest = self.data["snapshots"][-1]

        summary = {
            "snapshots": len(self.data["snapshots"]),
            "keywords_tracked": len(self.data["priority_keywords"]),
            "latest_date": latest.get("date"),
            "ranking_count": latest.get("priority_ranking_count", 0),
            "ranking_total": latest.get("priority_total", 0),
        }

        # Compare to previous if available
        if len(self.data["snapshots"]) >= 2:
            prev = self.data["snapshots"][-2]
            summary["ranking_change"] = (
                latest.get("priority_ranking_count", 0) -
                prev.get("priority_ranking_count", 0)
            )

        return summary


def main():
    """CLI for history management."""
    import argparse

    parser = argparse.ArgumentParser(description="SEO History Manager")
    parser.add_argument("--export", action="store_true", help="Export to markdown")
    parser.add_argument("--summary", action="store_true", help="Show summary")
    parser.add_argument("--output", help="Output file for export")

    args = parser.parse_args()

    history = SEOHistory()

    if args.summary:
        summary = history.get_summary()
        print("SEO History Summary:")
        print(f"  Snapshots: {summary.get('snapshots', 0)}")
        print(f"  Keywords tracked: {summary.get('keywords_tracked', 0)}")
        if summary.get('latest_date'):
            print(f"  Latest: {summary['latest_date']}")
            print(f"  Ranking: {summary.get('ranking_count', 0)}/{summary.get('ranking_total', 0)}")

    if args.export:
        output_path = Path(args.output) if args.output else None
        md = history.export_markdown(output_path)
        if not output_path:
            print(md)


if __name__ == "__main__":
    main()
