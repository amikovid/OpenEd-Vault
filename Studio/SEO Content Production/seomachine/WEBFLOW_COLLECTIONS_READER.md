# Webflow Collections Reader

A simple tool to read and search the Tools and Subjects collections from Webflow without syncing to markdown.

## Usage

### View All Tools
```bash
./read_webflow_collections.py tools
```

### View All Subjects
```bash
./read_webflow_collections.py subjects
```

### Search Tools by Keyword
```bash
./read_webflow_collections.py search --keyword "math"
./read_webflow_collections.py search -k "reading"
```

### Export to JSON (for offline access)
```bash
# Export tools collection
./read_webflow_collections.py export --collection tools

# Export subjects collection
./read_webflow_collections.py export --collection subjects

# Export posts collection (if needed)
./read_webflow_collections.py export --collection posts
```

## Features

- **Read-only access** - No modifications to Webflow
- **Search functionality** - Find tools by keyword
- **JSON export** - Save collections for offline use
- **No markdown sync** - Just displays or exports data

## Use Cases

1. **Quick lookups** - When you need to check what tools are available
2. **Offline access** - Export to JSON and grep/search locally
3. **Integration** - Use the exported JSON in other scripts
4. **Reference** - Keep a snapshot of collections at a point in time

## Python API Usage

You can also use it as a module:

```python
from read_webflow_collections import WebflowReader

reader = WebflowReader()

# Get all tools
tools = reader.get_collection_items(os.getenv('WEBFLOW_TOOLS_COLLECTION_ID'))

# Search for specific tools
reader.search_tools("math")
```

## Note

This tool uses the same `.env` configuration as the main sync script, so no additional setup is needed.