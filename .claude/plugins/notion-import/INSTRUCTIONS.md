# Notion Import Plugin

This plugin provides a `/notion-import` command to quickly import markdown files into Notion.

## Usage

```
/notion-import <file-path> [title] [--parent "Parent Page Name"]
```

## Examples

1. Import with auto-generated title:
   ```
   /notion-import test.md
   ```

2. Import with custom title:
   ```
   /notion-import content.md "My Custom Title"
   ```

3. Import to specific parent page:
   ```
   /notion-import blog-post.md --parent "Blog Drafts"
   ```

## Process

When the user runs `/notion-import`:

1. **Parse the command** to extract:
   - File path (required)
   - Title (optional - use filename if not provided)
   - Parent page (optional - use "To Sort" if not provided)

2. **Read the markdown file**

3. **Find parent page in Notion** (if specified):
   - Use NOTION_SEARCH_NOTION_PAGE with the parent name
   - Default to "To Sort" (ID: 2aaafe52-ef59-8058-b649-e3960bef82bb)

4. **Create the Notion page**:
   - Use NOTION_CREATE_NOTION_PAGE with parent ID and title

5. **Convert and import content**:
   - Parse markdown into blocks
   - Use NOTION_ADD_MULTIPLE_PAGE_CONTENT
   - Handle formatting: **bold**, *italic*, ~~strike~~, `code`, [links](url)
   - Convert headings, lists, code blocks, quotes

6. **Report success** with link to created page

## Implementation Notes

- Use the Composio RUBE tools for Notion operations
- Auto-split content over 2000 characters
- Skip tables (require separate API)
- Add 📝 emoji to page by default

## Error Handling

- File not found: Clear error message
- Parent page not found: Use default "To Sort"
- Import failures: Report specific issue

## Token Optimization

To minimize tokens:
- Batch all content into single ADD_MULTIPLE_PAGE_CONTENT call
- Only search for parent if not using default
- Skip schema loading if parameters are known