#!/usr/bin/env python3
"""
Weekly HubSpot Attribution Report

Generates a consolidated report of subscriber attribution and funnel performance.
Run alongside weekly_social_report.py and weekly_seo_report.py for full marketing analytics.

Usage:
    python weekly_hubspot_report.py --output markdown --save report.md
    python weekly_hubspot_report.py --output console
    python weekly_hubspot_report.py --days 14
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / 'data_sources/config/.env')

from data_sources.modules.hubspot import HubSpotAnalytics


class WeeklyHubSpotReport:
    """Generate weekly HubSpot attribution report"""

    def __init__(self, days: int = 7):
        self.days = days
        self.data = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'attribution': None,
            'landing_pages': None,
            'forms': None,
            'curriculove': None,
            'funnel': None,
            'trends': None,
            'errors': [],
        }

    def collect_attribution(self):
        """Collect source attribution data"""
        try:
            hs = HubSpotAnalytics()

            sources = hs.get_contacts_by_source(days=self.days, max_contacts=5000)
            source_rates = hs.get_source_to_lead_rate(days=self.days, max_contacts=5000)

            total = sum(sources.values())

            self.data['attribution'] = {
                'total_contacts': total,
                'by_source': sources,
                'source_rates': source_rates,
            }

        except Exception as e:
            self.data['errors'].append(f'Attribution error: {str(e)}')

    def collect_landing_pages(self):
        """Collect landing page conversion data"""
        try:
            hs = HubSpotAnalytics()

            pages = hs.get_landing_page_conversions(days=self.days, max_contacts=5000)

            # Categorize
            blog = [p for p in pages if '/blog/' in p['url'] or '/education-hub/' in p['url']]
            homepage = [p for p in pages if p['url'].rstrip('/').endswith('.co')]

            self.data['landing_pages'] = {
                'total_pages': len(pages),
                'top_pages': pages[:10],
                'blog_conversions': sum(p['count'] for p in blog),
                'homepage_conversions': sum(p['count'] for p in homepage),
            }

        except Exception as e:
            self.data['errors'].append(f'Landing pages error: {str(e)}')

    def collect_forms(self):
        """Collect form submission data"""
        try:
            hs = HubSpotAnalytics()

            forms = hs.get_form_conversions(days=self.days, max_contacts=5000)

            self.data['forms'] = {
                'total_submissions': sum(forms.values()),
                'by_form': forms,
            }

        except Exception as e:
            self.data['errors'].append(f'Forms error: {str(e)}')

    def collect_curriculove(self):
        """Collect Curriculove lead magnet data"""
        try:
            hs = HubSpotAnalytics()

            curriculove = hs.get_curriculove_leads(days=self.days, max_contacts=5000)

            self.data['curriculove'] = curriculove

        except Exception as e:
            self.data['errors'].append(f'Curriculove error: {str(e)}')

    def collect_funnel(self):
        """Collect funnel conversion data"""
        try:
            hs = HubSpotAnalytics()

            funnel = hs.get_funnel_conversion_rates(days=self.days, max_contacts=5000)

            self.data['funnel'] = funnel

        except Exception as e:
            self.data['errors'].append(f'Funnel error: {str(e)}')

    def collect_trends(self):
        """Collect week-over-week trend data"""
        try:
            hs = HubSpotAnalytics()

            # Get last 4 weeks for trends
            weekly = hs.get_weekly_signups(weeks=4)

            if len(weekly) >= 2:
                current = weekly[-1]['count'] if weekly else 0
                previous = weekly[-2]['count'] if len(weekly) > 1 else 0
                wow_change = ((current - previous) / previous * 100) if previous > 0 else 0
            else:
                current = previous = wow_change = 0

            self.data['trends'] = {
                'weekly_signups': weekly,
                'current_week': current,
                'previous_week': previous,
                'wow_change_pct': round(wow_change, 1),
            }

        except Exception as e:
            self.data['errors'].append(f'Trends error: {str(e)}')

    def collect_all(self):
        """Collect data from all sources"""
        print("Collecting attribution data...")
        self.collect_attribution()

        print("Collecting landing page data...")
        self.collect_landing_pages()

        print("Collecting form data...")
        self.collect_forms()

        print("Collecting Curriculove data...")
        self.collect_curriculove()

        print("Collecting funnel data...")
        self.collect_funnel()

        print("Collecting trend data...")
        self.collect_trends()

    def format_markdown(self) -> str:
        """Format report as markdown"""
        lines = []
        lines.append(f"# Weekly HubSpot Attribution Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Period:** Last {self.days} days")
        lines.append("")

        # Quick Summary
        lines.append("## Quick Summary")
        lines.append("")

        if self.data['attribution']:
            attr = self.data['attribution']
            lines.append(f"- **New Contacts:** {attr['total_contacts']:,}")

        if self.data['trends']:
            trends = self.data['trends']
            sign = '+' if trends['wow_change_pct'] >= 0 else ''
            lines.append(f"- **Week-over-Week:** {sign}{trends['wow_change_pct']:.1f}%")

        if self.data['curriculove']:
            curr = self.data['curriculove']
            lines.append(f"- **Curriculove Leads:** {curr['total']}")

        if self.data['funnel']:
            funnel = self.data['funnel']
            lines.append(f"- **Subscriber→Lead Rate:** {funnel['conversion_rates']['subscriber_to_lead']:.1f}%")

        lines.append("")

        # Attribution Section
        if self.data['attribution']:
            attr = self.data['attribution']
            lines.append("## Source Attribution")
            lines.append("")
            lines.append("| Source | Contacts | % | Lead Rate |")
            lines.append("|--------|----------|---|-----------|")

            total = attr['total_contacts']
            for source, count in attr['by_source'].items():
                pct = count / total * 100 if total > 0 else 0
                rate = attr['source_rates'].get(source, {}).get('rate', 0)
                lines.append(f"| {source} | {count:,} | {pct:.1f}% | {rate:.1f}% |")

            lines.append("")

        # Landing Pages Section
        if self.data['landing_pages']:
            lp = self.data['landing_pages']
            lines.append("## Top Landing Pages")
            lines.append("")
            lines.append(f"*Blog conversions: {lp['blog_conversions']} | Homepage: {lp['homepage_conversions']}*")
            lines.append("")
            lines.append("| Page | Conversions | Source |")
            lines.append("|------|-------------|--------|")

            for page in lp['top_pages'][:10]:
                url_short = page['url'][:50] + "..." if len(page['url']) > 50 else page['url']
                lines.append(f"| {url_short} | {page['count']} | {page['top_source']} |")

            lines.append("")

        # Forms Section
        if self.data['forms']:
            forms = self.data['forms']
            lines.append("## Form Submissions")
            lines.append("")
            lines.append(f"**Total:** {forms['total_submissions']:,}")
            lines.append("")
            lines.append("| Form | Submissions |")
            lines.append("|------|-------------|")

            for form, count in list(forms['by_form'].items())[:10]:
                form_short = form[:40] + "..." if len(form) > 40 else form
                lines.append(f"| {form_short} | {count:,} |")

            lines.append("")

        # Curriculove Section
        if self.data['curriculove'] and self.data['curriculove']['total'] > 0:
            curr = self.data['curriculove']
            lines.append("## Curriculove Lead Magnet")
            lines.append("")
            lines.append(f"**Total Leads:** {curr['total']}")
            lines.append("")

            if curr['by_philosophy']:
                lines.append("### By Philosophy")
                lines.append("")
                for phil, count in list(curr['by_philosophy'].items())[:5]:
                    lines.append(f"- {phil}: {count}")
                lines.append("")

            if curr['by_source']:
                lines.append("### By Source")
                lines.append("")
                for src, count in list(curr['by_source'].items())[:5]:
                    lines.append(f"- {src}: {count}")
                lines.append("")

        # Funnel Section
        if self.data['funnel']:
            funnel = self.data['funnel']
            lines.append("## Funnel Metrics")
            lines.append("")
            lines.append("### Stage Distribution")
            lines.append("")

            for stage, count in funnel['stages'].items():
                lines.append(f"- {stage}: {count:,}")
            lines.append("")

            lines.append("### Conversion Rates")
            lines.append("")

            for rate_name, rate_value in funnel['conversion_rates'].items():
                readable = rate_name.replace("_", " → ").replace("to", "").title().strip()
                lines.append(f"- {readable}: {rate_value:.1f}%")
            lines.append("")

        # Trends Section
        if self.data['trends']:
            trends = self.data['trends']
            lines.append("## Week-over-Week Trends")
            lines.append("")
            lines.append(f"- Current week: {trends['current_week']} signups")
            lines.append(f"- Previous week: {trends['previous_week']} signups")
            sign = '+' if trends['wow_change_pct'] >= 0 else ''
            lines.append(f"- Change: {sign}{trends['wow_change_pct']:.1f}%")
            lines.append("")

        # Errors
        if self.data['errors']:
            lines.append("## Errors")
            lines.append("")
            for error in self.data['errors']:
                lines.append(f"- {error}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(f"*Generated by `weekly_hubspot_report.py`*")

        return '\n'.join(lines)

    def format_console(self) -> str:
        """Format report for console output"""
        lines = []
        lines.append("=" * 60)
        lines.append("WEEKLY HUBSPOT ATTRIBUTION REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"Period: Last {self.days} days")
        lines.append("=" * 60)
        lines.append("")

        if self.data['attribution']:
            attr = self.data['attribution']
            lines.append(f"📊 ATTRIBUTION ({attr['total_contacts']:,} contacts)")
            for source, count in list(attr['by_source'].items())[:5]:
                rate = attr['source_rates'].get(source, {}).get('rate', 0)
                lines.append(f"   {source}: {count:,} ({rate:.1f}% lead rate)")
            lines.append("")

        if self.data['landing_pages']:
            lp = self.data['landing_pages']
            lines.append(f"📄 TOP LANDING PAGES")
            for page in lp['top_pages'][:5]:
                lines.append(f"   {page['url'][:50]}: {page['count']}")
            lines.append("")

        if self.data['curriculove']:
            curr = self.data['curriculove']
            lines.append(f"🎓 CURRICULOVE: {curr['total']} leads")
            for phil, count in list(curr['by_philosophy'].items())[:3]:
                lines.append(f"   {phil}: {count}")
            lines.append("")

        if self.data['funnel']:
            funnel = self.data['funnel']
            lines.append(f"📈 FUNNEL")
            for stage, count in funnel['stages'].items():
                lines.append(f"   {stage}: {count:,}")
            lines.append(f"   Subscriber→Lead: {funnel['conversion_rates']['subscriber_to_lead']:.1f}%")
            lines.append("")

        if self.data['trends']:
            trends = self.data['trends']
            sign = '+' if trends['wow_change_pct'] >= 0 else ''
            lines.append(f"📉 TRENDS")
            lines.append(f"   This week: {trends['current_week']}")
            lines.append(f"   Last week: {trends['previous_week']}")
            lines.append(f"   Change: {sign}{trends['wow_change_pct']:.1f}%")
            lines.append("")

        if self.data['errors']:
            lines.append("-" * 60)
            lines.append("⚠️ ERRORS")
            for error in self.data['errors']:
                lines.append(f"   - {error}")
            lines.append("")

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate weekly HubSpot attribution report')
    parser.add_argument(
        '--output',
        choices=['console', 'markdown', 'json'],
        default='console',
        help='Output format'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to analyze (default: 7)'
    )
    parser.add_argument(
        '--save',
        help='Save output to file'
    )
    args = parser.parse_args()

    report = WeeklyHubSpotReport(days=args.days)
    report.collect_all()

    if args.output == 'console':
        output = report.format_console()
        print(output)
    elif args.output == 'markdown':
        output = report.format_markdown()
        print(output)
    elif args.output == 'json':
        output = json.dumps(report.data, indent=2, default=str)
        print(output)

    if args.save:
        save_output = output if isinstance(output, str) else json.dumps(output)
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        Path(args.save).write_text(save_output)
        print(f"\nSaved to: {args.save}")


if __name__ == "__main__":
    main()
