#!/usr/bin/env python3
"""
Analyze Master Content Database and create a detailed index with progressive disclosure tags.
This script extracts tags and tools from content and updates frontmatter for easy parsing.
"""

import os
import re
import yaml
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class ContentAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.content_stats = defaultdict(list)
        self.tool_mentions = Counter()
        self.tag_frequency = Counter()
        self.philosophy_tags = {
            'unschooling', 'montessori', 'waldorf', 'charlotte-mason', 
            'classical-education', 'forest-school', 'reggio-emilia',
            'project-based', 'stem', 'steam', 'nature-based'
        }
        self.tool_patterns = {
            'khan-academy': r'khan\s*academy',
            'outschool': r'outschool',
            'baketivity': r'baketivity',
            'acellus': r'acellus',
            'time4learning': r'time\s*4\s*learning',
            'ixl': r'\bixl\b',
            'duolingo': r'duolingo',
            'minecraft': r'minecraft',
            'lego': r'\blego\b',
            'scratch': r'\bscratch\b',
            'chatgpt': r'chatgpt|chat\s*gpt',
            'ai-tutor': r'ai\s*tutor|artificial\s*intelligence.*tutor',
            'google': r'google\s*(classroom|docs|sheets)',
            'zoom': r'\bzoom\b',
            'youtube': r'youtube',
            'kindle': r'kindle',
            'audiobook': r'audiobook|audible'
        }
        
    def extract_tags_from_content(self, content, title=""):
        """Extract tags based on content analysis"""
        tags = []
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Check for philosophy mentions
        for philosophy in self.philosophy_tags:
            pattern = philosophy.replace('-', r'[\s-]')
            if re.search(pattern, content_lower) or re.search(pattern, title_lower):
                tags.append(philosophy)
        
        # Age-based tags
        age_patterns = {
            'preschool': r'\bpreschool|pre-k|prek\b',
            'kindergarten': r'\bkindergarten\b',
            'elementary': r'\belementary|grade[s]?\s*[1-5]\b',
            'middle-school': r'\bmiddle\s*school|grade[s]?\s*[6-8]\b',
            'high-school': r'\bhigh\s*school|teen|grade[s]?\s*(?:9|10|11|12)\b',
            '10-14-years': r'\b10[\s-]to[\s-]14|ages?\s*10[\s-]14\b'
        }
        
        for tag, pattern in age_patterns.items():
            if re.search(pattern, content_lower):
                tags.append(tag)
        
        # Subject tags
        subject_patterns = {
            'math': r'\bmath|algebra|geometry|calculus\b',
            'science': r'\bscience|biology|chemistry|physics|stem\b',
            'reading': r'\bread|literacy|phonics|dyslexia\b',
            'writing': r'\bwrit|essay|composition\b',
            'art': r'\bart[s]?\b|drawing|painting|creative\b',
            'music': r'\bmusic|instrument|piano|guitar\b',
            'history': r'\bhistory|historical\b',
            'language': r'\blanguage|spanish|french|foreign\b',
            'coding': r'\bcod[ei]|programming|computer\s*science\b'
        }
        
        for tag, pattern in subject_patterns.items():
            if re.search(pattern, content_lower):
                tags.append(tag)
        
        # Topic tags
        topic_patterns = {
            'adhd': r'\badhd|attention\s*deficit\b',
            'special-needs': r'\bspecial\s*needs|learning\s*disabilit|dyslexia\b',
            'gifted': r'\bgifted|advanced|accelerated\b',
            'socialization': r'\bsocial|friend|peer\b',
            'curriculum': r'\bcurriculum|course|program\b',
            'assessment': r'\bassess|test|grade|evaluat\b',
            'microschool': r'\bmicroschool|micro-school|pod\b',
            'roadschooling': r'\broadschool|rv.*school|travel.*school\b',
            'worldschooling': r'\bworldschool\b',
            'college-prep': r'\bcollege|university|sat|act\b',
            'career': r'\bcareer|job|work|employ|trade|vocation\b',
            'entrepreneurship': r'\bentrepreneur|business|startup\b',
            'technology': r'\btechnology|tech|digital|online|virtual\b',
            'outdoor': r'\boutdoor|nature|forest|garden\b',
            'faith-based': r'\bfaith|religious|christian|catholic\b',
            'secular': r'\bsecular|non-religious\b'
        }
        
        for tag, pattern in topic_patterns.items():
            if re.search(pattern, content_lower):
                tags.append(tag)
        
        return list(set(tags))  # Remove duplicates
    
    def extract_tools_from_content(self, content, limit_lines=50):
        """Extract tool mentions from the first N lines of content"""
        tools = []
        # Get first N lines
        lines = content.split('\n')[:limit_lines]
        early_content = '\n'.join(lines).lower()
        
        for tool, pattern in self.tool_patterns.items():
            if re.search(pattern, early_content, re.IGNORECASE):
                tools.append(tool)
                self.tool_mentions[tool] += 1
        
        return tools
    
    def parse_markdown_file(self, file_path):
        """Parse a markdown file and extract metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if frontmatter_match:
                try:
                    metadata = yaml.safe_load(frontmatter_match.group(1))
                except:
                    metadata = {}
            else:
                metadata = {}
            
            # Get content after frontmatter
            if frontmatter_match:
                main_content = content[frontmatter_match.end():]
            else:
                main_content = content
            
            # Extract title
            title = metadata.get('title', '')
            if not title:
                title_match = re.search(r'^#\s+(.+)$', main_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
            
            # Extract tags and tools
            tags = self.extract_tags_from_content(main_content, title)
            tools = self.extract_tools_from_content(main_content)
            
            # Update tag frequency
            for tag in tags:
                self.tag_frequency[tag] += 1
            
            return {
                'file_path': str(file_path),
                'title': title,
                'type': metadata.get('type', 'unknown'),
                'date': metadata.get('date', ''),
                'summary': metadata.get('summary', ''),
                'tags': tags,
                'tools': tools,
                'url': metadata.get('url', ''),
                'existing_metadata': metadata
            }
        
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return None
    
    def analyze_directory(self):
        """Analyze all markdown files in the directory"""
        results = []
        
        for md_file in self.base_path.rglob('*.md'):
            if md_file.is_file():
                result = self.parse_markdown_file(md_file)
                if result:
                    results.append(result)
                    # Categorize by type
                    content_type = result['type']
                    self.content_stats[content_type].append(result)
        
        return results
    
    def generate_index(self, results):
        """Generate a comprehensive index with progressive disclosure"""
        index_content = """# Master Content Database Index

