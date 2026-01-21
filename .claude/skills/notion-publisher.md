# Notion Publisher

Publish content to Notion pages using direct API calls.

---

## When to Use

- Publishing lead magnets, guides, or structured content to Notion
- Creating shareable Notion pages for ManyChat delivery
- Any time you need to programmatically add content to Notion

---

## Prerequisites

1. **Notion API Token** in `.mcp.json`:
   ```json
   "notion": {
     "env": {
       "NOTION_API_KEY": "ntn_..."
     }
   }
   ```

2. **Page shared with integration**: In Notion, the target page must be connected to "Claude Code" via Share > Connections

3. **Token refresh**: If you get 401 errors, get a new token from https://www.notion.so/my-integrations

---

## API Reference

### Test Connection

```bash
curl -s -X GET "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

### Search for Pages

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "Page Name", "page_size": 10}'
```

### Create Page

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "PARENT_PAGE_ID"},
    "icon": {"type": "emoji", "emoji": "📚"},
    "properties": {
      "title": [{"text": {"content": "Page Title Here"}}]
    }
  }'
```

Returns: `page_id` to use for adding content.

### Add Content Blocks

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/PAGE_ID/children" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      ... block objects ...
    ]
  }'
```

---

## Block Types

### Paragraph
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"type": "text", "text": {"content": "Plain text here"}}]
  }
}
```

### Paragraph with formatting
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {"type": "text", "text": {"content": "Bold text."}, "annotations": {"bold": true}},
      {"type": "text", "text": {"content": " Normal text."}}
    ]
  }
}
```

### Heading 2
```json
{
  "object": "block",
  "type": "heading_2",
  "heading_2": {
    "rich_text": [{"type": "text", "text": {"content": "Section Title"}}]
  }
}
```

### Heading 3
```json
{
  "object": "block",
  "type": "heading_3",
  "heading_3": {
    "rich_text": [{"type": "text", "text": {"content": "Subsection"}}]
  }
}
```

### Bulleted List Item
```json
{
  "object": "block",
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{"type": "text", "text": {"content": "List item text"}}]
  }
}
```

### Quote
```json
{
  "object": "block",
  "type": "quote",
  "quote": {
    "rich_text": [{"type": "text", "text": {"content": "Quoted text here"}}]
  }
}
```

### Callout (with emoji icon)
```json
{
  "object": "block",
  "type": "callout",
  "callout": {
    "rich_text": [{"type": "text", "text": {"content": "Important note here"}}],
    "icon": {"type": "emoji", "emoji": "⚠️"}
  }
}
```

### Divider
```json
{
  "object": "block",
  "type": "divider",
  "divider": {}
}
```

### Link in text
```json
{
  "type": "text",
  "text": {"content": "Link Text", "link": {"url": "https://example.com"}}
}
```

---

## Rich Text Annotations

Available annotations for any text span:
- `"bold": true`
- `"italic": true`
- `"strikethrough": true`
- `"underline": true`
- `"code": true`

Example combining multiple:
```json
{
  "type": "text",
  "text": {"content": "Important link", "link": {"url": "https://..."}},
  "annotations": {"bold": true, "italic": true}
}
```

---

## Batching Strategy

**Constraints:**
- Max 100 blocks per API call
- Max 2000 characters per text block

**Typical lead magnet batching:**
- Batch 1: Intro + first 2-3 sections
- Batch 2: Middle sections
- Batch 3: Final sections + CTA

Each batch = one PATCH call to `/blocks/{page_id}/children`

---

## Complete Workflow Example

### 1. Find parent page
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "Lead Magnet Templates"}'
```

### 2. Create new page
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "PARENT_ID_FROM_STEP_1"},
    "icon": {"type": "emoji", "emoji": "📖"},
    "properties": {
      "title": [{"text": {"content": "My Lead Magnet Title"}}]
    }
  }'
# Save the returned page ID
```

### 3. Add content (batch 1)
```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/NEW_PAGE_ID/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Intro text..."}, "annotations": {"italic": true}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "First Section"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Section content..."}}]}}
    ]
  }'
```

### 4. Repeat for additional batches

### 5. Manual: Publish to web
User goes to Notion > Share > Publish to get public URL.

---

## Known Page IDs (OpenEd)

| Page | ID |
|------|-----|
| Lead Magnet Templates | `8eea70ee-9462-4ccd-9603-536ef5021a7c` |

---

## Escaping in Bash

When using curl in bash, escape:
- Single quotes in content: `'\''` (end quote, escaped quote, start quote)
- Double quotes in JSON: `\"`

Example:
```bash
"content": "What'\''s the problem?"  # produces: What's the problem?
"content": "She said \"hello\""      # produces: She said "hello"
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired/invalid | Get new token from Notion integrations |
| 404 Object not found | Page not shared with integration | Share page with "Claude Code" in Notion |
| 400 Validation error | Malformed JSON or invalid block type | Check JSON structure, escape quotes |

---

## Lead Magnet Specific Notes

**Structure that works:**
1. Italic subtitle/attribution line
2. Divider
3. H2: Hook section (the problem)
4. H2: The solution/framework
5. Bulleted quick wins
6. Callout for urgent warning
7. H2: Resources with links
8. Divider
9. CTA paragraph with OpenEd link

**Final step:** User publishes to web, copies URL for ManyChat flow.

---

*Updated: 2026-01-20*
