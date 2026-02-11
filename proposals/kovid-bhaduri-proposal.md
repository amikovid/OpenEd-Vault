# Kovid Bhaduri - 2-Week Sprint Proposal

## Domain

Systems architecture and analytics infrastructure - specifically closing the feedback loop between published content and editorial decisions, and unblocking execution bottlenecks across the vault.

## What I Built Today

### Primary: Content Performance Scoring System

The vault has analytics modules scattered across 6 services (GA4, GSC, HubSpot, YouTube, Meta, DataForSEO) that never connect back to the point where decisions get made. Content goes out, but learning never comes back in. Charlie approves content in Notion and Slack without knowing what similar content did last time.

I built a system that closes that loop:

**Scoring engine** (`agents/content_performance_agent.py`) - Imports the existing seomachine modules, calculates a 0-100 composite score for every published piece using platform-specific weighting (LinkedIn weights comments, X weights reposts, Instagram weights saves), and writes scores back to Notion. Generates narrative insight digests - not just "top 5 posts" but "curriculum reviews outperform education news by 2x, and they perform best on LinkedIn, not X."

**One-command setup** (`agents/setup_performance_scoring.py`) - Charlie runs one script. It checks his API keys, automatically creates 12 performance tracking properties on the Notion database via API, runs initial scoring, and offers to set up daily cron. Five minutes from zero to working.

**Approval context injection** (`get_approval_context()`) - Any skill can import this function. When Charlie is reviewing a draft, it returns: "Posts about curriculum reviews average 72 on LinkedIn, 35 on X. Best performer in this theme scored 89. Route this to LinkedIn." This is the piece that makes historical data show up at the exact moment a decision is being made.

**Skill file and reference docs** - Full system design in `.claude/skills/content-performance-scoring/SKILL.md`, quick reference card for Charlie, updated Notion schema doc, updated agents README.

### Secondary: Execution Bottleneck Analysis

Audited the vault for automation gaps. Five findings:

1. **SEO publish pipeline** - 92 articles planned, 0 published. But 3+ comparison articles are draft-complete, quality-checked, and thumbnailed. The batch publish script exists but hasn't been run. This isn't a technical problem.
2. **Archive repurposing** - 405 published pieces with no systematic resurfacing. The `archive-suggest` skill is a 172-line template, not a working system.
3. **Quote sourcing** - Every SEO article requires real teacher/parent quotes. Currently writers manually search Slack. No quote database exists.
4. **Slack MCP** - Documented but not operational. Blocks automation of the social approval workflow.
5. **Cron automation** - Zero scripts run on schedule. RSS curation, scoring, reporting - all manual execution.

Documented with concrete fixes, effort estimates, and a prioritized sprint order.

## What I'd Deliver in 2 Weeks

### Week 1: Make the scoring system production-ready + publish existing SEO content

- Test the scoring agent against live data, fix edge cases
- Wire `get_approval_context()` into `quality-loop` as a 6th judge (Performance Advisor)
- Wire scoring data into `archive-suggest` so it prioritizes resurfacing high scorers
- Wire platform routing into `newsletter-to-social` so derivatives go to the platform where that theme scores highest
- Publish the 3 ready comparison articles (Khan vs IXL, Saxon vs Math-U-See, IXL vs Exact Path) - immediate SEO wins with zero new content creation
- Set up cron jobs for daily scoring + weekly digest

### Week 2: Build the archive repurposing system + quote database

- Rebuild `archive-suggest` from its 172-line skeleton into a proper system with performance-aware scoring, Notion integration, and automated daily suggestions
- Build a quote extraction system that scans 66 podcast transcripts and structures quotes by speaker, topic, and source - so article writers query a database instead of searching Slack
- Get the RSS curation cron job running (the script exists, launchd setup doesn't)
- Document all changes, update vault guide

### Measurable outcomes after 2 weeks:
- Every published piece has a performance score visible in Notion
- Charlie gets a weekly insights digest with platform routing recommendations
- 3+ SEO articles published (from existing ready drafts)
- Archive resurfacing generates 3-5 scored post suggestions daily
- Quote database covers 66 podcast episodes

## Why This Domain

The vault's content production engine is well-built - 60 skills, hub-and-spoke model, quality gates. The gap isn't creation. It's the feedback loop (content goes out but performance data never comes back) and execution automation (scripts exist but nothing runs). These are systems problems, not content problems, and they compound - every day without performance feedback is a day of editorial decisions made without data.

I gravitated here because I think in terms of systems and leverage. My instinct when looking at the vault wasn't "which newsletter should I draft" - it was "why does data flow in one direction?" and "why are finished articles sitting unpublished?" Those are the questions that lead to structural improvements rather than one-off deliverables.

## What I Learned Today

- The vault is architecturally sophisticated - the skill system, hub-and-spoke model, and quality gates are genuinely well-designed. The bottlenecks are at the seams, not in the components.
- Charlie's time is the scarcest resource. Every manual step in a workflow is a cost, every automated step is leverage.
- The 92-to-0 SEO execution gap tells me the system is better at planning than shipping. The scoring system helps here because it creates urgency - when you can see "this keyword has 2,900 monthly searches and your finished article is sitting in drafts," inaction becomes visible.
- The existing seomachine modules (GA4, GSC, HubSpot, Meta, YouTube) are solid infrastructure. The problem was never "we can't get the data" - it was "the data doesn't reach the decision."
- "I did" over "we should" is the right culture for this kind of work. I'd rather ship an imperfect scoring agent today than pitch a perfect analytics strategy next week.

## Rate

Open to discussing based on scope and expectations. Happy to align on this after you've seen the work.

## Files Created/Modified

| File | Type | Purpose |
|---|---|---|
| `agents/content_performance_agent.py` | New | Scoring engine + digest + approval context |
| `agents/setup_performance_scoring.py` | New | One-command setup wizard |
| `.claude/skills/content-performance-scoring/SKILL.md` | New | Full system design + algorithm |
| `.claude/references/content-performance-scoring-quickref.md` | New | Charlie's one-page reference |
| `.claude/references/execution-bottleneck-analysis.md` | New | 5 bottlenecks with fixes |
| `.claude/references/notion-content-schema.md` | Modified | Added 12 performance properties |
| `agents/README.md` | Modified | Added agent documentation |