Generated: {date}
Total Files: {total}

## Content Distribution

{distribution}

## Tag Cloud

Most frequent tags:
{tag_cloud}

## Tools & Resources Mentioned

{tools_mentioned}

## Content by Type

### Blog Posts ({blog_count})

{blog_content}

### Daily Newsletters ({daily_count})

{daily_content}

### Podcast Episodes ({podcast_count})

{podcast_content}

### Announcements ({announcement_count})

{announcement_content}

## Content by Philosophy

{philosophy_content}

## Tools & Resources Index

{tools_index}

---
*Use this index to quickly find content by type, tag, or tool mention.*
""".format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            total=len(results),
            distribution=self._generate_distribution(),
            tag_cloud=self._generate_tag_cloud(),
            tools_mentioned=self._generate_tools_summary(),
            blog_count=len(self.content_stats.get('blog', [])),
            blog_content=self._generate_type_content('blog'),
            daily_count=len(self.content_stats.get('daily', [])),
            daily_content=self._generate_type_content('daily'),
            podcast_count=len(self.content_stats.get('podcast', [])),
            podcast_content=self._generate_type_content('podcast'),
            announcement_count=len(self.content_stats.get('announcement', [])),
            announcement_content=self._generate_type_content('announcement'),
            philosophy_content=self._generate_philosophy_content(results),
            tools_index=self._generate_tools_index(results)
        )
        
        return index_content
    
    def _generate_distribution(self):
        """Generate content distribution stats"""
        lines = []
        for content_type, items in sorted(self.content_stats.items()):
            lines.append(f"- **{content_type.title()}**: {len(items)} files")
        return '\n'.join(lines)
    
    def _generate_tag_cloud(self):
        """Generate tag frequency cloud"""
        top_tags = self.tag_frequency.most_common(20)
        lines = []
        for tag, count in top_tags:
            lines.append(f"- `{tag}` ({count})")
        return '\n'.join(lines)
    
    def _generate_tools_summary(self):
        """Generate tools mention summary"""
        lines = []
        for tool, count in self.tool_mentions.most_common(10):
            lines.append(f"- **{tool}**: mentioned in {count} files")
        return '\n'.join(lines)
    
    def _generate_type_content(self, content_type):
        """Generate content listing for a specific type"""
        items = self.content_stats.get(content_type, [])
        if not items:
            return "*No content found*"
        
        lines = []
        # Sort by date (newest first)
        sorted_items = sorted(items, key=lambda x: x.get('date', ''), reverse=True)
        
        for item in sorted_items[:50]:  # Limit to 50 most recent
            date_str = item.get('date', 'undated')
            tags_str = ', '.join(item['tags'][:5]) if item['tags'] else 'untagged'
            tools_str = ', '.join(item['tools']) if item['tools'] else ''
            
            line = f"- **{item['title']}** ({date_str})"
            if tags_str:
                line += f"\n  - Tags: `{tags_str}`"
            if tools_str:
                line += f"\n  - Tools: {tools_str}"
            if item.get('summary'):
                line += f"\n  - Summary: {item['summary'][:100]}..."
            
            lines.append(line)
        
        if len(items) > 50:
            lines.append(f"\n*...and {len(items) - 50} more*")
        
        return '\n'.join(lines)
    
    def _generate_philosophy_content(self, results):
        """Group content by educational philosophy"""
        philosophy_groups = defaultdict(list)
        
        for result in results:
            for tag in result['tags']:
                if tag in self.philosophy_tags:
                    philosophy_groups[tag].append(result)
        
        lines = []
        for philosophy, items in sorted(philosophy_groups.items()):
            lines.append(f"### {philosophy.replace('-', ' ').title()} ({len(items)} items)")
            for item in items[:10]:
                lines.append(f"- {item['title']}")
            if len(items) > 10:
                lines.append(f"*...and {len(items) - 10} more*")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_tools_index(self, results):
        """Generate index of content by tools mentioned"""
        tools_groups = defaultdict(list)
        
        for result in results:
            for tool in result['tools']:
                tools_groups[tool].append(result)
        
        lines = []
        for tool, items in sorted(tools_groups.items()):
            lines.append(f"### {tool.replace('-', ' ').title()} ({len(items)} mentions)")
            for item in items[:5]:
                lines.append(f"- {item['title']} ({item['type']})")
            if len(items) > 5:
                lines.append(f"*...and {len(items) - 5} more*")
            lines.append("")
        
        return '\n'.join(lines)
    
    def create_frontmatter_update_script(self, results):
        """Create a script to update frontmatter with progressive disclosure"""
        script_content = """#!/usr/bin/env python3
