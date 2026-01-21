# Lead Magnet Automation

End-to-end skill for launching "comment [KEYWORD] to get it" lead magnets.

---

## When to Use

When you have lead magnet content ready and need to:
1. Publish it to Notion
2. Set up comment-to-DM automation (Instagram)
3. Create social assets

---

## Workflow

### Step 1: Publish to Notion

**Method:** Direct Notion API calls (see `/.claude/skills/notion-publisher.md`)

**Parent page ID:** `8eea70ee-9462-4ccd-9603-536ef5021a7c` (Lead Magnet Templates)

**Process:**
1. Create page under parent using POST to `/v1/pages`
2. Add content in batches using PATCH to `/v1/blocks/{page_id}/children`
3. Use block types: `heading_2`, `heading_3`, `paragraph`, `quote`, `callout`, `bulleted_list_item`, `divider`

**API Token:** Stored in `.mcp.json` under `notion.env.NOTION_API_KEY`

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

### Step 3: Set Up ManyChat Automation (Instagram)

**IMPORTANT:** Instagram requires user engagement before you can send links. The flow must be:
1. User comments keyword
2. Bot asks them to reply
3. User replies
4. Bot sends the link

**PROMPT USER with full instructions + copy:**

```
Set up the ManyChat automation:

1. Go to manychat.com > Automation > + New Automation

2. NAME: [KEYWORD] Lead Magnet

3. TRIGGER:
   - Click "Add Trigger"
   - Select "Instagram" > "Comments"
   - Condition: "Comment contains keyword"
   - Keyword: [KEYWORD]
   - Case insensitive: ON

4. FIRST MESSAGE (no link yet):
   [INSERT MESSAGE 1 BELOW]

5. ADD CONDITION: Wait for Reply
   - Add "Wait for Reply" step
   - This captures their engagement

6. SECOND MESSAGE (after reply):
   [INSERT MESSAGE 2 BELOW]

7. Click "Publish" (top right)
```

---

### Message Templates

**Message 1 (engagement prompt):**
```
Hey! I'd love to send you [SHORT_DESCRIPTION]. Reply YES and I'll send it right over.
```

**Message 2 (deliver content + email ask):**
```
Here you go!

[PUBLIC_NOTION_URL]

[BRIEF_DESCRIPTION_OF_CONTENTS]

Quick question - what's the best email to send you more resources like this? We share stuff we don't post publicly.
```

**Message 3 (after email provided):**
```
Got it! You'll hear from us soon. [OPTIONAL_EXTRA_CTA]
```

---

### Step 4: Create Social Assets

**Caption Template:**
```
[Hook - speaks to the pain point]

[What they're getting - 3-4 bullet points with arrows]

Comment [KEYWORD] and I'll send it to your DMs.
```

**Example:**
```
Is your child struggling with reading?

Here's a free guide with:
→ 3 questions to know if it's a real problem
→ The "4th grade cliff" (and why early matters)
→ Free tools that actually work
→ When to suspect dyslexia

Comment READING and I'll send it to your DMs.
```

Save to: `Studio/Lead Magnet Project/[Name]-Social-Assets.md`

---

### Step 5: Post and Test

**PROMPT USER:**
```
Ready to launch:

1. Post your Reel/post with the caption
2. Test: Comment [KEYWORD] on the post from another account
3. Verify: Bot asks for reply
4. Reply YES
5. Verify: DM arrives with the correct link

Confirm when the test is complete.
```

---

## Checklist

```markdown
## Lead Magnet: [NAME]
Keyword: [KEYWORD]

- [ ] Content created
- [ ] Notion page created via direct API
- [ ] Notion page made PUBLIC
- [ ] Public URL obtained
- [ ] ManyChat automation created (2-step: engage then deliver)
- [ ] DM messages configured
- [ ] Caption created
- [ ] Post/Reel published
- [ ] Test: Commented keyword, replied, received DM
```

---

## Known Page IDs

| Page | ID |
|------|-----|
| Lead Magnet Templates | `8eea70ee-9462-4ccd-9603-536ef5021a7c` |
| Reading Guide | `2eeafe52-ef59-814d-a410-fe0583953011` |
| Confidence Scripts | `2e7afe52-ef59-81c5-b52a-c4a563f74808` |

---

## Related Skills

- `/.claude/skills/notion-publisher.md` - Direct API calls for Notion publishing
- `lead-magnet-generator.md` - Strategy and frameworks for creating lead magnets

---

*Updated: 2026-01-20*
