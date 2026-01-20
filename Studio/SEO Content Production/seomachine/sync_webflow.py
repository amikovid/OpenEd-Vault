#!/usr/bin/env python3
"""
Sync Webflow content to Master Content Database
Run this script to pull latest content from Webflow CMS
"""

import os
import sys
from pathlib import Path

# Add the data_sources directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "data_sources"))

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    env_path = Path(__file__).parent / "data_sources" / "config" / ".env"
    if not env_path.exists():
        print("Error: .env file not found!")
        print(f"Please copy .env.template to .env in: {env_path.parent}")
        print("Then add your Webflow API credentials.")
        sys.exit(1)
    
    load_dotenv(env_path)
    
    # Check if required environment variables are set
    required_vars = ["WEBFLOW_API_KEY", "WEBFLOW_SITE_NAME", "WEBFLOW_POSTS_COLLECTION_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var) or os.getenv(var) == "your_api_key_here"]
    
    if missing_vars:
        print("Error: Missing or unconfigured environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease edit the .env file with your actual Webflow API credentials.")
        sys.exit(1)
    
    # Import and run the sync function
    from modules.webflow import sync_content_database
    
    print("Starting Webflow content sync...")
    sync_content_database()
    print("Sync completed successfully!")
    
except ImportError as e:
    print(f"Error: Missing required Python package: {e}")
    print("Please install required packages with:")
    print("  pip install python-dotenv requests")
    sys.exit(1)
except Exception as e:
    print(f"Error during sync: {e}")
    sys.exit(1)