# OpenEd Content Engine

An AI-first content production system for OpenEd - alternative education company creating newsletters, podcasts, social media, SEO content, and educational resources.

**Operating States:** AR, IN, IA, KS, MN, MT, NV, OR, UT (9 states)

---

## What This Is

This is a Claude Code workspace with **39 specialized skills** that enable one person to operate a complete content machine. Instead of generic AI prompting, we built specialized workflows encoded as markdown files that Claude loads on demand.

### The Challenge It Solves

Traditional content teams need 5-7 people:

- Daily newsletter (4/week) - 1 writer + 1 editor

- Weekly podcast - 1 producer + 1 editor

- Blog articles (2-4/month) - 1-2 writers

- Social posts (5-10/day) - 1 social manager

- SEO content (ongoing) - 1 specialist

**This system lets one person maintain consistent quality across all channels.**

---

## Quick Start

### 1\. Clone and Setup

```bash
git clone [repo-url]
cd OpenEd-Vault
```

### 2\. Copy Environment Files

```bash
# Root level
cp .env.example .env

# Claude settings
cp .claude/settings.local.example.json .claude/settings.local.json

# Curriculove app (if using)
cp Studio/Lead\ Magnet\ Project/curriculove/.env.example \
   Studio/Lead\ Magnet\ Project/curriculove/.env.local
```

### 3\. Add Your API Keys

Edit each `.env` file with your credentials. See the `.example` files for what's needed.

### 4\. Open with Claude Code

```bash
claude
```

Claude will automatically read `CLAUDE.md` for context.

---

## Folder Structure

```
OpenEd Vault/
├── CLAUDE.md                    # AI instructions (auto-loaded)
├── NOW.md                       # Current state, priorities
├── Master_Content_Index.md      # 406 published articles indexed
│
├── Studio/                      # Active projects
│   ├── OpenEd Daily/            # Mon-Thu newsletter workflow
│   ├── Open Ed Podcasts/        # Weekly podcast workflow
│   ├── SEO Content Production/  # Blog articles
│   ├── Meta Ads/                # Ad creative library
│   ├── Lead Magnet Project/     # Curriculove quiz app
│   └── Social Media/            # Format inventory
│
├── Content/                     # Published archive
├── CRM/                         # Contact database (382)
├── Archive/                     # Historical content
│
└── .claude/
    ├── skills/                  # 39 production skills
    ├── references/              # On-demand context docs
    └── sessions/                # Conversation history
```

---

## Key Skills

| Skill | Purpose | Key Feature |
| --- | --- | --- |
| text-content | Social posts | 360+ templates, platform routing |
| podcast-production | Episode workflow | 4 checkpoints to publish |
| opened-daily-newsletter-writer | Mon-Thu newsletters | Thought-Trend-Tool format |
| quality-loop | Iterative drafting | 5-judge quality gates |
| image-prompt-generator | AI images | Gemini API, style library |
| ghostwriter | Human voice | Anti-AI pattern detection |
| short-form-video | Reels/TikTok | Sponge-then-sharpen method |
| seo-research | Keywords | DataForSEO integration |

### How Skills Work

Skills are markdown files with:

1. **Frontmatter** - Name, description, when to invoke

2. **Methodology** - Complete process

3. **References** - Supporting docs loaded on demand

Invoke with: `/skill-name` or "use the \[skill-name\] skill"

---

## Hub-and-Spoke Model

One hub piece generates multiple spokes:

```
                    ┌─────────────────┐
                    │    PODCAST      │
                    │   (Hub Piece)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Blog Post   │   │    Social     │   │  Newsletter   │
│   (Spoke)     │   │   (Spoke)     │   │   (Spoke)     │
└───────────────┘   └───────────────┘   └───────────────┘
```

| Hub Type | Skill | Natural Spokes |
| --- | --- | --- |
| Podcast | podcast-production | Blog, clips, LinkedIn, newsletter |
| Deep Dive | open-education-hub-deep-dives | 3-5 LinkedIn, Twitter, newsletter |
| Newsletter | opened-daily-newsletter-writer | LinkedIn post, Twitter thread |

---

## Writing Rules

**Hard rules for all public content:**

### Never Use Correlative Constructions

- ❌ "X isn't just Y - it's Z"

- ❌ "It's not about X, it's about Y"

- This is the #1 AI tell

### Avoid AI-isms

**Words:** delve, comprehensive, crucial, leverage, landscape, navigate, foster, paradigm, journey, tapestry, myriad, seamless

**Phrases:**

- "The best part? ..." / "The secret? ..."

- "What if I told you..."

- "In today's fast-paced..."

- Staccato patterns: "No fluff. No filler. Just results."

### Dash Style

- ✅ Use hyphens with spaces - like this

- ❌ Never em dashes

---

## External Integrations

| Service | Purpose | Setup |
| --- | --- | --- |
| Notion | Content database | MCP server in settings.local.json |
| DataForSEO | Keyword research | Credentials in .env |
| GetLate | Social scheduling | API key in .env |
| Webflow | Blog sync | API key in .env |
| Gemini | AI images, long context | API key in .env |
| ManyChat | Instagram automation | API key in .env |

---

## Key Files

| File | Purpose |
| --- | --- |
| CLAUDE.md | AI instructions, auto-loaded |
| NOW.md | Current state, priorities, blockers |
| Master_Content_Index.md | 406 published articles by tag |
| Studio/Social Media/FORMAT_INVENTORY.md | Social format guide with scoring |
| .claude/references/opened-program-details.md | Program specifics by state |

---

## Development

### Curriculove App

```bash
cd Studio/Lead\ Magnet\ Project/curriculove
npm install
npm run dev
```

### Webflow Sync

```bash
python3 agents/webflow_sync_agent.py
```

---

## Security Notes

- **Never commit `.env` files** - Use `.env.example` templates

- **Never commit `settings.local.json`** - Contains API keys

- Share credentials via secure channel (Slack, 1Password)

---

## Support

For questions about:

- **Content workflows** - Check skill files in `.claude/skills/`

- **Current state** - Read `NOW.md`

- **Project specifics** - See `PROJECT.md` in each Studio folder

---

*Built with Claude Code. Last updated: 2026-01-15*