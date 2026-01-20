#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Gmail to Notion CRM Setup ==="
echo ""

if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  Edit .env with your Notion token before proceeding"
    echo "   Get token from: https://www.notion.so/my-integrations"
    echo ""
fi

if [ ! -f "credentials.json" ]; then
    echo "⚠️  Missing credentials.json"
    echo ""
    echo "Steps to get it:"
    echo "1. Go to: https://console.cloud.google.com"
    echo "2. Create project → Enable Gmail API"
    echo "3. APIs & Services → Credentials → Create OAuth client ID (Desktop app)"
    echo "4. Download JSON → rename to 'credentials.json' → put in this folder"
    echo ""
    exit 1
fi

echo "Installing Python dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

source .env 2>/dev/null || true

if [ -z "$NOTION_TOKEN" ]; then
    echo "⚠️  NOTION_TOKEN not set in .env"
    echo "   Edit .env and add your Notion integration token"
    exit 1
fi

if [ -z "$NOTION_CRM_DATABASE_ID" ]; then
    echo "No Notion database configured. Creating one..."
    echo ""
    echo "Enter the Notion page ID where you want the CRM database:"
    echo "(Find it in the page URL: notion.so/PAGE_ID?v=...)"
    read -p "> " PAGE_ID
    
    if [ -n "$PAGE_ID" ]; then
        DB_ID=$(python gmail_to_notion_crm.py --create-db "$PAGE_ID" 2>&1 | grep "Created Notion database:" | cut -d: -f2 | tr -d ' ')
        if [ -n "$DB_ID" ]; then
            echo "NOTION_CRM_DATABASE_ID=$DB_ID" >> .env
            echo "✓ Database created and saved to .env"
        fi
    fi
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Run the CRM extraction:"
echo "  python gmail_to_notion_crm.py --full"
echo ""
echo "Or step by step:"
echo "  python gmail_to_notion_crm.py --extract  # Extract from Gmail"
echo "  python gmail_to_notion_crm.py --sync     # Sync to Notion"
