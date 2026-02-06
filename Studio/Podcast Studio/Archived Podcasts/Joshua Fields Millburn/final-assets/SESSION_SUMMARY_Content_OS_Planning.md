# Session Summary: Content OS Planning & Joshua Fields Millburn Case Study

**Date:** 2026-01-29
**Purpose:** Document findings from Content OS architecture planning session, using JFM podcast as concrete test case.

---

## Part 1: Vault Restructuring Completed

### Project Dandelion Consolidation

Retargeting Strategy is now a **subfolder** inside Project Dandelion (not a separate project):

```
Projects/Project-Dandelion/
├── PROJECT.md
├── SPRINT-01.md
├── research/
│   └── meta-ads-performance-analysis-2026-01-28.md
├── playbook/
└── retargeting-strategy/
    ├── PROJECT.md
    ├── Pillar-1-Creative-Proposals.md (improved "evidence over accusation")
    ├── Pillar-1-Creative-Proposals-ORIGINAL.md (archived)
    └── Pillar-1-Handoff-Notes-Ella.md
```

**Key insight from performance analysis:** Lo-fi, native-feeling formats dramatically outperform polished designs. Same copy with "corporate" styling (highlights, underlines) performed 28x worse.

### Content Engine Refactor Archived

Moved to `Projects/_archive/_content-engine-refactor-archived-2026-01-29/`

**Valuable parts preserved:**
- Sub-agent prompts → `.claude/skills/content-repurposer/references/sub-agents/`
- Architecture map → `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md`

**All path references updated across:**
- CLAUDE.md
- NOW.md
- newsletter-to-social skill
- text-content skill
- slack-social-distribution skill
- content-inbox-workflow reference

---

## Part 2: Content OS Architecture Discussion

### The Problem We're Solving

1. **Notion is adding friction** - except maybe for pillar content (SEO articles, podcasts)
2. **Social media should NOT go through Notion** - triage happens in Slack
3. **Too many items / unclear review process** - bottleneck is volume and process clarity
4. **Platform-specific content requires specialized agents** - but no clear protocol for how agents work together

### Proposed Three-Layer Architecture

```
LAYER 1: ORCHESTRATORS (decide what to do)
         │
         ├─ newsletter-orchestrator (newsletter complete → spawn platform agents)
         ├─ podcast-orchestrator (episode published → spawn clip + promo agents)
         └─ article-orchestrator (deep dive ready → spawn distribution agents)

LAYER 2: SPECIALISTS (do the work)
         │
         ├─ linkedin-agent
         ├─ x-agent
         ├─ instagram-agent
         └─ (video-agent, email-agent, etc.)

LAYER 3: REVIEWERS (quality gates)
         │
         └─ Posts to Slack for human triage (not Notion)
```

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **Notion only for pillar content** | SEO articles, podcasts need editorial calendar. Social doesn't. |
| **Social never touches Notion** | Goes straight to Slack triage |
| **Create content bundle together** | Don't create pillar then generate social later. Create everything at once. |
| **Store bundles in Studio folders** | Each episode/article gets a folder with all assets |
| **Slack for triage** | Where everyone already is. No separate system. |

### The Shift in Workflow

**OLD:**
```
Create pillar → Publish → THEN generate social suggestions
```

**NEW:**
```
Create pillar + social together → Store in Studio folder → Slack triage → Publish all
```

### Content Bundle Structure (Target)

```
Studio/Podcast Studio/[Episode Name]/
├── final-assets/
│   ├── blog-post.md
│   ├── social-plan.md
│   └── clips/
│       ├── clip-1-no-shoulds.mp4
│       ├── clip-2-fentanyl.mp4
│       └── ...
├── SOURCE.md (transcript)
├── Checkpoint_1_*.md
├── Checkpoint_2_*.md
└── ...
```

### Alignment Question: Git vs Notion

**Current state:**
- Vault is source of truth
- Vault syncs to GitHub (via regular git, NOT Nomendex)
- Colleagues may still look at Notion

**Options discussed:**
1. Non-technical colleagues learn GitHub (viable)
2. Notion as thin sync layer - auto-populated from vault (scripts exist)
3. Monday morning Slack post: "This week's content: [list]" (simplest)

**Key insight:** If the vault is truth and Slack is triage, Notion becomes a third place to maintain. That's where friction lives.

---

## Part 3: Joshua Fields Millburn Case Study

### Current State

