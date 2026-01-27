#!/usr/bin/env python3
"""
HubSpot Deep Dive Explorer

Comprehensive exploration of HubSpot CRM data to surface:
- All contact properties (custom + HubSpot)
- All forms and submission patterns
- All lists with member counts
- Source attribution breakdown
- Curriculove-specific data
- Landing page conversions
- Time-based signup patterns

Outputs detailed markdown report to reports/hubspot-audit-YYYY-MM-DD.md

Usage:
    python hubspot_deep_dive.py
    python hubspot_deep_dive.py --output console
    python hubspot_deep_dive.py --days 90
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter

# Add seomachine to path for module imports
seomachine_path = Path(__file__).parent.parent / "SEO Content Production" / "seomachine"
sys.path.insert(0, str(seomachine_path))

from dotenv import load_dotenv
load_dotenv(seomachine_path / 'data_sources/config/.env')

from data_sources.modules.hubspot import HubSpotAnalytics


class HubSpotDeepDive:
    """Comprehensive HubSpot data exploration and reporting"""

    def __init__(self, days: int = 30):
        self.hs = HubSpotAnalytics()
        self.days = days
        self.report_data = {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "sections": [],
        }

    def explore_all(self) -> dict:
        """Run all exploration methods"""
        print("Starting HubSpot Deep Dive...")
        print(f"Period: Last {self.days} days")
        print("=" * 60)

        self._explore_properties()
        self._explore_forms()
        self._explore_lists()
        self._explore_sources()
        self._explore_landing_pages()
        self._explore_curriculove()
        self._explore_funnel()
        self._explore_time_patterns()
        self._explore_states()

        print("\n" + "=" * 60)
        print("Deep dive complete!")

        return self.report_data

    def _add_section(self, title: str, content: dict):
        """Add a section to the report"""
        self.report_data["sections"].append({
            "title": title,
            "content": content
        })

    def _explore_properties(self):
        """Explore all contact properties"""
        print("\n[1/9] Exploring contact properties...")

        properties = self.hs.get_contact_properties()

        custom_props = [p for p in properties if not p['hubspot_defined']]
        hubspot_props = [p for p in properties if p['hubspot_defined']]

        # Find attribution-related properties
        attribution_keywords = ['source', 'campaign', 'medium', 'first', 'recent', 'original', 'conversion', 'form', 'page', 'referrer']
        attribution_props = [
            p for p in hubspot_props
            if any(kw in p["name"].lower() for kw in attribution_keywords)
        ]

        # Find Curriculove-related
        curriculove_props = [p for p in custom_props if 'curriculove' in p["name"].lower()]

        self._add_section("Contact Properties", {
            "total": len(properties),
            "custom_count": len(custom_props),
            "hubspot_count": len(hubspot_props),
            "custom_properties": [{"name": p["name"], "label": p["label"], "type": p["type"]} for p in custom_props],
            "attribution_properties": [{"name": p["name"], "label": p["label"]} for p in attribution_props],
            "curriculove_properties": [{"name": p["name"], "label": p["label"], "type": p["type"]} for p in curriculove_props],
        })

        print(f"   Found {len(custom_props)} custom, {len(hubspot_props)} HubSpot properties")
        print(f"   Curriculove-related: {len(curriculove_props)}")

    def _explore_forms(self):
        """Explore all marketing forms"""
        print("\n[2/9] Exploring marketing forms...")

        forms = self.hs.get_forms()
        form_conversions = self.hs.get_form_conversions(days=self.days, max_contacts=5000)

        forms_with_data = []
        for form in forms:
            form_name = form["name"]
            conversion_count = form_conversions.get(form_name, 0)
            forms_with_data.append({
                "name": form_name,
                "id": form["id"],
                "type": form["type"],
                "conversions": conversion_count,
                "fields": form["fields"][:10],  # First 10 fields
            })

        # Sort by conversions
        forms_with_data.sort(key=lambda x: -x["conversions"])

        self._add_section("Marketing Forms", {
            "total": len(forms),
            "forms": forms_with_data[:20],  # Top 20
            "total_conversions": sum(f["conversions"] for f in forms_with_data),
        })

        print(f"   Found {len(forms)} forms")
        if forms_with_data:
            print(f"   Top form: {forms_with_data[0]['name']} ({forms_with_data[0]['conversions']} conversions)")

    def _explore_lists(self):
        """Explore contact lists"""
        print("\n[3/9] Exploring contact lists...")

        lists = self.hs.get_lists()

        self._add_section("Contact Lists", {
            "total": len(lists),
            "total_members": sum(l["count"] for l in lists),
            "lists": lists[:25],  # Top 25 by count
        })

        print(f"   Found {len(lists)} lists")
        if lists:
            print(f"   Largest: {lists[0]['name']} ({lists[0]['count']:,} contacts)")

    def _explore_sources(self):
        """Explore traffic source breakdown"""
        print("\n[4/9] Exploring source attribution...")

        sources = self.hs.get_contacts_by_source(days=self.days, max_contacts=5000)
        source_detail = self.hs.get_contacts_by_source_detail(days=self.days, max_contacts=5000)
        source_to_lead = self.hs.get_source_to_lead_rate(days=self.days, max_contacts=5000)

        total = sum(sources.values())

        self._add_section("Source Attribution", {
            "total_contacts": total,
            "by_source": sources,
            "by_source_detail": source_detail,
            "source_to_lead_rate": source_to_lead,
        })

        print(f"   Analyzed {total:,} contacts")
        for source, count in list(sources.items())[:5]:
            pct = count / total * 100 if total > 0 else 0
            rate = source_to_lead.get(source, {}).get("rate", 0)
            print(f"   {source}: {count:,} ({pct:.1f}%) - {rate:.1f}% to lead")

    def _explore_landing_pages(self):
        """Explore landing page conversions"""
        print("\n[5/9] Exploring landing page conversions...")

        pages = self.hs.get_landing_page_conversions(days=self.days, max_contacts=5000)

        # Categorize pages
        blog_pages = [p for p in pages if '/blog/' in p['url'] or '/education-hub/' in p['url']]
        home_pages = [p for p in pages if p['url'].rstrip('/').endswith('.co') or p['url'].rstrip('/').endswith('.com')]
        other_pages = [p for p in pages if p not in blog_pages and p not in home_pages]

        self._add_section("Landing Page Conversions", {
            "total_pages": len(pages),
            "total_conversions": sum(p["count"] for p in pages),
            "top_pages": pages[:20],
            "blog_pages": blog_pages[:10],
            "home_pages": home_pages[:5],
            "other_top": other_pages[:10],
        })

        print(f"   Found {len(pages)} unique landing pages")
        if pages:
            print(f"   Top: {pages[0]['url'][:50]}... ({pages[0]['count']} conversions)")

    def _explore_curriculove(self):
        """Explore Curriculove lead magnet data"""
        print("\n[6/9] Exploring Curriculove data...")

        curriculove = self.hs.get_curriculove_leads(days=self.days, max_contacts=5000)

        self._add_section("Curriculove Lead Magnet", {
            "total_leads": curriculove["total"],
            "by_philosophy": curriculove["by_philosophy"],
            "by_confidence": curriculove["by_confidence"],
            "by_state": curriculove["by_state"],
            "by_source": curriculove["by_source"],
        })

        print(f"   Total Curriculove leads: {curriculove['total']:,}")
        if curriculove["by_philosophy"]:
            top_phil = list(curriculove["by_philosophy"].items())[0]
            print(f"   Top philosophy: {top_phil[0]} ({top_phil[1]})")

    def _explore_funnel(self):
        """Explore funnel conversion rates"""
        print("\n[7/9] Exploring funnel metrics...")

        funnel = self.hs.get_funnel_conversion_rates(days=self.days, max_contacts=5000)

        self._add_section("Funnel Conversion", {
            "total_contacts": funnel["total_contacts"],
            "stages": funnel["stages"],
            "conversion_rates": funnel["conversion_rates"],
        })

        print(f"   Total contacts: {funnel['total_contacts']:,}")
        for stage, count in funnel["stages"].items():
            print(f"   {stage}: {count:,}")
        print(f"   Subscriber->Lead: {funnel['conversion_rates']['subscriber_to_lead']:.1f}%")

    def _explore_time_patterns(self):
        """Explore time-based signup patterns"""
        print("\n[8/9] Exploring time patterns...")

        weekly = self.hs.get_weekly_signups(weeks=12)
        monthly = self.hs.get_monthly_signups(months=6)

        # Calculate trends
        if len(weekly) >= 2:
            recent = sum(w["count"] for w in weekly[-4:])  # Last 4 weeks
            previous = sum(w["count"] for w in weekly[-8:-4])  # 4 weeks before
            weekly_trend = ((recent - previous) / previous * 100) if previous > 0 else 0
        else:
            weekly_trend = 0

        self._add_section("Time Patterns", {
            "weekly_signups": weekly,
            "monthly_signups": monthly,
            "weekly_trend_pct": round(weekly_trend, 1),
        })

        print(f"   Analyzed {len(weekly)} weeks, {len(monthly)} months")
        if weekly:
            print(f"   Latest week: {weekly[-1]['count']} signups")
        print(f"   4-week trend: {'+' if weekly_trend >= 0 else ''}{weekly_trend:.1f}%")

    def _explore_states(self):
        """Explore state-level distribution"""
        print("\n[9/9] Exploring state distribution...")

        states = self.hs.get_leads_by_state(days=self.days, max_contacts=5000)

        # OpenEd operating states
        operating_states = ['AR', 'IN', 'IA', 'KS', 'MN', 'MT', 'NV', 'OR', 'UT']
        operating_count = sum(states.get(s, 0) for s in operating_states)
        total = sum(states.values())

        self._add_section("State Distribution", {
            "total_with_state": total,
            "by_state": states,
            "operating_states_total": operating_count,
            "operating_states_pct": round(operating_count / total * 100, 1) if total > 0 else 0,
        })

        print(f"   {total:,} contacts with state data")
        print(f"   Operating states: {operating_count:,} ({operating_count/total*100:.1f}%)" if total else "")

    def format_markdown(self) -> str:
        """Format report as markdown"""
        lines = []
        lines.append("# HubSpot Deep Dive Audit")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Period:** Last {self.days} days")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        for i, section in enumerate(self.report_data["sections"], 1):
            anchor = section["title"].lower().replace(" ", "-")
            lines.append(f"{i}. [{section['title']}](#{anchor})")
        lines.append("")

        # Each section
        for section in self.report_data["sections"]:
            lines.append(f"## {section['title']}")
            lines.append("")

            content = section["content"]

            if section["title"] == "Contact Properties":
                lines.append(f"**Total properties:** {content['total']}")
                lines.append(f"- Custom: {content['custom_count']}")
                lines.append(f"- HubSpot: {content['hubspot_count']}")
                lines.append("")

                if content["curriculove_properties"]:
                    lines.append("### Curriculove Properties")
                    lines.append("")
                    lines.append("| Name | Label | Type |")
                    lines.append("|------|-------|------|")
                    for p in content["curriculove_properties"]:
                        lines.append(f"| `{p['name']}` | {p['label']} | {p['type']} |")
                    lines.append("")

                if content["custom_properties"]:
                    lines.append("### All Custom Properties")
                    lines.append("")
                    lines.append("| Name | Label | Type |")
                    lines.append("|------|-------|------|")
                    for p in content["custom_properties"][:30]:
                        lines.append(f"| `{p['name']}` | {p['label']} | {p['type']} |")
                    if len(content["custom_properties"]) > 30:
                        lines.append(f"| ... | *{len(content['custom_properties']) - 30} more* | |")
                    lines.append("")

            elif section["title"] == "Marketing Forms":
                lines.append(f"**Total forms:** {content['total']}")
                lines.append(f"**Total conversions (period):** {content['total_conversions']:,}")
                lines.append("")

                if content["forms"]:
                    lines.append("### Top Forms by Conversions")
                    lines.append("")
                    lines.append("| Form | Type | Conversions |")
                    lines.append("|------|------|-------------|")
                    for f in content["forms"][:15]:
                        lines.append(f"| {f['name'][:50]} | {f['type']} | {f['conversions']:,} |")
                    lines.append("")

            elif section["title"] == "Contact Lists":
                lines.append(f"**Total lists:** {content['total']}")
                lines.append(f"**Total members:** {content['total_members']:,}")
                lines.append("")

                if content["lists"]:
                    lines.append("### Top Lists by Size")
                    lines.append("")
                    lines.append("| List | Members | Type |")
                    lines.append("|------|---------|------|")
                    for lst in content["lists"][:15]:
                        lines.append(f"| {lst['name'][:50]} | {lst['count']:,} | {lst['type']} |")
                    lines.append("")

            elif section["title"] == "Source Attribution":
                lines.append(f"**Total contacts:** {content['total_contacts']:,}")
                lines.append("")

                lines.append("### By Source")
                lines.append("")
                lines.append("| Source | Count | % | Lead Rate |")
                lines.append("|--------|-------|---|-----------|")
                total = content["total_contacts"]
                for source, count in content["by_source"].items():
                    pct = count / total * 100 if total > 0 else 0
                    rate = content["source_to_lead_rate"].get(source, {}).get("rate", 0)
                    lines.append(f"| {source} | {count:,} | {pct:.1f}% | {rate:.1f}% |")
                lines.append("")

                # Source detail
                if content["by_source_detail"]:
                    lines.append("### Source Detail Breakdown")
                    lines.append("")
                    for source, details in content["by_source_detail"].items():
                        lines.append(f"**{source}:**")
                        for detail, cnt in list(details.items())[:5]:
                            lines.append(f"- {detail}: {cnt}")
                        lines.append("")

            elif section["title"] == "Landing Page Conversions":
                lines.append(f"**Total unique pages:** {content['total_pages']}")
                lines.append(f"**Total conversions:** {content['total_conversions']:,}")
                lines.append("")

                if content["top_pages"]:
                    lines.append("### Top Landing Pages")
                    lines.append("")
                    lines.append("| Page | Conversions | Top Source |")
                    lines.append("|------|-------------|------------|")
                    for p in content["top_pages"][:15]:
                        url_short = p['url'][:60] + "..." if len(p['url']) > 60 else p['url']
                        lines.append(f"| {url_short} | {p['count']:,} | {p['top_source']} |")
                    lines.append("")

            elif section["title"] == "Curriculove Lead Magnet":
                lines.append(f"**Total Curriculove leads:** {content['total_leads']:,}")
                lines.append("")

                if content["by_philosophy"]:
                    lines.append("### By Philosophy")
                    lines.append("")
                    for phil, count in content["by_philosophy"].items():
                        lines.append(f"- {phil}: {count}")
                    lines.append("")

                if content["by_confidence"]:
                    lines.append("### By Confidence Level")
                    lines.append("")
                    for conf, count in content["by_confidence"].items():
                        lines.append(f"- {conf}: {count}")
                    lines.append("")

                if content["by_source"]:
                    lines.append("### By Source")
                    lines.append("")
                    for src, count in list(content["by_source"].items())[:10]:
                        lines.append(f"- {src}: {count}")
                    lines.append("")

            elif section["title"] == "Funnel Conversion":
                lines.append(f"**Total contacts:** {content['total_contacts']:,}")
                lines.append("")

                lines.append("### Stage Distribution")
                lines.append("")
                for stage, count in content["stages"].items():
                    lines.append(f"- {stage}: {count:,}")
                lines.append("")

                lines.append("### Conversion Rates")
                lines.append("")
                for rate_name, rate_value in content["conversion_rates"].items():
                    readable = rate_name.replace("_", " ").title()
                    lines.append(f"- {readable}: {rate_value:.1f}%")
                lines.append("")

            elif section["title"] == "Time Patterns":
                lines.append(f"**4-Week Trend:** {'+' if content['weekly_trend_pct'] >= 0 else ''}{content['weekly_trend_pct']:.1f}%")
                lines.append("")

                if content["weekly_signups"]:
                    lines.append("### Weekly Signups (Last 12 Weeks)")
                    lines.append("")
                    lines.append("| Week | Signups |")
                    lines.append("|------|---------|")
                    for w in content["weekly_signups"][-12:]:
                        lines.append(f"| {w['week_start']} | {w['count']} |")
                    lines.append("")

                if content["monthly_signups"]:
                    lines.append("### Monthly Signups")
                    lines.append("")
                    for m in content["monthly_signups"]:
                        lines.append(f"- {m['month']}: {m['count']}")
                    lines.append("")

            elif section["title"] == "State Distribution":
                lines.append(f"**Contacts with state:** {content['total_with_state']:,}")
                lines.append(f"**Operating states:** {content['operating_states_total']:,} ({content['operating_states_pct']:.1f}%)")
                lines.append("")

                if content["by_state"]:
                    lines.append("### Top States")
                    lines.append("")
                    lines.append("| State | Count |")
                    lines.append("|-------|-------|")
                    for state, count in list(content["by_state"].items())[:20]:
                        marker = " *" if state in ['AR', 'IN', 'IA', 'KS', 'MN', 'MT', 'NV', 'OR', 'UT'] else ""
                        lines.append(f"| {state}{marker} | {count:,} |")
                    lines.append("")
                    lines.append("*\\* = Operating state*")
                    lines.append("")

            lines.append("---")
            lines.append("")

        # Footer
        lines.append("## Key Insights")
        lines.append("")
        lines.append("*Add your analysis notes here after reviewing the data.*")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"*Report generated by `hubspot_deep_dive.py` on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

        return "\n".join(lines)

    def format_console(self) -> str:
        """Format report for console output"""
        lines = []
        lines.append("=" * 60)
        lines.append("HUBSPOT DEEP DIVE AUDIT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"Period: Last {self.days} days")
        lines.append("=" * 60)

        for section in self.report_data["sections"]:
            lines.append("")
            lines.append(f"--- {section['title'].upper()} ---")
            content = section["content"]

            # Simplified console output
            if "total" in content:
                lines.append(f"Total: {content['total']}")
            if "total_contacts" in content:
                lines.append(f"Total contacts: {content['total_contacts']:,}")
            if "by_source" in content:
                for source, count in list(content["by_source"].items())[:5]:
                    lines.append(f"  {source}: {count:,}")
            if "stages" in content:
                for stage, count in content["stages"].items():
                    lines.append(f"  {stage}: {count:,}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='HubSpot Deep Dive Audit')
    parser.add_argument(
        '--output',
        choices=['console', 'markdown'],
        default='markdown',
        help='Output format'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze'
    )
    parser.add_argument(
        '--save',
        help='Save output to specific file path'
    )
    args = parser.parse_args()

    # Run deep dive
    dive = HubSpotDeepDive(days=args.days)
    dive.explore_all()

    # Format output
    if args.output == 'console':
        output = dive.format_console()
        print(output)
    else:
        output = dive.format_markdown()
        print("\n" + output[:2000] + "...\n(truncated for console)")

    # Save report
    if args.save:
        save_path = Path(args.save)
    else:
        reports_dir = Path(__file__).parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        save_path = reports_dir / f"hubspot-audit-{datetime.now().strftime('%Y-%m-%d')}.md"

    save_path.write_text(output)
    print(f"\nFull report saved to: {save_path}")


if __name__ == "__main__":
    main()
