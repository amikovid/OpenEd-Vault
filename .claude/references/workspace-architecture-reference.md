# Workspace Architecture Reference

**Context:** This document captures the documentation and task management architecture for a multi-project workspace managed with Claude Code. Created from an audit session on 2026-01-27.

---

## Documentation Tiers

The workspace uses a tiered documentation system based on scope and complexity.

### Tier 1: CLAUDE.md + NOW.md (Workspaces)

**Use for:** Large scopes you context-switch into as a "workspace" - typically with their own codebase, multiple sub-projects, or ongoing state that changes session-to-session.

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Static context - architecture, key files, workflows, rules | When structure changes |
| `NOW.md` | Living state - current priorities, blockers, session log | Every session |

**Examples:**
- Root level (entire workspace router)
- OpenEd Vault (content production system)
- Curriculove (full app with its own stack)
- Doodle Reader, Skill Stack, etc. (standalone apps/products)

**Criteria - gets CLAUDE.md + NOW.md if:**
- You context-switch into it as a distinct workspace
- Has its own codebase or app
- Multiple developers/agents work in it
- Needs session-to-session state tracking
- Has sub-projects that need coordination

### Tier 2: PROJECT.md Only (Discrete Projects)

**Use for:** Smaller, focused projects where static context is enough. Typically content work, planning documents, or single-focus deliverables.

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `PROJECT.md` | Project context, goals, key files, status | As needed |

**Examples:**
- SEO Content Production sub-projects (Grade Guides, State Pages, etc.)
- Meta Ads campaigns
- Eddie Awards planning
- Newsletter workflows (OpenEd Daily, Weekly)
- Podcast production workflows

**Criteria - PROJECT.md only if:**
- It's a discrete deliverable with clear end state
- Single-focus work (not a "workspace")
- Static context is sufficient
- You don't need to track session-to-session state

### Tier 3: No Documentation (Simple Folders)

**Use for:** Date-stamped outputs, archives, asset folders, or folders that are children of documented projects.

**Examples:**
- `OpenEd Daily Studio/2026-01-27 - Episode Name/`
- `_archive/` folders
- `public/images/` asset folders

---

## Current Workspace Structure

```
New Root Docs/
│
├── CLAUDE.md ──────────── Workspace router (Tier 1)
├── NOW.md ─────────────── Personal current state
├── USER.md, SOUL.md ───── Identity context (Clawdbot)
├── HEARTBEAT.md ───────── Clawdbot
├── IDENTITY.md ────────── Clawdbot
│
├── OpenEd Vault/ ──────── CLAUDE.md + NOW.md (Tier 1)
│   ├── Studio/
│   │   ├── OpenEd Daily Studio/ ──── PROJECT.md (workflow)
│   │   ├── Podcast Studio/ ───────── PROJECT.md (workflow)
│   │   ├── SEO Content Production/ ─ PROJECT.md + sub-PROJECT.mds
│   │   ├── Social Media/ ─────────── PROJECT.md
│   │   ├── Meta Ads/ ─────────────── PROJECT.md
│   │   └── ...
│   │
│   └── Projects/
│       ├── Lead Magnet Project/ ──── PROJECT.md
│       │   └── curriculove/ ──────── CLAUDE.md + NOW.md (Tier 1)
│       ├── Eddie Awards/ ─────────── PROJECT.md
│       ├── Retargeting Strategy/ ─── PROJECT.md
│       └── ...
│
├── Creative Intelligence Agency/ ── (needs top-level CLAUDE.md)
│   ├── doodle-reader/ ────────────── CLAUDE.md + NOW.md
│   ├── skill-stack-studio/ ───────── CLAUDE.md
│   ├── wiki-projects/ ────────────── CLAUDE.md
│   └── clients/
│       ├── Naval/ ────────────────── CLAUDE.md
│       └── Pause/ ────────────────── CLAUDE.md
│
└── Personal/ ─────────────────────── (needs top-level CLAUDE.md)
    ├── Benedict Challenge/ ────────── CLAUDE.md + NOW.md
    ├── JFK50/ ─────────────────────── CLAUDE.md
    ├── California CLM/ ────────────── CLAUDE.md
    └── California Revival/ ────────── CLAUDE.md
```

---

## Task & Backlog Architecture

### The Problem with Centralized Backlogs

