# Webflow Content Sync Setup

This directory contains the scripts to sync content from your Webflow CMS to the Master Content Database.

## Setup Instructions

1. **Configure API Credentials**
   ```bash
   cd "data_sources/config"
   cp .env.template .env
   # Edit .env with your actual Webflow API credentials
   ```

2. **Install Python Dependencies** (if not already installed)
   ```bash
   pip install python-dotenv requests
   ```

3. **Run the Sync**
   ```bash
   # From the seomachine directory:
   python3 sync_webflow.py
   
   # Or from anywhere:
   cd ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/Root\ Docs/OpenEd\ Vault/Studio/Misc.\ Utilities/seomachine
   ./sync_webflow.py
   ```

## Getting Your Webflow API Credentials

1. **API Key**: 
   - Log into Webflow
   - Go to Account Settings > API Access
   - Generate an API key

2. **Site Name**: 
   - Usually visible in your Webflow dashboard URL
   - For OpenEd, it's typically "open-ed"

3. **Collection ID**:
   - In Webflow, go to your CMS Collections
   - Click on your blog posts collection
   - The collection ID is in the URL

## Automation Options

You can automate this sync using:
- **cron** for scheduled runs
- **launchd** on macOS
- Manual run at the start of content sessions

## What Gets Synced

The sync creates/updates markdown files in:
`~/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/`

Each file includes:
- YAML frontmatter (title, url, type, date, meta_description, summary)
- Full content body
- Proper categorization by content type