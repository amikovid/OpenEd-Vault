# The OpenEd AI-First Content Engine

*How one person operates a complete content machine with Claude Code, 25+ specialized skills, and integrated workflows*

---

## The Challenge

Traditional content teams face an impossible math problem:

| Content Type | Frequency | People Required |
|--------------|-----------|-----------------|
| Daily newsletter | 4/week | 1 writer + 1 editor |
| Weekly podcast | 1/week | 1 producer + 1 editor |
| Blog articles | 2-4/month | 1-2 writers |
| Social posts | 5-10/day | 1 social manager |
| SEO content | Ongoing | 1 specialist |

**That's 5-7 people to maintain consistent quality across channels.**

But what if the bottleneck isn't people - it's process?

---

## The Insight

Content creation has predictable patterns. The same mental processes repeat:

- Research → Outline → Draft → Edit → Publish
- Source material → Multiple formats
- High performer → Spin variations

**Pattern recognition is what AI does best.**

The question isn't "Can AI write?" - it's "How do we encode our best processes so AI can execute them consistently?"

---

## The Solution: A Skills-Based Architecture

Instead of generic AI prompting, we built **specialized skills** - complete workflows encoded as markdown files that Claude Code loads on demand.

```
.claude/
├── skills/           # 25+ content production skills
├── references/       # On-demand context (brand, SEO, etc.)
├── sessions/         # Conversation history
└── settings.json     # Configuration
```

**Key insight:** Skills are portable, not project-bound. The same skill works anywhere in the vault.

---

## How Claude Code Works

### The .claude Folder

Every project contains a `.claude/` folder with:

| File/Folder | Purpose |
|-------------|---------|
| `skills/` | Specialized AI capabilities loaded on demand |
| `references/` | Context documents (brand voice, SEO data, etc.) |
| `sessions/` | Historical conversation transcripts |
| `settings.json` | MCP servers, API keys, configuration |

### Living Documents

| Document | Function |
|----------|----------|
| `CLAUDE.md` | Permanent instructions - what the AI needs to know |
| `NOW.md` | Current state - what's happening right now |
| `PROJECT.md` | Project-specific context (in each project folder) |

**These documents solve the context window problem.** Instead of re-explaining your project every conversation, the AI reads your documentation automatically.

---

## The Skills Library

### 25+ Production Skills

| Skill | Purpose | Key Feature |
|-------|---------|-------------|
| **text-content** | Social media posts | 360+ templates, platform routing |
| **image-prompt-generator** | AI image creation | Gemini API, style library |
| **podcast-production** | Episode workflow | 4 checkpoints to publication |
| **opened-daily-newsletter-writer** | Mon-Thu newsletters | Thought-Trend-Tool format |
| **quality-loop** | Iterative drafting | 5-judge quality gates |
| **open-education-hub-deep-dives** | SEO articles | Proprietary + SEO structure |
| **ghostwriter** | Human voice | Anti-AI pattern detection |
| **hook-and-headline-writing** | Headlines | 15 formulas, 4 U's test |
| **seo-research** | Keyword research | DataForSEO API |
| **transcript-polisher** | Audio → text | Preserve voice, clean up |
| **cold-open-creator** | Podcast hooks | 25-35 second openers |
| **youtube-title-creator** | Video titles | 119 proven formulas |
| **short-form-video** | Reels/TikTok/Shorts | Sponge-then-sharpen method |
| **video-caption-creation** | Video hooks | Triple Word Score system |
| **meta-ads-creative** | Facebook/Instagram ads | 6 Elements framework |

### How Skills Work

Skills are **markdown files** with three sections:

1. **Frontmatter** - Name, description, when to invoke
2. **Methodology** - The complete process
3. **References** - Supporting documents loaded on demand