A single cross-project `backlog.md` conflates different concerns:
- Your week (what you're actually doing)
- Project feature lists (contextual to codebases)
- Someday/maybe items
- Active vs paused project tracking

### The Solution: Distributed Backlogs

**Layer 1: Your Week (Execution)**
- Lives in Apple Reminders (or similar external tool)
- Gets priority tags (1/3/9)
- Is about *your* attention and calendar
- Not stored in the vault

**Layer 2: Active Project Tracking (Root NOW.md)**
- Root `NOW.md` tracks *which projects are active*
- Lists current focus areas, not individual tasks
- Updated weekly during planning

```markdown
# NOW.md (Root)

## Active Projects

| Project | Status | This Week |
|---------|--------|-----------|
| Benedict Challenge | 🔥 Active | Chapter 1 revision |
| Curriculove | Active | Internal launch prep |
| OpenEd | Maintenance | Newsletter + SEO |
| Doodle Reader | Active | PageSnap deploy |

## Paused
- JFK50 (after Benedict ships)
- California Revival
```

**Layer 3: Project Feature Backlogs (Per-Project NOW.md)**
- Each project's `NOW.md` has a "What's Next" section
- Features, bugs, improvements live *in context*
- Claude sees relevant backlog when working in that project

```markdown
# NOW.md (Curriculove)

## What's Next

### Before Internal Launch
- [ ] Get production Clerk keys
- [ ] OpenEd badge icon for partner curricula
- [ ] Internal Slack announcement

### Phase 2: Enhanced Discovery
- [ ] Reality Check questions
- [ ] Neurodivergence screening
- [ ] Side-by-side comparison
```

### Why This Works

1. **Context:** When Claude works in curriculove, it sees curriculove's backlog - not your JFK50 tasks
2. **Estimation:** Project backlogs don't need time estimates - Claude might do 5 items in one session
3. **Weekly planning:** You skim active project NOW.mds and pull specific items into Apple Reminders
4. **No duplication:** Tasks live in one place (the project), not copied to a central list

---

## OpenEd Vault Specifics

### Documentation Hierarchy

```
OpenEd Vault/
├── CLAUDE.md ─────── Master context (writing rules, skills, workflows)
├── NOW.md ────────── Active projects, QBR items, blocked items
│
├── Studio/ ───────── Ongoing production workflows
│   └── [workflow]/PROJECT.md
│
└── Projects/ ─────── Discrete projects with end states
    └── [project]/PROJECT.md or CLAUDE.md+NOW.md
```

### What Goes Where

| Content Type | Location | Doc Type |
|--------------|----------|----------|
| Newsletter production | `Studio/OpenEd Daily Studio/` | PROJECT.md |
| Podcast production | `Studio/Podcast Studio/` | PROJECT.md |
| SEO content | `Studio/SEO Content Production/` | PROJECT.md + subs |
| Social media | `Studio/Social Media/` | PROJECT.md |
| Meta ads | `Studio/Meta Ads/` | PROJECT.md |
| Curriculove app | `Projects/Lead Magnet Project/curriculove/` | CLAUDE.md + NOW.md |
| Eddie Awards | `Projects/Eddie Awards/` | PROJECT.md |
| Retargeting | `Projects/Retargeting Strategy/` | PROJECT.md |

### Workflow vs Project Distinction

**Workflows** (Studio/):
- Ongoing, no end state
- Cadence-based (daily, weekly)
- Examples: Newsletter, Podcast, Social posting

**Projects** (Projects/):
- Discrete deliverables
- Have completion criteria
- Examples: Curriculove launch, Eddie Awards, Retargeting campaign

### Skills Integration

OpenEd has 45+ skills in `.claude/skills/`. Key routing:

| Content Type | Skill |
|--------------|-------|
| Daily newsletter | `opened-daily-newsletter-writer` |
| Weekly newsletter | `opened-weekly-newsletter-writer` |
| Social posts | `text-content` (360+ templates) |
| Newsletter → Social | `newsletter-to-social` |
| Podcast | `podcast-production` |
| Deep dives | `open-education-hub-deep-dives` |
| Quality control | `quality-loop` |

---

## Session Protocol

### Starting a Session

1. Read the relevant CLAUDE.md (static context)
2. Read NOW.md (current state)
3. Check what's blocked, what's next
4. Work on priorities

### Ending a Session

1. Update NOW.md with:
   - What was completed
   - What's blocked
   - What's next
   - Session log entry with date
2. Use `/handoff` for formal context capture if needed

### NOW.md Session Log Format

```markdown
## Session Log

### 2026-01-27

**Completed:**
- Item 1
- Item 2

**Left off:** Brief note on state

**Next session:** What to pick up
```

---

## Maintenance Tasks

### Identified Gaps (from 2026-01-27 audit)

| Task | Status |
|------|--------|
| Create `curriculove/CLAUDE.md` | ✅ Done |
| Delete orphaned `OpenEd Vault/node_modules` (ralphy) | ✅ Done |
| Create `Creative Intelligence Agency/CLAUDE.md` | TODO |
| Create `Personal/CLAUDE.md` | TODO |
| Update root `CLAUDE.md` with missing folders | TODO |
| Deprecate root `backlog.md` | TODO (migrate to NOW.md pattern) |

### Periodic Reviews

- **Weekly:** Update root NOW.md with active project status
- **Monthly:** Check PROJECT.md files are current
- **Quarterly:** Audit folder structure, archive stale projects

---

## Quick Reference

### When to create CLAUDE.md + NOW.md
- It's a workspace you context-switch into
- Has its own codebase
- Multiple sub-projects
- Needs session-to-session state

### When to use PROJECT.md only
- Discrete deliverable
- Single focus
- Static context is enough
- Part of a larger documented workspace

### Where tasks live
- **Your week:** Apple Reminders (external)
- **Active projects:** Root NOW.md (list only)
- **Feature backlogs:** Per-project NOW.md

### File naming
- `CLAUDE.md` - Always caps, always this name
- `NOW.md` - Always caps, always this name
- `PROJECT.md` - Always caps, always this name

---

*Created: 2026-01-27*
*Context: Workspace architecture audit and task management redesign*
