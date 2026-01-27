"""
HubSpot Insights Engine

Automated pattern detection for HubSpot data:
- Channel shifts (significant changes vs last period)
- High-value sources (best subscriber → lead conversion)
- Underperforming content (high traffic, low conversion)
- Seasonal patterns
- Anomaly detection

Usage:
    from data_sources.modules.hubspot_insights import HubSpotInsights

    insights = HubSpotInsights()
    observations = insights.get_all_insights()

    for obs in observations:
        print(f"[{obs['severity']}] {obs['title']}")
        print(f"  {obs['description']}")
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from statistics import mean, stdev

from .hubspot import HubSpotAnalytics


class HubSpotInsights:
    """Automated insight generation from HubSpot data"""

    SEVERITY_LEVELS = ['info', 'warning', 'critical', 'opportunity']

    def __init__(self, api_key: Optional[str] = None):
        self.hs = HubSpotAnalytics(api_key=api_key)

    def get_all_insights(self, days: int = 30, comparison_days: int = 30) -> List[Dict[str, Any]]:
        """
        Generate all insights

        Args:
            days: Period to analyze
            comparison_days: Previous period for comparison

        Returns:
            List of insight dicts with title, description, severity, data
        """
        insights = []

        insights.extend(self._analyze_channel_shifts(days, comparison_days))
        insights.extend(self._analyze_high_value_sources(days))
        insights.extend(self._analyze_underperformers(days))
        insights.extend(self._analyze_curriculove_patterns(days))
        insights.extend(self._analyze_funnel_bottlenecks(days))
        insights.extend(self._analyze_time_patterns(weeks=8))

        # Sort by severity (critical first, then opportunity, warning, info)
        severity_order = {'critical': 0, 'opportunity': 1, 'warning': 2, 'info': 3}
        insights.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 3))

        return insights

    def _create_insight(
        self,
        title: str,
        description: str,
        severity: str = 'info',
        data: Optional[Dict] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        """Helper to create insight dict"""
        return {
            'title': title,
            'description': description,
            'severity': severity,
            'data': data or {},
            'action': action,
            'generated_at': datetime.now().isoformat(),
        }

    def _analyze_channel_shifts(self, days: int, comparison_days: int) -> List[Dict[str, Any]]:
        """Detect significant channel mix changes"""
        insights = []

        try:
            # Current period
            current = self.hs.get_contacts_by_source(days=days, max_contacts=5000)
            current_total = sum(current.values())

            # Previous period (offset by current period)
            previous = self.hs.get_contacts_by_source(days=comparison_days, max_contacts=5000)
            previous_total = sum(previous.values())

            if current_total == 0 or previous_total == 0:
                return insights

            # Check each source for shifts
            all_sources = set(current.keys()) | set(previous.keys())

            for source in all_sources:
                curr_count = current.get(source, 0)
                prev_count = previous.get(source, 0)

                curr_pct = curr_count / current_total * 100
                prev_pct = prev_count / previous_total * 100

                shift = curr_pct - prev_pct

                # Significant shift threshold: 5 percentage points
                if abs(shift) >= 5:
                    direction = "increased" if shift > 0 else "decreased"
                    severity = "opportunity" if shift > 0 else "warning"

                    insights.append(self._create_insight(
                        title=f"{source} traffic {direction} significantly",
                        description=f"{source} share shifted from {prev_pct:.1f}% to {curr_pct:.1f}% ({shift:+.1f}pp)",
                        severity=severity,
                        data={
                            'source': source,
                            'previous_pct': round(prev_pct, 1),
                            'current_pct': round(curr_pct, 1),
                            'shift_pp': round(shift, 1),
                        },
                        action=f"Investigate what caused the {direction.lower()} in {source} traffic"
                    ))

            # Overall volume change
            volume_change = ((current_total - previous_total) / previous_total * 100) if previous_total > 0 else 0

            if abs(volume_change) >= 20:
                direction = "up" if volume_change > 0 else "down"
                severity = "opportunity" if volume_change > 0 else "warning"

                insights.append(self._create_insight(
                    title=f"Overall contact volume {direction} {abs(volume_change):.0f}%",
                    description=f"New contacts changed from {previous_total:,} to {current_total:,} ({volume_change:+.1f}%)",
                    severity=severity,
                    data={
                        'previous_total': previous_total,
                        'current_total': current_total,
                        'change_pct': round(volume_change, 1),
                    },
                    action="Review marketing activities and campaigns during this period"
                ))

        except Exception as e:
            insights.append(self._create_insight(
                title="Channel analysis error",
                description=str(e),
                severity="info"
            ))

        return insights

    def _analyze_high_value_sources(self, days: int) -> List[Dict[str, Any]]:
        """Identify sources with best lead conversion"""
        insights = []

        try:
            source_rates = self.hs.get_source_to_lead_rate(days=days, max_contacts=5000)

            if not source_rates:
                return insights

            # Find sources with significant volume and high conversion
            high_value = []
            for source, data in source_rates.items():
                if data['total'] >= 10:  # Minimum volume threshold
                    high_value.append({
                        'source': source,
                        'total': data['total'],
                        'leads': data['leads'],
                        'rate': data['rate'],
                    })

            high_value.sort(key=lambda x: -x['rate'])

            # Top performer
            if high_value and high_value[0]['rate'] > 0:
                top = high_value[0]
                avg_rate = mean([h['rate'] for h in high_value]) if len(high_value) > 1 else 0

                if top['rate'] > avg_rate * 1.5:  # 50% above average
                    insights.append(self._create_insight(
                        title=f"{top['source']} has exceptional lead conversion",
                        description=f"{top['rate']:.1f}% lead rate vs {avg_rate:.1f}% average - {top['leads']} leads from {top['total']} contacts",
                        severity="opportunity",
                        data={
                            'source': top['source'],
                            'rate': top['rate'],
                            'average_rate': round(avg_rate, 1),
                            'contacts': top['total'],
                            'leads': top['leads'],
                        },
                        action=f"Double down on {top['source']} - highest quality traffic source"
                    ))

            # Low performers with volume
            low_performers = [h for h in high_value if h['rate'] < 2 and h['total'] >= 50]
            if low_performers:
                worst = low_performers[0] if low_performers else None
                if worst:
                    insights.append(self._create_insight(
                        title=f"{worst['source']} has low lead conversion",
                        description=f"Only {worst['rate']:.1f}% lead rate despite {worst['total']} contacts",
                        severity="warning",
                        data=worst,
                        action=f"Review {worst['source']} landing experience and targeting"
                    ))

        except Exception as e:
            pass

        return insights

    def _analyze_underperformers(self, days: int) -> List[Dict[str, Any]]:
        """Find high-traffic pages with low conversion"""
        insights = []

        try:
            pages = self.hs.get_landing_page_conversions(days=days, max_contacts=5000)

            if not pages or len(pages) < 3:
                return insights

            # Calculate average conversions per page
            total_conversions = sum(p['count'] for p in pages)
            avg_conversions = total_conversions / len(pages)

            # Find pages significantly above average (might be opportunities to optimize)
            top_pages = [p for p in pages if p['count'] > avg_conversions * 2]

            if top_pages:
                top = top_pages[0]
                insights.append(self._create_insight(
                    title=f"Top converting landing page identified",
                    description=f"{top['url'][:60]}... converts {top['count']} contacts - {top['count']/avg_conversions:.1f}x average",
                    severity="opportunity",
                    data={
                        'url': top['url'],
                        'conversions': top['count'],
                        'average': round(avg_conversions, 1),
                        'top_source': top['top_source'],
                    },
                    action="Study this page's structure for optimization patterns"
                ))

            # Find blog content performance
            blog_pages = [p for p in pages if '/blog/' in p['url'] or '/education-hub/' in p['url']]
            if blog_pages:
                top_blog = blog_pages[0]
                insights.append(self._create_insight(
                    title=f"Top blog conversion page",
                    description=f"{top_blog['url'].split('/')[-1][:40]} - {top_blog['count']} conversions via {top_blog['top_source']}",
                    severity="info",
                    data={
                        'url': top_blog['url'],
                        'conversions': top_blog['count'],
                        'source': top_blog['top_source'],
                    },
                    action="Create more content like this top performer"
                ))

        except Exception as e:
            pass

        return insights

    def _analyze_curriculove_patterns(self, days: int) -> List[Dict[str, Any]]:
        """Analyze Curriculove lead magnet performance"""
        insights = []

        try:
            curriculove = self.hs.get_curriculove_leads(days=days, max_contacts=5000)

            if curriculove['total'] == 0:
                return insights

            # Philosophy distribution
            if curriculove['by_philosophy']:
                top_phil = list(curriculove['by_philosophy'].items())[0]
                total_phil = sum(curriculove['by_philosophy'].values())

                if total_phil > 0:
                    top_pct = top_phil[1] / total_phil * 100

                    if top_pct > 40:
                        insights.append(self._create_insight(
                            title=f"Curriculove dominated by {top_phil[0]}",
                            description=f"{top_pct:.0f}% of quiz takers match {top_phil[0]} - consider content for this audience",
                            severity="info",
                            data={
                                'philosophy': top_phil[0],
                                'count': top_phil[1],
                                'percentage': round(top_pct, 1),
                            },
                            action=f"Create more content targeted at {top_phil[0]} parents"
                        ))

            # State patterns
            if curriculove['by_state']:
                # Operating states
                operating = ['AR', 'IN', 'IA', 'KS', 'MN', 'MT', 'NV', 'OR', 'UT']
                total_state = sum(curriculove['by_state'].values())
                operating_count = sum(curriculove['by_state'].get(s, 0) for s in operating)

                if total_state > 0:
                    operating_pct = operating_count / total_state * 100

                    if operating_pct < 50:
                        insights.append(self._create_insight(
                            title="Most Curriculove leads outside operating states",
                            description=f"Only {operating_pct:.0f}% from operating states - {total_state - operating_count} leads in non-operating states",
                            severity="info",
                            data={
                                'operating_pct': round(operating_pct, 1),
                                'operating_count': operating_count,
                                'non_operating': total_state - operating_count,
                            },
                            action="Consider expansion opportunities or state-specific content"
                        ))

        except Exception as e:
            pass

        return insights

    def _analyze_funnel_bottlenecks(self, days: int) -> List[Dict[str, Any]]:
        """Identify funnel conversion bottlenecks"""
        insights = []

        try:
            funnel = self.hs.get_funnel_conversion_rates(days=days, max_contacts=5000)

            rates = funnel['conversion_rates']

            # Low subscriber to lead conversion
            if rates['subscriber_to_lead'] < 5:
                insights.append(self._create_insight(
                    title="Low subscriber-to-lead conversion",
                    description=f"Only {rates['subscriber_to_lead']:.1f}% of subscribers become leads - nurture sequence opportunity",
                    severity="warning",
                    data={
                        'rate': rates['subscriber_to_lead'],
                        'subscribers': funnel['stages'].get('subscriber', 0),
                        'leads': funnel['stages'].get('lead', 0),
                    },
                    action="Review email nurture sequence and lead qualification criteria"
                ))

            # Good conversion (opportunity to scale)
            if rates['subscriber_to_lead'] > 15:
                insights.append(self._create_insight(
                    title="Strong subscriber-to-lead conversion",
                    description=f"{rates['subscriber_to_lead']:.1f}% conversion rate - focus on scaling subscriber acquisition",
                    severity="opportunity",
                    data={
                        'rate': rates['subscriber_to_lead'],
                    },
                    action="Increase top-of-funnel investment to leverage strong conversion"
                ))

        except Exception as e:
            pass

        return insights

    def _analyze_time_patterns(self, weeks: int = 8) -> List[Dict[str, Any]]:
        """Analyze time-based signup patterns"""
        insights = []

        try:
            weekly = self.hs.get_weekly_signups(weeks=weeks)

            if len(weekly) < 4:
                return insights

            counts = [w['count'] for w in weekly]

            # Trend analysis
            first_half = mean(counts[:len(counts)//2])
            second_half = mean(counts[len(counts)//2:])

            trend_pct = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0

            if abs(trend_pct) > 25:
                direction = "growing" if trend_pct > 0 else "declining"
                severity = "opportunity" if trend_pct > 0 else "warning"

                insights.append(self._create_insight(
                    title=f"Signup volume {direction} over time",
                    description=f"Recent weeks average {second_half:.0f}/week vs earlier {first_half:.0f}/week ({trend_pct:+.0f}%)",
                    severity=severity,
                    data={
                        'first_half_avg': round(first_half, 1),
                        'second_half_avg': round(second_half, 1),
                        'trend_pct': round(trend_pct, 1),
                    },
                    action="Investigate factors driving the trend"
                ))

            # Volatility check
            if len(counts) >= 4:
                try:
                    volatility = stdev(counts) / mean(counts) * 100
                    if volatility > 50:
                        insights.append(self._create_insight(
                            title="High signup volatility detected",
                            description=f"Weekly signups vary by {volatility:.0f}% - indicates inconsistent marketing or seasonality",
                            severity="info",
                            data={
                                'volatility_pct': round(volatility, 1),
                                'min': min(counts),
                                'max': max(counts),
                            },
                            action="Identify causes of peaks and valleys to smooth acquisition"
                        ))
                except:
                    pass

        except Exception as e:
            pass

        return insights

    def format_insights_markdown(self, insights: List[Dict[str, Any]]) -> str:
        """Format insights as markdown"""
        lines = []
        lines.append("# HubSpot Insights Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Insights found:** {len(insights)}")
        lines.append("")

        # Group by severity
        for severity in ['critical', 'opportunity', 'warning', 'info']:
            group = [i for i in insights if i.get('severity') == severity]
            if not group:
                continue

            emoji = {'critical': '🚨', 'opportunity': '💡', 'warning': '⚠️', 'info': 'ℹ️'}
            lines.append(f"## {emoji.get(severity, '')} {severity.title()}")
            lines.append("")

            for insight in group:
                lines.append(f"### {insight['title']}")
                lines.append("")
                lines.append(insight['description'])
                lines.append("")
                if insight.get('action'):
                    lines.append(f"**Action:** {insight['action']}")
                    lines.append("")

        return '\n'.join(lines)


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    engine = HubSpotInsights()
    insights = engine.get_all_insights(days=30)

    print("HubSpot Insights")
    print("=" * 50)

    for insight in insights:
        severity = insight.get('severity', 'info').upper()
        print(f"\n[{severity}] {insight['title']}")
        print(f"  {insight['description']}")
        if insight.get('action'):
            print(f"  → {insight['action']}")
