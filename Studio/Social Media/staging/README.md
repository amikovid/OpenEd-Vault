# Social Media Staging

**Frictionless path:** Markdown files here → GetLate API → Platforms

---

## How It Works

1. **Create post** as markdown file with frontmatter
2. **Run publish script** (or use Claude Code)
3. **GetLate API** schedules to configured platforms

No Notion. No intermediate database. Just markdown → publish.

---

## File Format

```markdown
---
platforms: [linkedin, twitter]      # Where to post
scheduled_for: 2026-01-20 09:00     # When (or "now" for immediate)
status: draft | ready | published
type: text | carousel | thread
---

Your post content here.

For threads, use --- to separate tweets.
```

---

## Folder Structure

```
staging/
├── README.md           # This file
├── drafts/             # Work in progress
├── ready/              # Approved, awaiting publish
└── published/          # Archive of sent posts
```

---

## Publishing

```bash
# Via script (TODO: create)
./publish-social.sh ready/my-post.md

# Via Claude Code
"Publish the LinkedIn post in staging/ready/"
```

---

## GetLate Integration

GetLate is configured with 8 platforms. API credentials in OpenEd .claude/settings.local.json

Supported platforms:
- LinkedIn (personal + company)
- X/Twitter
- Instagram
- Facebook
- Others as configured

---

*Principle: Source of truth is markdown. Everything else is just a viewer or publisher.*
