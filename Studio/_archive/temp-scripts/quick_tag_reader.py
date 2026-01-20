#!/usr/bin/env python3
"""
Quick tag reader for Master Content Database.
Demonstrates progressive disclosure by reading only the first few lines.
"""

import os
import yaml
import re
from pathlib import Path
from collections import defaultdict

def read_file_tags(file_path, max_lines=10):
    """Read only the first few lines to get title and tags"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read just the first N lines
            lines = []
            for i, line in enumerate(f):
                lines.append(line)
                if i >= max_lines:
                    break
            
            content = ''.join(lines)
            
            # Check if we have frontmatter
            if content.startswith('---\n'):
                # Find the end of frontmatter
                end_match = re.search(r'\n---\n', content[4:])
                if end_match:
                    frontmatter = content[4:4+end_match.start()]
                    try:
                        metadata = yaml.safe_load(frontmatter)
                        return {
                            'title': metadata.get('title', 'Untitled'),
                            'tags': metadata.get('tags', []),
                            'tools': metadata.get('tools', []),
                            'type': metadata.get('type', 'unknown')
                        }
                    except:
                        pass
            
            return None
            
    except Exception as e:
        return None


def find_content_by_tag(base_path, target_tag):
    """Find all content with a specific tag using progressive disclosure"""
    matches = []
    
    for md_file in Path(base_path).rglob('*.md'):
        if md_file.is_file():
            result = read_file_tags(md_file)
            if result and target_tag in result.get('tags', []):
                matches.append({
                    'file': str(md_file.relative_to(base_path)),
                    'title': result['title'],
                    'tags': result['tags'],
                    'tools': result['tools']
                })
    
    return matches


def find_content_by_tool(base_path, target_tool):
    """Find all content mentioning a specific tool"""
    matches = []
    
    for md_file in Path(base_path).rglob('*.md'):
        if md_file.is_file():
            result = read_file_tags(md_file)
            if result and target_tool in result.get('tools', []):
                matches.append({
                    'file': str(md_file.relative_to(base_path)),
                    'title': result['title'],
                    'tools': result['tools'],
                    'type': result['type']
                })
    
    return matches


def build_tag_index(base_path):
    """Build a quick index of all tags"""
    tag_index = defaultdict(list)
    tool_index = defaultdict(list)
    
    for md_file in Path(base_path).rglob('*.md'):
        if md_file.is_file():
            result = read_file_tags(md_file)
            if result:
                rel_path = str(md_file.relative_to(base_path))
                
                # Index by tags
                for tag in result.get('tags', []):
                    tag_index[tag].append({
                        'file': rel_path,
                        'title': result['title']
                    })
                
                # Index by tools
                for tool in result.get('tools', []):
                    tool_index[tool].append({
                        'file': rel_path,
                        'title': result['title']
                    })
    
    return dict(tag_index), dict(tool_index)


def main():
    """Demo the progressive disclosure functionality"""
    base_path = "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database"
    
    print("Master Content Database - Quick Tag Reader")
    print("==========================================")
    
    # Example 1: Find content by philosophy
    print("\n1. Finding all Montessori content:")
    montessori_content = find_content_by_tag(base_path, 'montessori')
    for item in montessori_content[:5]:
        print(f"  - {item['title']}")
        print(f"    Tags: {', '.join(item['tags'][:5])}...")
    
    # Example 2: Find content by tool
    print("\n2. Finding all content mentioning Khan Academy:")
    khan_content = find_content_by_tool(base_path, 'khan-academy')
    for item in khan_content[:5]:
        print(f"  - {item['title']} ({item['type']})")
    
    # Example 3: Build tag cloud
    print("\n3. Building tag index (reading only first 10 lines of each file)...")
    tag_index, tool_index = build_tag_index(base_path)
    
    # Show top tags
    print("\nTop 10 tags by frequency:")
    sorted_tags = sorted(tag_index.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    for tag, files in sorted_tags:
        print(f"  - {tag}: {len(files)} files")
    
    # Show all tools
    print("\nAll tools mentioned:")
    for tool, files in sorted(tool_index.items()):
        print(f"  - {tool}: {len(files)} files")
    
    # Performance note
    import time
    start = time.time()
    all_tags = build_tag_index(base_path)
    end = time.time()
    
    print(f"\nPerformance: Indexed {sum(len(v) for v in tag_index.values())} tag occurrences")
    print(f"in {end - start:.2f} seconds by reading only first 10 lines of each file")


if __name__ == "__main__":
    main()