\"\"\"
Update frontmatter in Master Content Database files to add tags for progressive disclosure.
Generated from analyze_master_content.py
\"\"\"

import re
import yaml
from pathlib import Path

updates = {updates_json}

def update_file(file_path, tags, tools):
    \"\"\"Update a single file's frontmatter\"\"\"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract existing frontmatter
        frontmatter_match = re.match(r'^---\\n(.*?)\\n---\\n', content, re.DOTALL)
        if frontmatter_match:
            metadata = yaml.safe_load(frontmatter_match.group(1))
            body = content[frontmatter_match.end():]
        else:
            print(f"No frontmatter found in {{file_path}}")
            return False
        
        # Add tags right after title
        metadata['tags'] = tags
        if tools:
            metadata['tools'] = tools
        
        # Rebuild file with updated frontmatter
        # Order matters: title, tags, tools, then rest
        ordered_metadata = {{'title': metadata.get('title', '')}}
        ordered_metadata['tags'] = tags
        if tools:
            ordered_metadata['tools'] = tools
        
        # Add remaining fields
        for key, value in metadata.items():
            if key not in ['title', 'tags', 'tools']:
                ordered_metadata[key] = value
        
        # Write back
        new_content = "---\\n"
        new_content += yaml.dump(ordered_metadata, default_flow_style=False, allow_unicode=True)
        new_content += "---\\n"
        new_content += body
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {{file_path}}: {{str(e)}}")
        return False

# Process updates
successful = 0
for file_path, data in updates.items():
    if update_file(file_path, data['tags'], data['tools']):
        successful += 1

print(f"Successfully updated {{successful}}/{{len(updates)}} files")
"""
        
        # Prepare updates data
        updates = {}
        for result in results:
            updates[result['file_path']] = {
                'tags': result['tags'],
                'tools': result['tools']
            }
        
        return script_content.format(updates_json=json.dumps(updates, indent=2))


def main():
    """Main execution function"""
    base_path = "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database"
    
    print(f"Analyzing Master Content Database at: {base_path}")
    
    analyzer = ContentAnalyzer(base_path)
    results = analyzer.analyze_directory()
    
    print(f"\nAnalyzed {len(results)} files")
    print(f"Found {len(analyzer.tag_frequency)} unique tags")
    print(f"Found {len(analyzer.tool_mentions)} unique tools")
    
    # Generate index
    index_content = analyzer.generate_index(results)
    index_path = Path(base_path).parent / "Master_Content_Index.md"
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\nIndex written to: {index_path}")
    
    # Generate update script
    update_script = analyzer.create_frontmatter_update_script(results)
    script_path = Path(base_path).parent / "Studio" / "update_frontmatter.py"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(update_script)
    
    print(f"Update script written to: {script_path}")
    
    # Save detailed results as JSON
    json_path = Path(base_path).parent / "Studio" / "content_analysis.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'analysis_date': datetime.now().isoformat(),
            'total_files': len(results),
            'content_types': {k: len(v) for k, v in analyzer.content_stats.items()},
            'top_tags': dict(analyzer.tag_frequency.most_common(50)),
            'tool_mentions': dict(analyzer.tool_mentions),
            'files': results
        }, f, indent=2)
    
    print(f"Detailed analysis saved to: {json_path}")


if __name__ == "__main__":
    main()