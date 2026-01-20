# Notion Lead Magnet Publisher

Publish lead magnet guides to Notion using the Rube MCP.

---

## When to Use

When you have a completed lead magnet guide (markdown) and need to publish it as a shareable Notion page.

---

## Prerequisites

- Lead magnet content ready in markdown
- Rube MCP connected with active Notion connection
- Parent page ID for lead magnets: `28cafe52-ef59-802b-8648-d4c0a3d51672` (LEAD MAGNET page)

---

## Workflow

### 1. Create the Page

Use `RUBE_SEARCH_TOOLS` to find Notion tools, then create the page:

```
Tool: NOTION_CREATE_PAGE_IN_PAGE
Arguments:
  - parent_page_id: "28cafe52-ef59-802b-8648-d4c0a3d51672"
  - title: "Lead Magnet Title Here"
```

Save the returned `page_id` for adding content.

### 2. Add Content in Batches

Use `NOTION_ADD_MULTIPLE_PAGE_CONTENT` to add content blocks.

**Constraints:**
- Max 100 blocks per API call
- Max 2000 characters per text block
- Markdown formatting (**bold**, *italic*, [links](url)) auto-parses

**Block Format:**
```json
{
  "parent_block_id": "page_id_here",
  "content_blocks": [
    {"content": "Heading Text", "block_property": "heading_2"},
    {"content": "Paragraph text with **bold** and *italic*.", "block_property": "paragraph"},
    {"content": "Quoted script text here.", "block_property": "quote"},
    {"content": "", "block_property": "divider"}
  ]
}
```

**Block Properties:**
| Type | Use For |
|------|---------|
| `heading_1` | Main sections |
| `heading_2` | Subsections |
| `heading_3` | Individual items (e.g., each objection) |
| `paragraph` | Body text, labels |
| `quote` | Scripts, responses to say |
| `bulleted_list_item` | Lists |
| `divider` | Section breaks |
| `callout` | Highlighted tips |

### 3. Batch Strategy

For a typical lead magnet:
- **Batch 1:** Intro + first 3-4 scripts
- **Batch 2:** Next 4-5 scripts
- **Batch 3:** Final scripts + CTA section

Each batch = one `NOTION_ADD_MULTIPLE_PAGE_CONTENT` call.

### 4. Manual Step: Make Public

User must manually publish the page:
1. Open page in Notion
2. Share > Publish to web
3. Copy public URL for DM automation

---

## Example: Scripts Lead Magnet Structure

```
heading_2: "First, Understand This"
paragraph: intro text

divider

heading_3: "\"What about socialization?\""
paragraph: "**What they're really asking:** ..."
paragraph: "**Script:**"
quote: "The actual script text..."

divider

[repeat for each objection]

heading_2: "Want More?"
paragraph: CTA and links
```

---

## Session Management

Always use the same session_id across all Rube calls:
```
session: {"id": "existing_session_id"}
```

Or generate new for first call:
```
session: {"generate_id": true}
```

---

## Known Page IDs

| Page | ID |
|------|-----|
| LEAD MAGNET parent | `28cafe52-ef59-802b-8648-d4c0a3d51672` |
| Confidence Scripts guide | `2e7afe52-ef59-81c5-b52a-c4a563f74808` |

---

*Created: 2026-01-13*
