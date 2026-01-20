#!/usr/bin/env python3
"""
Read-only access to Webflow Tools and Subjects collections
Use this to fetch and display content from these collections without syncing to markdown
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the data_sources directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "data_sources"))

try:
    from dotenv import load_dotenv
    import requests
    
    # Load environment variables
    env_path = Path(__file__).parent / "data_sources" / "config" / ".env"
    load_dotenv(env_path)
    
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install with: pip install python-dotenv requests")
    sys.exit(1)


class WebflowReader:
    """Simple reader for Webflow collections"""
    
    def __init__(self):
        self.api_key = os.getenv('WEBFLOW_API_KEY')
        self.site_name = os.getenv('WEBFLOW_SITE_NAME')
        
        if not self.api_key:
            raise ValueError("WEBFLOW_API_KEY not found in .env file")
        
        self.base_url = 'https://api.webflow.com/v2'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'accept': 'application/json'
        }
    
    def get_collection_items(self, collection_id, limit=100):
        """Fetch all items from a specific collection"""
        all_items = []
        offset = 0
        
        while True:
            url = f"{self.base_url}/collections/{collection_id}/items"
            params = {'limit': limit, 'offset': offset}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            all_items.extend(items)
            
            # Check pagination
            pagination = data.get('pagination', {})
            total = pagination.get('total', 0)
            
            if len(all_items) >= total or len(items) < limit:
                break
                
            offset += limit
        
        return all_items
    
    def display_tools(self):
        """Display all tools from the Tools collection"""
        tools_id = os.getenv('WEBFLOW_TOOLS_COLLECTION_ID')
        if not tools_id:
            print("WEBFLOW_TOOLS_COLLECTION_ID not found in .env")
            return
        
        print("\n=== TOOLS COLLECTION ===\n")
        tools = self.get_collection_items(tools_id)
        
        for i, tool in enumerate(tools, 1):
            fields = tool.get('fieldData', {})
            print(f"{i}. {fields.get('name', 'Unnamed')}")
            print(f"   Slug: {fields.get('slug', 'N/A')}")
            print(f"   Description: {fields.get('description', 'N/A')[:100]}...")
            print(f"   URL: {fields.get('url', 'N/A')}")
            print()
    
    def display_subjects(self):
        """Display all subjects from the Subjects collection"""
        subjects_id = os.getenv('WEBFLOW_SUBJECTS_COLLECTION_ID')
        if not subjects_id:
            print("WEBFLOW_SUBJECTS_COLLECTION_ID not found in .env")
            return
        
        print("\n=== SUBJECTS COLLECTION ===\n")
        subjects = self.get_collection_items(subjects_id)
        
        for i, subject in enumerate(subjects, 1):
            fields = subject.get('fieldData', {})
            print(f"{i}. {fields.get('name', 'Unnamed')}")
            print(f"   Slug: {fields.get('slug', 'N/A')}")
            print(f"   Description: {fields.get('description', 'N/A')[:100]}...")
            print()
    
    def export_to_json(self, collection_name):
        """Export a collection to JSON file for offline access"""
        collection_map = {
            'tools': os.getenv('WEBFLOW_TOOLS_COLLECTION_ID'),
            'subjects': os.getenv('WEBFLOW_SUBJECTS_COLLECTION_ID'),
            'posts': os.getenv('WEBFLOW_POSTS_COLLECTION_ID')
        }
        
        collection_id = collection_map.get(collection_name.lower())
        if not collection_id:
            print(f"Unknown collection: {collection_name}")
            print(f"Available: {', '.join(collection_map.keys())}")
            return
        
        items = self.get_collection_items(collection_id)
        
        # Clean data for export
        export_data = []
        for item in items:
            fields = item.get('fieldData', {})
            export_data.append({
                'id': item.get('id'),
                'name': fields.get('name', ''),
                'slug': fields.get('slug', ''),
                'description': fields.get('description', ''),
                'url': fields.get('url', ''),
                'created': item.get('createdOn', ''),
                'updated': item.get('updatedOn', ''),
                'fields': fields  # Include all fields
            })
        
        # Save to JSON
        filename = f"webflow_{collection_name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nExported {len(export_data)} items to {filename}")
    
    def search_tools(self, keyword):
        """Search tools by keyword"""
        tools_id = os.getenv('WEBFLOW_TOOLS_COLLECTION_ID')
        if not tools_id:
            print("WEBFLOW_TOOLS_COLLECTION_ID not found in .env")
            return
        
        tools = self.get_collection_items(tools_id)
        keyword_lower = keyword.lower()
        matches = []
        
        for tool in tools:
            fields = tool.get('fieldData', {})
            name = fields.get('name', '').lower()
            desc = fields.get('description', '').lower()
            
            if keyword_lower in name or keyword_lower in desc:
                matches.append(fields)
        
        if matches:
            print(f"\n=== Found {len(matches)} tools matching '{keyword}' ===\n")
            for i, tool in enumerate(matches, 1):
                print(f"{i}. {tool.get('name', 'Unnamed')}")
                print(f"   URL: {tool.get('url', 'N/A')}")
                print(f"   Description: {tool.get('description', 'N/A')[:150]}...")
                print()
        else:
            print(f"\nNo tools found matching '{keyword}'")


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Read Webflow collections')
    parser.add_argument('action', choices=['tools', 'subjects', 'export', 'search'],
                       help='Action to perform')
    parser.add_argument('--collection', '-c', help='Collection name for export')
    parser.add_argument('--keyword', '-k', help='Keyword for search')
    
    args = parser.parse_args()
    
    try:
        reader = WebflowReader()
        
        if args.action == 'tools':
            reader.display_tools()
        elif args.action == 'subjects':
            reader.display_subjects()
        elif args.action == 'export':
            if not args.collection:
                print("Please specify collection with --collection")
                sys.exit(1)
            reader.export_to_json(args.collection)
        elif args.action == 'search':
            if not args.keyword:
                print("Please specify keyword with --keyword")
                sys.exit(1)
            reader.search_tools(args.keyword)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()