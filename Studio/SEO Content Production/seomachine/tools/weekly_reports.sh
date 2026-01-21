#!/bin/bash
# Weekly Marketing Reports
# Generates both SEO and Social reports
#
# Usage: ./weekly_reports.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SEOMACHINE_DIR="$(dirname "$SCRIPT_DIR")"
REPORTS_DIR="/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/Studio/Analytics & Attribution/reports"
DATE=$(date +%Y-%m-%d)

cd "$SEOMACHINE_DIR"

echo "=================================="
echo "WEEKLY MARKETING REPORTS - $DATE"
echo "=================================="
echo ""

# Create reports directory if needed
mkdir -p "$REPORTS_DIR"

# Run SEO Report
echo "📊 Generating SEO Report..."
python3 tools/weekly_seo_report.py \
    --domain opened.co \
    --output markdown \
    --save "$REPORTS_DIR/weekly-seo-$DATE.md" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Saved: weekly-seo-$DATE.md"
else
    echo "   ❌ SEO report failed"
fi

echo ""

# Run Social Report
echo "📱 Generating Social Report..."
python3 tools/weekly_social_report.py \
    --output markdown \
    --save "$REPORTS_DIR/weekly-social-$DATE.md" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Saved: weekly-social-$DATE.md"
else
    echo "   ❌ Social report failed"
fi

echo ""
echo "=================================="
echo "Reports saved to:"
echo "$REPORTS_DIR"
echo "=================================="