| Asset | Status |
|-------|--------|
| YouTube (full episode) | ✅ Live |
| Spotify | ✅ Live |
| Blog post | ⚠️ Needs update on Webflow |
| 5 video clips | Ready in Descript |
| Social posts | Written, need scheduling |

### Clips Inventory

| # | Clip Name | Duration | Descript Link | Category |
|---|-----------|----------|---------------|----------|
| 1 | "No Shoulds, Only Coulds" | 6:53 | [Link](https://share.descript.com/view/BYq3vKEO7bV) | LONG |
| 2 | "Would You Give Your Kids Fentanyl?" | 0:55 | [Link](https://share.descript.com/view/lpvDkamGlE5) | SHORT |
| 3 | "Joy Cannot Be Acquired" | 0:40 | [Link](https://share.descript.com/view/zN3xng7Py22) | SHORT |
| 4 | "The Entryway Rule" | 0:55 | [Link](https://share.descript.com/view/DIvr4LnLGHJ) | SHORT |
| 5 | "Competition Is a Mental Illness" | 5:48 | [Link](https://share.descript.com/view/palKQrpfOcA) | LONG |

### Handles

| Person/Brand | X/Instagram | LinkedIn |
|--------------|-------------|----------|
| Joshua Fields Millburn | @joshuafieldsmillburn | - |
| The Minimalists | @theminimalists | - |
| Isaac Morehouse | @isaacmorehouse | @isaacmorehouse |
| OpenEd | @OpenEdHQ | OpenEd |

### Files Created/Modified

- `final-assets/blog-post.md` - Polished blog (no story beats, proper intro)
- `final-assets/social-plan.md` - Platform-specific posts with scheduling
- `final-assets/SESSION_SUMMARY_Content_OS_Planning.md` - This file

---

## Part 4: References

### Content OS Architecture

| Document | Location |
|----------|----------|
| Content OS PROJECT.md | `Projects/OpenEd-Content-OS/PROJECT.md` |
| Skill Architecture Map | `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md` |
| Content Staging Pipeline | `Studio/Content Staging Pipeline/PROJECT.md` |
| Content Repurposer Skill | `.claude/skills/content-repurposer/SKILL.md` |
| Sub-agent prompts | `.claude/skills/content-repurposer/references/sub-agents/` |

### Vault Organization

| Document | Location |
|----------|----------|
| Master context | `CLAUDE.md` |
| Current state | `NOW.md` |
| Weekly execution | `EXECUTION.md` |
| Nearbound profiles | `Studio/Nearbound Pipeline/people/` |

### Skills Relevant to Content OS

| Skill | Purpose |
|-------|---------|
| `content-repurposer` | Framework fitting for multi-platform distribution |
| `newsletter-to-social` | Newsletter → social router |
| `text-content` | 360+ social templates |
| `podcast-production` | Full podcast workflow |
| `x-posting` | GetLate API integration |
| `quality-loop` | 5-judge quality gates |

---

## Part 5: Open Questions / Next Steps

### For Content OS

1. **Formalize orchestrator protocol** - How does an orchestrator actually spawn specialists? Need explicit "spawn these agents in parallel" logic.

2. **Define the bundle spec** - What files should every content bundle contain?

3. **GitHub alignment** - Do colleagues access GitHub directly, or do we create a thin Notion sync?

4. **GetLate integration** - The x-posting skill exists. Need to verify it works for batch scheduling.

### For JFM Episode

1. **Blog post** - Update on Webflow (may be manual due to HTML conversion)
2. **Download clips** - From Descript links
3. **Schedule social** - Via GetLate or manual
4. **Isaac coordination** - Which posts does Isaac share directly vs. RT?

---

## Part 6: What We Learned

### Content OS Insights

1. **Opinionated = focus** - Not trying to do everything. Doing few things well.

2. **Platform-specific beats spray-and-pray** - But requires specialized agents.

3. **Create together, not sequentially** - Pillar + social in same workflow.

4. **Slack beats Notion for triage** - Where everyone already is.

5. **Vault is truth** - Everything else is a view of it.

### Process Insights

1. **Work from concrete examples** - Abstract architecture got unwieldy. JFM case study grounded it.

2. **The content is ready** - Creation isn't the bottleneck. Distribution/scheduling is.

3. **Skills exist but orchestration is missing** - Sub-agents exist, but no clear protocol for spawning them.

---

*Created: 2026-01-29*
*For merging with other session context*
