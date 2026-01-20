# Lead Magnet Automation

End-to-end skill for launching "comment [KEYWORD] to get it" lead magnets.

---

## When to Use

When you have lead magnet content ready and need to:
1. Publish it to Notion
2. Set up comment-to-DM automation
3. Create social assets

---

## Workflow

### Step 1: Publish to Notion

**Tool:** Rube MCP with `NOTION_ADD_MULTIPLE_PAGE_CONTENT`

**Parent page ID:** `28cafe52-ef59-802b-8648-d4c0a3d51672` (LEAD MAGNET)

**Process:**
1. Create page under parent
2. Add content in batches (~25 blocks per call)
3. Use block types: `heading_2`, `heading_3`, `paragraph`, `quote`, `divider`

**Constraints:**
- Max 100 blocks per API call
- Max 2000 characters per text block
- Markdown auto-parses: **bold**, *italic*, [links](url)

**Block format:**
```json
{
  "parent_block_id": "page_id_here",
  "content_blocks": [
    {"content": "Section Title", "block_property": "heading_2"},
    {"content": "Body text with **bold**.", "block_property": "paragraph"},
    {"content": "Script text to say out loud.", "block_property": "quote"},
    {"content": "", "block_property": "divider"}
  ]
}
```

---

### Step 2: Make Notion Page Public

**PROMPT USER:**
```
The Notion page is created but not public yet.

To make it shareable:
1. Open the page in Notion
2. Click "Share" (top right)
3. Click "Publish" tab
4. Toggle "Publish to web" ON
5. Copy the public URL

Paste the public URL here when ready.
```

---

### Step 3: Set Up ManyChat Automation

**PROMPT USER with full instructions + copy:**

```
Set up the ManyChat automation:

1. Go to manychat.com → Automation → + New Automation

2. NAME: [KEYWORD] Lead Magnet

3. TRIGGER:
   - Click "Add Trigger"
   - Select "Instagram" → "Comments"
   - Condition: "Comment contains keyword"
   - Keyword: [KEYWORD]
   - Case insensitive: ON

4. ACTION:
   - Click "Add Action" → "Send Message"
   - Message type: Text
   - Paste this message:

---
[DM MESSAGE - INSERT BELOW]
---

5. Click "Publish" (top right) to set automation LIVE

The automation is now active. When someone comments [KEYWORD] on any post, they'll receive the DM automatically.
```

**DM Message Template:**
```
Here are your [SHORT_DESCRIPTION]:

[PUBLIC_NOTION_URL]

From OpenEd
```

---

### Step 4: Create Social Assets

Generate caption for the Reel/post.

**Caption Template:**
```
[Hook - one line that complements the video]

[Value prop - what they're getting, 1-2 lines]

Comment [KEYWORD] and we'll send it.
```

**Hashtags:**
```
#homeschool #homeschoolmom #homeschooling #alternativeeducation #homeschoollife
```

Save to: `Studio/Lead Magnet Project/Quick Guides/[Name]-Social-Assets.md`

---

### Step 5: Post and Test

**PROMPT USER:**
```
Ready to launch:

1. Post your Reel with the caption
2. Test: Comment [KEYWORD] on the post from another account
3. Verify: DM arrives with the correct link

Confirm when the test DM is received.
```

---

## Checklist

```markdown
## Lead Magnet: [NAME]
Keyword: [KEYWORD]

- [ ] Content created (markdown)
- [ ] Notion page created via Rube MCP
- [ ] Notion page made PUBLIC
- [ ] Public URL obtained
- [ ] ManyChat automation created
- [ ] DM message configured with public URL
- [ ] Caption created
- [ ] Reel posted
- [ ] Test: Commented keyword, received DM
```

---

## Example: Confidence Scripts

**Keyword:** SCRIPTS

**Notion page ID:** `2e7afe52-ef59-81c5-b52a-c4a563f74808`

**DM message:**
```
Here are your scripts for the 7 conversations you've been dreading.

Word-for-word responses for when family and friends question your homeschool:

[PUBLIC_URL]

From OpenEd
```

**Caption:**
```
The hardest part isn't the teaching. You're already their teacher.

The hardest part is the awkward conversations with the doubters.

We put together scripts you can use to handle those conversations.

Comment SCRIPTS and we'll send them.
```

---

## Known Page IDs

| Page | ID |
|------|-----|
| LEAD MAGNET parent | `28cafe52-ef59-802b-8648-d4c0a3d51672` |
| Confidence Scripts | `2e7afe52-ef59-81c5-b52a-c4a563f74808` |

---

*Created: 2026-01-13*
