# Slack Social Distribution Skill

Post social media content to Slack for team review and distribution coordination.

---

## When to Use

After creating social media content (from newsletters, podcasts, or deep dives), post to `#market-daily` for:
- Team visibility on what's ready to publish
- Copyable content for each platform
- Coordination on posting schedule

---

## Channel

**#market-daily** - `C07U9S53TLL`

---

## Workflow

### Step 1: Create Parent Message

Post a summary message announcing the content package:

```markdown
📰 **[Content Title]: [Date]**

Published content ready for social distribution:

**Newsletter:** [Title]
**Blog Post:** [URL]
**Webflow Status:** [Draft/Published]

**Theme:** [1-line summary]

Social posts for each platform in thread below 👇
```

### Step 2: Add Platform Replies

Reply to the parent message with content for each platform. One reply per platform:

| Platform | Emoji | Notes |
|----------|-------|-------|
| LinkedIn | 🔗 | Full post with hook and body |
| X/Twitter Thread | 🐦 | Numbered tweets (Tweet 1, Tweet 2, etc.) |
| X/Twitter Singles | 🐦 | Standalone quotables (Option A, B, C) |
| Instagram Stories | 📸 | Slide-by-slide breakdown |
| Facebook | 📘 | Community-focused version |

### Step 3: Include Handles

For tagged content, include the handles in posts:
- `@michaelbhorn` (Michael Horn)
- `@KenColeman` (Ken Coleman)
- `@mikeroweworks` (Mike Rowe)
- `@SmartPathHQ` (SmartPath)

Check `Studio/_content-engine-refactor/nearbound/` for more handles.

---

## Message Format

Each platform reply should include:

1. **Platform header** with emoji
2. **Horizontal rule** (`---`)
3. **Content** formatted for that platform
4. For threads: number each tweet
5. For options: label as Option A, B, C

**Example LinkedIn:**
```markdown
**🔗 LinkedIn Post (Deep Dive Feature)**

---

**Hook:** [Opening line]

**Body:**
[Full post content]

Link in comments.
```

**Example X Thread:**
```markdown
**🐦 X/Twitter Thread (Topic)**

---

**Tweet 1:**
[Content]

**Tweet 2:**
[Content]

...
```

---

## API Reference

**Post to channel:**
```
mcp__slack__conversations_add_message
- channel_id: C07U9S53TLL
- payload: [markdown content]
- content_type: text/markdown
```

**Reply to thread:**
```
mcp__slack__conversations_add_message
- channel_id: C07U9S53TLL
- thread_ts: [parent message timestamp]
- payload: [markdown content]
- content_type: text/markdown
```

---

## Integration with Content Workflow

This skill pairs with:
- `newsletter-to-social` - Generates the social content
- `webflow-publish` - Publishes the blog post
- `text-content` - Template matching for posts

**Typical flow:**
1. Create newsletter/content
2. Generate social slate using `newsletter-to-social`
3. Publish blog to Webflow using `webflow-publish`
4. Post to Slack using this skill
5. Team reviews and schedules posts

---

## Example Session

```
User: Post the Jan 24 newsletter social content to Slack

Claude:
1. Posts parent message to #market-daily with newsletter summary
2. Adds LinkedIn post as reply
3. Adds X thread as reply
4. Adds X singles as reply
5. Adds Instagram stories as reply
6. Adds Facebook post as reply
```

---

*Created: 2026-01-23*