```markdown
---
name: text-content
description: Create high-performing text posts using framework fitting...
---

# Text Content Skill

## Methodology
[Complete workflow...]

## Reference Loading
Load these files based on platform:
- LinkedIn: `references/linkedin/*.md`
- X: `references/platforms/x-twitter.md`
```

---

## Skill Deep Dive: text-content

**Purpose:** Create social media posts across LinkedIn, X, Facebook, Instagram using proven templates.

### Progressive Disclosure Architecture

Instead of loading 360+ templates every time, the skill routes to specific files:

```
text-content/
├── SKILL.md                    # Core methodology + routing
└── references/
    ├── templates/              # General-purpose (250+)
    │   ├── post-structures.md     # 100+ frameworks
    │   ├── linkedin-swipe-file.md # 86 templates
    │   ├── justin-welsh.md        # 30 templates
    │   └── one-liners.md          # 12 patterns
    ├── linkedin/               # Platform-specific (118)
    │   ├── engagement.md          # Drive comments
    │   ├── story.md               # Emotional connection
    │   ├── list.md                # Scannable value
    │   ├── contrarian.md          # Pattern interrupt
    │   ├── authority.md           # Build credibility
    │   └── community.md           # Relationship building
    ├── platforms/              # Heuristics
    │   ├── x-twitter.md           # "I wish I said that"
    │   ├── facebook.md            # Comments drive reach
    │   └── instagram-captions.md  # Visual-first
    └── methods/
        └── proliferation.md       # SCAMPER, 8 Desires, Vision
```

### The Workflow

1. **Identify the job** - Engagement? Authority? Story?
2. **Load ONE category** - Don't overwhelm with options
3. **Match concept to 5-10 templates** - Framework fitting
4. **Select best 1-2** - Human judgment
5. **Execute and iterate** - Draft, refine, approve

### Proliferation System

One winning post becomes 17+ variations:

| Method | Output |
|--------|--------|
| **SCAMPER** | 7 variations (Substitute, Combine, Adapt, Modify, Purpose, Eliminate, Reverse) |
| **8 Human Desires** | 8 reframes (Safety, Success, Enjoyment, Acceptance, Comfort, Freedom, Status) |
| **Vision/Anti-Vision** | 2-3 frames (what we're FOR, what we're AGAINST) |

---

## Skill Deep Dive: image-prompt-generator

**Purpose:** Generate professional, non-generic images using Gemini API (Nano Banana Pro).

### The Workflow

```
Brainstorm → Select → Optimize → Style → Generate → Iterate
```

### Style Library

| Style | Use Case |
|-------|----------|
| **watercolor-line** | Ink linework + watercolor, warm (DEFAULT for thumbnails) |
| **opened-editorial** | Brand colors, conceptual wit |
| **minimalist-ink** | High-contrast black and white |
| **newyorker-cartoon** | Single-panel observational humor |

### Key Principles

1. **No generic imagery** - No lightbulbs for "ideas," no books for "education"
2. **Natural language** - Brief like a creative director, not tag soup
3. **Maximum 2-3 elements** - If it feels busy, remove something
4. **Favor metaphor** - Compass with crayon needle > literal image of self-directed learning

### Output Routing

Images save alongside content, not in generic dumps:

| Content Type | Output Location |
|--------------|-----------------|
| Newsletter | `Studio/OpenEd Daily/[date]/` |
| Podcast | `Studio/Open Ed Podcasts/[episode]/` |
| Blog | `Studio/SEO Content Production/[article]/` |

---

## The Hub-and-Spoke Model

**One hub piece generates multiple spokes:**

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
|----------|-------|----------------|
| Podcast | `podcast-production` | Blog, clips, LinkedIn, newsletter |
| Deep Dive | `open-education-hub-deep-dives` | 3-5 LinkedIn, Twitter, newsletter |
| Newsletter | `opened-daily-newsletter-writer` | LinkedIn post, Twitter thread |

**After completing any hub, the system proactively offers spokes.**

---

## External Integrations

### APIs & MCP Servers

| Integration | Purpose | Status |
|-------------|---------|--------|
| **Notion MCP** | Content database, scheduling | Active |
| **Slack MCP** | Team alerts, content sharing | Active |
| **GetLate API** | Multi-platform social scheduling | 8 platforms |
| **DataForSEO** | Keyword research, SERP analysis | Active |
| **GA4** | Traffic analytics | Active |
| **Gemini 3 Flash** | Image generation, context processing | Active |
| **Webflow** | Website sync | Active |

### Data Flow

```
Source Material                Processing                 Distribution
─────────────────             ──────────────             ─────────────
Podcasts          ──┐
Slack             ──┤         ┌────────────┐            Social (8 platforms)
Articles          ──┼────────▶│   Skills   │────────────▶Website
Expert Interviews ──┤         └────────────┘            Newsletter
Analytics         ──┘                                   Notion (scheduling)
```

---

## The Content Library

### Master Content Database

**415 published pieces** organized by format:

| Format | Count | Location |
|--------|-------|----------|
| Daily Newsletters | 200+ | `Content/Master Content Database/Daily Newsletters/` |
| Podcast Episodes | 50+ | `Content/Master Content Database/Podcast Episodes/` |
| Blog Posts | 100+ | `Content/Master Content Database/Blog Posts/` |
| Thinker Profiles | 6 | `Content/Master Content Database/Profiles/` |

### Content Index

`Master_Content_Index.md` provides searchable metadata:

- Tags for topic-based discovery
- Tools/resources referenced
- Summary for quick scanning
- Internal linking opportunities

---

## Active Workflows

### Daily Newsletter (Mon-Thu)

**Skill:** `opened-daily-newsletter-writer`
**Format:** Thought-Trend-Tool (~500-800 words)

```
1. Source material (Slack, podcasts, events)
        ↓
2. Identify segments (1 Thought, 1 Trend, 1 Tool)
        ↓
3. Draft with voice guidance
        ↓
4. Quality check (anti-AI patterns)
        ↓
5. Publish via Notion
```

### Podcast Production

**Skill:** `podcast-production`
**4 Checkpoint System:**

1. **Checkpoint 1:** Transcript → Key moments identified
2. **Checkpoint 2:** Blog outline approved
3. **Checkpoint 3:** Social package drafted
4. **Checkpoint 4:** All assets finalized

### SEO Content

**Skill:** `open-education-hub-deep-dives`
**Workflow:**

1. Keyword research (DataForSEO)
2. Source material compilation (GraphRAG search)
3. SEO outline with keyword targeting
4. Quality loop drafting (5 judges)
5. Internal linking (from Master Index)

---

## Analytics & Intelligence

### Data Sources

| Source | Purpose | Access |
|--------|---------|--------|
| **DataForSEO** | Keywords, SERP, competitors | API |
| **GA4** | Traffic, engagement, conversions | API |
| **GSC** | Search performance, rankings | Pending |
| **Notion** | Content scheduling, status | MCP |

### SEO Commands

The system includes ready-to-use SEO research commands:

- `quick-wins` - Low-difficulty keywords with traffic potential
- `content-gaps` - What competitors rank for that we don't
- `keyword-research` - Full keyword exploration

---

## Active Projects

| Project | Status | Key Files |
|---------|--------|-----------|
| **Eddie Awards** | Website planning | `Studio/Eddie Awards/PROJECT.md` |
| **Meta Ads** | 100 concepts ready | `Studio/Meta Ads/PROJECT.md` |
| **SEO Content** | Ongoing production | `Studio/SEO Content Production/PROJECT.md` |
| **Lead Magnet** | Quiz development | `Studio/Lead Magnet Project/` |
| **Guest Contributors** | 4 emails ready | `Studio/SEO Content Production/Guest Contributors/` |

### This Week

- [ ] Send 4 contributor outreach emails
- [ ] Daily newsletters (Mon-Thu)
- [ ] Weekly podcast episode
- [ ] Test short-form-video skill

---

## Writing Guardrails

### Hard Rules

| Rule | Reason |
|------|--------|
| **No correlative constructions** | "#1 AI tell" - Never "X isn't just Y - it's Z" |
| **Dash consistency** | Hyphens with spaces - like this |
| **No emojis in body** | Professional voice |

### Words to Avoid

> delve, comprehensive, crucial, vital, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge

### Phrases to Avoid

> "The best part? ..." / "What if I told you..." / "Here's the thing..." / "In today's fast-paced..." / "Let's be honest..."

### The Anti-AI Test

Before publishing: **Does this sound like something a human would actually say?**

- Read it aloud
- Check for staccato patterns
- Verify quotes are real
- Ensure internal links exist

---

## The Result

### What One Person Can Produce

| Output | Frequency | Time Investment |
|--------|-----------|-----------------|
| Daily newsletters | 4/week | ~30 min each |
| Weekly podcast | 1/week | ~2-3 hours |
| SEO articles | 2-4/month | ~1-2 hours each |
| Social posts | 5-10/day | Batched weekly |

### The Multiplier Effect

```
Traditional: 1 podcast = 1 podcast
AI-Augmented: 1 podcast = blog + 5 social + newsletter segment + clips
```

---

## Why This Works

### 1. Skills > Prompts

Generic prompting produces generic content. Encoded workflows produce consistent quality.

### 2. Progressive Disclosure

Load only what you need. 360 templates are useless if you're overwhelmed. Route to 10 relevant ones.

### 3. Human in the Loop

AI drafts, human approves. AI suggests, human selects. AI proliferates, human curates.

### 4. Living Documentation

Context persists across sessions. No re-explaining your project. The AI reads your docs.

### 5. Hub-and-Spoke Thinking

Every piece of content is a potential hub. Train yourself to see the spokes.

---

## Getting Started

### Minimum Viable Setup

1. Create `.claude/` folder in your project
2. Write a `CLAUDE.md` with project context
3. Create `NOW.md` for current state
4. Build one skill for your most common task

### Growing the System

1. Document processes that repeat
2. Encode them as skills
3. Build reference libraries
4. Add integrations as needed

### The Philosophy

> "File over app" - Your knowledge lives in markdown files you control, not locked in proprietary tools.

---

## Questions?

**Resources:**

- Vault structure: `CLAUDE.md`
- Current state: `NOW.md`
- All skills: `.claude/skills/`
- Published content: `Content/Master Content Database/`

---

*Built with Claude Code + human judgment*
*OpenEd Alternative Education - 9 states*
