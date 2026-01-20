# OpenEd Vault - Master Context

**Content production system for OpenEd** - Alternative education company creating newsletters, podcasts, social media, SEO content, and educational resources.

**Operating States:** AR, IN, IA, KS, MN, MT, NV, OR, UT (9 states)
**Program Details:** `.claude/references/opened-program-details.md`

---

## Start Here

| Need | Go To |
|------|-------|
| **Current state / priorities** | `NOW.md` |
| **Project context** | `Studio/[project]/PROJECT.md` |
| **Published content** | `Master_Content_Index.md` (406 articles by tag) |

---

## Where Things Live

| Need | Go To |
|------|-------|
| **Daily/Weekly newsletter** | `Studio/OpenEd Daily/` + skill: `opened-daily-newsletter-writer` |
| **SEO content** | `Studio/SEO Content Production/PROJECT.md` |
| **Podcast workflow** | `Studio/Open Ed Podcasts/` + skill: `podcast-production` |
| **Social posts** | skill: `text-content` + `Studio/Social Media/FORMAT_INVENTORY.md` |
| **Short-form video** | skill: `short-form-video` + `video-caption-creation` |
| **Meta ads** | `Studio/Meta Ads/PROJECT.md` |
| **Notion schema** | `.claude/references/notion-content-schema.md` |

---

## Studio Projects

Each project has a `PROJECT.md` with full context. Navigate there first.

| Project | Location | Status |
|---------|----------|--------|
| **Lead Magnet** | `Studio/Lead Magnet Project/` | Active (curriculove app) |
| **Meta Ads** | `Studio/Meta Ads/PROJECT.md` | 100 concepts ready |
| **SEO Content** | `Studio/SEO Content Production/PROJECT.md` | Active |
| **Eddie Awards** | `Studio/Eddie Awards/PROJECT.md` | Planning |
| **KPI Discussions** | `Studio/KPI Discussions/PROJECT.md` | Active |
| **Retargeting** | `Studio/Retargeting Strategy FY26-27/PROJECT.md` | Planning |

### Ongoing Workflows

| Workflow | Location | Cadence |
|----------|----------|---------|
| **OpenEd Daily** | `Studio/OpenEd Daily/` | Mon-Thu |
| **Podcasts** | `Studio/Open Ed Podcasts/` | Weekly |
| **Open Education Hub** | `Studio/Open Education Hub/` | As needed |

---

## Writing Rules

**CRITICAL: Apply to ALL public-facing content.**

### Hard Rules (Never Break)

**No correlative constructions:**
- Never: "X isn't just Y - it's Z"
- Never: "It's not about X, it's about Y"
- This is the #1 AI tell - find another way

**Dash consistency:**
- Use: hyphens with spaces - like this
- Never: em dashes

**No emojis** in body content (rare exceptions for social captions).

### AI-isms to Avoid

**Words:** delve, comprehensive, crucial, vital, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge

**Phrases:**
- "The best part? ..." / "The secret? ..."
- "What if I told you..." / "Here's the thing..." / "Let's be honest..."
- "In today's fast-paced..." / "In the ever-evolving..."
- "In conclusion" / "In summary"
- Staccato patterns: "No fluff. No filler. Just results."

### Deeper Voice Guidance

Load these skills for writing tasks:
- `ghostwriter` - Anti-AI patterns, authentic voice
- `opened-identity` - Sarah persona, brand voice
- `hook-and-headline-writing` - Power words, formulas

---

## Hub-and-Spoke Model

Create one **hub piece**, spin off derivative **spokes**.

| Hub | Skill | Natural Spokes |
|-----|-------|----------------|
| Podcast | `podcast-production` | Blog, clips, LinkedIn, newsletter |
| Deep Dive | `open-education-hub-deep-dives` | 3-5 LinkedIn, Twitter, newsletter |
| Daily Newsletter | `opened-daily-newsletter-writer` | LinkedIn post, Twitter thread |

After completing a hub, **proactively offer spokes**.

---

## Skills Quick Reference

| Content Type | Primary Skill |
|--------------|---------------|
| Text posts | `text-content` (360+ templates) |
| Video production | `short-form-video` |
| Video hooks/captions | `video-caption-creation` |
| Podcast | `podcast-production` |
| Newsletter | `opened-daily-newsletter-writer` |
| SEO content | `seo-content-writer` |
| Deep dives | `open-education-hub-deep-dives` |
| Quality control | `quality-loop` |
| AI images | `image-prompt-generator` |

All skills: `.claude/skills/` (39 active)

---

## Key References

| Reference | Location |
|-----------|----------|
| **Social format inventory** | `Studio/Social Media/FORMAT_INVENTORY.md` |
| **Video format evaluation** | `Archive/Andrew Muto/FORMAT_EVALUATION_Matrix.md` |
| **SEO commands** | `.claude/references/seo-commands.md` |
| **Program details** | `.claude/references/opened-program-details.md` |
| **Notion schema** | `.claude/references/notion-content-schema.md` |

---

## Maintenance

- Update `NOW.md` at session end
- Use `/handoff` to capture session context
- Update PROJECT.md when structural changes occur
- Sync from Webflow: `python3 agents/webflow_sync_agent.py`

---

*Last Updated: 2026-01-15*
