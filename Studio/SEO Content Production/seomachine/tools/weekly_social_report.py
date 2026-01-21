#!/usr/bin/env python3
"""
Weekly Social Media Report

Generates a consolidated report of all social channel performance.
Run alongside weekly_seo_report.py for full marketing analytics.

Usage:
    python weekly_social_report.py --output markdown --save report.md
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

from data_sources.modules.youtube import YouTubeAnalytics
from data_sources.modules.meta import MetaAnalytics


class WeeklySocialReport:
    """Generate weekly social media performance report"""

    def __init__(self):
        self.data = {
            'generated_at': datetime.now().isoformat(),
            'youtube': None,
            'facebook': None,
            'instagram': None,
            'top_content': [],
            'errors': [],
        }

    def collect_youtube(self):
        """Collect YouTube channel and video data"""
        try:
            yt = YouTubeAnalytics()
            channel_id = os.getenv('YOUTUBE_CHANNEL_ID')

            if not channel_id:
                self.data['errors'].append('YOUTUBE_CHANNEL_ID not set')
                return

            stats = yt.get_channel_stats(channel_id)
            videos = yt.get_recent_videos(channel_id, max_results=10)

            self.data['youtube'] = {
                'channel': stats.get('title'),
                'subscribers': stats.get('subscribers', 0),
                'total_views': stats.get('total_views', 0),
                'video_count': stats.get('video_count', 0),
                'recent_videos': videos[:5],
            }

            # Add top video to top_content
            if videos:
                top_video = max(videos, key=lambda x: x.get('views', 0))
                self.data['top_content'].append({
                    'platform': 'YouTube',
                    'title': top_video.get('title', '')[:60],
                    'metric': f"{top_video.get('views', 0):,} views",
                    'url': f"https://youtube.com/watch?v={top_video['video_id']}",
                })

        except Exception as e:
            self.data['errors'].append(f'YouTube error: {str(e)}')

    def collect_meta(self):
        """Collect Facebook and Instagram data"""
        try:
            meta = MetaAnalytics()

            # Facebook
            try:
                fb_info = meta.get_page_info()
                fb_posts = meta.get_recent_posts(limit=10)

                self.data['facebook'] = {
                    'page': fb_info.get('name'),
                    'followers': fb_info.get('followers', 0),
                    'likes': fb_info.get('likes', 0),
                    'recent_posts': len(fb_posts),
                }

                # Top FB post by shares
                if fb_posts:
                    top_fb = max(fb_posts, key=lambda x: x.get('shares', 0))
                    if top_fb.get('shares', 0) > 0:
                        self.data['top_content'].append({
                            'platform': 'Facebook',
                            'title': top_fb.get('message', '')[:60],
                            'metric': f"{top_fb.get('shares', 0)} shares",
                            'url': top_fb.get('permalink', ''),
                        })

            except Exception as e:
                self.data['errors'].append(f'Facebook error: {str(e)}')

            # Instagram
            try:
                ig_info = meta.get_instagram_info()
                ig_posts = meta.get_instagram_media(limit=25)

                self.data['instagram'] = {
                    'username': ig_info.get('username'),
                    'followers': ig_info.get('followers', 0),
                    'following': ig_info.get('following', 0),
                    'post_count': ig_info.get('posts', 0),
                }

                # Top IG post by reach
                if ig_posts:
                    top_ig = max(ig_posts, key=lambda x: x.get('reach', 0))
                    self.data['top_content'].append({
                        'platform': 'Instagram',
                        'title': top_ig.get('caption', '')[:60],
                        'metric': f"{top_ig.get('reach', 0):,} reach",
                        'url': top_ig.get('permalink', ''),
                    })

                    # Calculate avg reach for context
                    avg_reach = sum(p.get('reach', 0) for p in ig_posts) / len(ig_posts)
                    self.data['instagram']['avg_reach'] = round(avg_reach, 0)
                    self.data['instagram']['top_reach'] = top_ig.get('reach', 0)

            except Exception as e:
                self.data['errors'].append(f'Instagram error: {str(e)}')

        except ValueError as e:
            self.data['errors'].append(f'Meta not configured: {str(e)}')

    def collect_all(self):
        """Collect data from all sources"""
        print("Collecting YouTube data...")
        self.collect_youtube()

        print("Collecting Meta (Facebook + Instagram) data...")
        self.collect_meta()

        # Sort top content by some heuristic
        self.data['top_content'].sort(
            key=lambda x: int(x['metric'].replace(',', '').split()[0]),
            reverse=True
        )

    def format_markdown(self) -> str:
        """Format report as markdown"""
        lines = []
        lines.append(f"# Weekly Social Media Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")

        # Summary table
        lines.append("## Channel Summary")
        lines.append("")
        lines.append("| Platform | Followers | Notes |")
        lines.append("|----------|-----------|-------|")

        if self.data['youtube']:
            yt = self.data['youtube']
            lines.append(f"| YouTube | {yt['subscribers']:,} | {yt['total_views']:,} total views, {yt['video_count']} videos |")

        if self.data['facebook']:
            fb = self.data['facebook']
            lines.append(f"| Facebook | {fb['followers']:,} | {fb['likes']:,} page likes |")

        if self.data['instagram']:
            ig = self.data['instagram']
            lines.append(f"| Instagram | {ig['followers']:,} | {ig['post_count']} posts, avg {ig.get('avg_reach', 0):,.0f} reach |")

        lines.append("")

        # Top content
        if self.data['top_content']:
            lines.append("## Top Performing Content")
            lines.append("")
            lines.append("| Platform | Content | Performance |")
            lines.append("|----------|---------|-------------|")

            for item in self.data['top_content'][:5]:
                title = item['title'][:50] + '...' if len(item['title']) > 50 else item['title']
                lines.append(f"| {item['platform']} | {title} | {item['metric']} |")

            lines.append("")

        # Recent YouTube videos
        if self.data['youtube'] and self.data['youtube'].get('recent_videos'):
            lines.append("## Recent YouTube Videos")
            lines.append("")
            lines.append("| Video | Views | Likes |")
            lines.append("|-------|-------|-------|")

            for video in self.data['youtube']['recent_videos'][:5]:
                title = video['title'][:50] + '...' if len(video['title']) > 50 else video['title']
                lines.append(f"| {title} | {video.get('views', 0):,} | {video.get('likes', 0):,} |")

            lines.append("")

        # Instagram insights
        if self.data['instagram']:
            ig = self.data['instagram']
            if ig.get('top_reach') and ig.get('avg_reach'):
                ratio = ig['top_reach'] / ig['avg_reach'] if ig['avg_reach'] > 0 else 0
                lines.append("## Instagram Insights")
                lines.append("")
                lines.append(f"- **Average post reach:** {ig['avg_reach']:,.0f}")
                lines.append(f"- **Top post reach:** {ig['top_reach']:,}")
                lines.append(f"- **Top post outperformance:** {ratio:.1f}x average")
                lines.append("")

        # Errors
        if self.data['errors']:
            lines.append("## Errors")
            lines.append("")
            for error in self.data['errors']:
                lines.append(f"- {error}")
            lines.append("")

        # Data sources
        lines.append("---")
        lines.append("")
        lines.append("## Data Sources Status")
        lines.append("")
        lines.append(f"- YouTube: {'✅ Connected' if self.data['youtube'] else '❌ Not connected'}")
        lines.append(f"- Facebook: {'✅ Connected' if self.data['facebook'] else '❌ Not connected'}")
        lines.append(f"- Instagram: {'✅ Connected' if self.data['instagram'] else '❌ Not connected'}")
        lines.append("")

        return '\n'.join(lines)

    def format_console(self) -> str:
        """Format report for console output"""
        lines = []
        lines.append("=" * 60)
        lines.append("WEEKLY SOCIAL MEDIA REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("=" * 60)
        lines.append("")

        if self.data['youtube']:
            yt = self.data['youtube']
            lines.append(f"📺 YOUTUBE: {yt['channel']}")
            lines.append(f"   Subscribers: {yt['subscribers']:,}")
            lines.append(f"   Total Views: {yt['total_views']:,}")
            lines.append("")

        if self.data['facebook']:
            fb = self.data['facebook']
            lines.append(f"📘 FACEBOOK: {fb['page']}")
            lines.append(f"   Followers: {fb['followers']:,}")
            lines.append("")

        if self.data['instagram']:
            ig = self.data['instagram']
            lines.append(f"📸 INSTAGRAM: @{ig['username']}")
            lines.append(f"   Followers: {ig['followers']:,}")
            lines.append(f"   Avg Reach: {ig.get('avg_reach', 0):,.0f}")
            lines.append("")

        if self.data['top_content']:
            lines.append("-" * 60)
            lines.append("🏆 TOP PERFORMING CONTENT")
            lines.append("-" * 60)
            for i, item in enumerate(self.data['top_content'][:3], 1):
                lines.append(f"{i}. [{item['platform']}] {item['metric']}")
                lines.append(f"   {item['title'][:60]}")
                lines.append("")

        if self.data['errors']:
            lines.append("-" * 60)
            lines.append("⚠️ ERRORS")
            for error in self.data['errors']:
                lines.append(f"   - {error}")
            lines.append("")

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate weekly social media report')
    parser.add_argument(
        '--output',
        choices=['console', 'markdown', 'json'],
        default='console',
        help='Output format'
    )
    parser.add_argument(
        '--save',
        help='Save output to file'
    )
    args = parser.parse_args()

    report = WeeklySocialReport()
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
