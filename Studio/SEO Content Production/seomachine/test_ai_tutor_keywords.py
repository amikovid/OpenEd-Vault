#!/usr/bin/env python3
"""
Test DataForSEO API for AI tutor keywords
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "data_sources", "config", ".env")
load_dotenv(env_path)

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data_sources"))

from modules.dataforseo import DataForSEO


def main():
    try:
        dfs = DataForSEO()

        keywords = [
            "AI tutor for kids",
            "best AI tutor",
            "adaptive learning apps",
            "AI tutoring platforms",
            "personalized learning software",
        ]

        print("=== DATAFORSEO API TEST ===\n")
        print(f"Testing {len(keywords)} keywords...\n")

        results = []

        for keyword in keywords:
            try:
                print(f"Fetching data for: {keyword}")
                serp = dfs.get_serp_data(keyword, limit=10)

                result = {
                    "keyword": keyword,
                    "search_volume": serp.get("search_volume"),
                    "cpc": serp.get("cpc"),
                    "competition": serp.get("competition"),
                    "total_results": serp.get("total_results", 0),
                    "top_domains": [
                        r["domain"] for r in serp.get("organic_results", [])[:5]
                    ],
                }

                results.append(result)

                print(f"  ✓ Volume: {result['search_volume'] or 'N/A'}")
                print(f"  ✓ CPC: ${result['cpc'] or 'N/A'}")
                print(f"  ✓ Competition: {result['competition'] or 'N/A'}")
                print()

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                print()

        # Print summary
        print("\n=== SUMMARY ===\n")
        for r in results:
            print(f"{r['keyword']}:")
            print(
                f"  Volume: {r['search_volume']:,}"
                if r["search_volume"]
                else "  Volume: N/A"
            )
            print(f"  Top 5 domains: {', '.join(r['top_domains'][:5])}")
            print()

    except ValueError as e:
        print(f"ERROR: {e}")
        print("\nDataForSEO credentials not found in .env file")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
