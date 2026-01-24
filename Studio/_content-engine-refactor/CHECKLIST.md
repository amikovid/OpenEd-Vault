# Content Engine Refactor - Implementation Checklist

## Phase 0: Archive Old Skills (Safety Step)
- [x] Create folder: `OpenEd Vault/.claude/skills/_archived-pre-refactor/`
- [x] Copy skills being refactored:
  - [x] text-content/
  - [x] x-posting/
  - [x] opened-daily-newsletter-writer/
  - [x] quality-loop/
  - [x] podcast-production/
- [x] Rename archived SKILL.md files to SKILL.archived.md
- [x] Create archive README

## Phase 1: Framework Fitting Infrastructure
- [x] Create TEMPLATE_INDEX.md (lightweight, ~200 tokens)
- [x] Create sub-agent prompt templates:
  - [x] linkedin-agent.md
  - [x] x-agent.md
  - [x] instagram-agent.md
  - [x] facebook-agent.md
- [ ] Test sub-agent with sample snippet
- [ ] Measure token reduction vs current approach
- [ ] Update text-content/SKILL.md to reference sub-agent pattern

## Phase 2: Quality Loop Universalization
- [ ] Read current quality-loop skill
- [ ] Document trigger points for each content type:
  - [ ] Newsletter (after draft, before send)
  - [ ] LinkedIn post (after draft, before schedule)
  - [ ] X post (after draft, before schedule)
  - [ ] Instagram (after draft + visual)
  - [ ] Deep Dive (before Webflow publish)
  - [ ] Podcast blog (before publish)
- [ ] Update quality-loop/skill.md with 5-judge detail
- [ ] Add context loading requirements to skills
- [ ] Test quality loop on sample newsletter
- [ ] Test quality loop on sample social post

## Phase 3: Instagram Coverage
- [x] Create instagram-agent.md prompt
- [x] Add Instagram to TEMPLATE_INDEX.md
- [ ] Document carousel workflow
- [ ] Document quote card workflow (with image-prompt-generator)
- [ ] Test with sample snippet

## Phase 4: Archive Repurposing Agent
- [ ] Design archive scanning logic
- [ ] Identify sources to scan:
  - [ ] Master_Content_Index.md
  - [ ] Podcast transcripts
  - [ ] Content/Master Content Database/
- [ ] Create suggestion format for Slack
- [ ] Test with 3 archive items
- [ ] Document daily run process

## Phase 5: Nearbound Quick Index
- [ ] Extract names from podcast episodes
- [ ] Extract names from newsletter mentions
- [ ] Create person profile template
- [ ] Create profiles for top 50 people
- [ ] Consolidate social handles

## Phase 6: SEO Report Refocus
- [ ] Create new report template
- [ ] Focus on:
  - [ ] Traffic summary
  - [ ] Revision candidates (positions 11-20)
  - [ ] Notable changes
  - [ ] Quick wins
- [ ] Test report generation
- [ ] Document weekly cadence

## Phase 7: Curation Pipeline
- [ ] Create separate PLAN.md in curation/
- [ ] Adapt RSS parser
- [ ] Test Slack integration
- [ ] Create /curate-to-content skill

## Phase 8: CLAUDE.md Restructure
- [ ] Add framework fitting section
- [ ] Add hub types table
- [ ] Add quality loop triggers
- [ ] Add Nearbound playbook
- [ ] Review and test routing

---

## Progress Log

### 2026-01-23
- Phase 0 complete: Archived 5 skills to `_archived-pre-refactor/`
- Phase 1 complete: Created TEMPLATE_INDEX.md and 4 sub-agent prompts
- Phase 2 complete: Updated quality-loop with universal triggers and Lite mode
- Phase 3 complete: Created Instagram workflows doc
- Phase 4 complete: Created archive-suggest skill
- Phase 5 complete: Created Nearbound templates and extraction queries
- Phase 6 complete: Created SEO report template
- Phase 7 complete: Created curation pipeline plan
- Phase 8 complete: Updated OpenEd CLAUDE.md with framework fitting, quality triggers, Nearbound

**All phases complete for initial implementation.**

### Next Steps (Ongoing)
- Test sub-agent pattern with real newsletter
- Build Nearbound profiles for top 50 people
- Set up daily archive-suggest run
- Implement curation pipeline scripts

---

## Phase 9: Social Media Funnel Optimization

Optimize all funnels from social media channels to conversion. Research and implement best practices for each platform.

### Platform Funnel Audit
- [ ] **LinkedIn**
  - [ ] Research best practices for profile → newsletter signup flow
  - [ ] Optimize CTA placement in posts
  - [ ] Review link-in-bio vs comment strategy
  - [ ] Document what's working for competitors

- [ ] **X/Twitter**
  - [ ] Research thread-to-newsletter conversion tactics
  - [ ] Optimize pinned tweet for signup
  - [ ] Review link placement (bio vs replies)
  - [ ] Analyze top performing CTAs

- [ ] **Instagram**
  - [ ] Research Stories → link sticker best practices
  - [ ] Optimize Linktree/bio link setup
  - [ ] Review carousel → action flow
  - [ ] Document Reels → profile → signup path

- [ ] **Facebook**
  - [ ] Research group → newsletter funnel
  - [ ] Optimize page CTA button
  - [ ] Review post → landing page flow

- [ ] **YouTube**
  - [ ] Research description link best practices
  - [ ] Optimize end screen CTAs
  - [ ] Review pinned comment strategy
  - [ ] Document shorts → subscribe → newsletter path

### Deliverables
- [ ] Platform-specific funnel playbooks
- [ ] Updated CTAs for each platform
- [ ] Tracking/attribution setup for each channel
- [ ] A/B test plan for top 2 platforms

---

## Phase 10: Skill Architecture Map & Reference Cleanup

**Status:** ✅ Complete (2026-01-23)

### Completed
- [x] Created `SKILL_ARCHITECTURE_MAP.md` - comprehensive visual architecture of content engine
  - Master flow: Source → Context Loading → Snippet Extraction → Framework Fitting → Quality Gate → Output
  - Hub-specific chains: Podcast (4 checkpoints), Newsletter (TTT → Quality → Spokes), Deep Dive
  - Video content skill chain with Triple Word Score
  - Skill dependency matrix
  - Platform-specific quick reference
  - Identified gaps for future work

- [x] Fixed broken skill references:
  - `youtube-clip-extractor`: `social-content-creation` → `text-content`
  - `youtube-clip-extractor`: Removed `hook-and-headline-writing` (archived)
  - `video-caption-creation`: `social-content-creation` → `text-content` (3 places)
  - `video-caption-creation`: `daily-newsletter-workflow` → `opened-daily-newsletter-writer`
  - `youtube-downloader`: Fixed frontmatter name (`youtube-transcript` → `youtube-downloader`)

- [x] Added "Examples Over Instructions" philosophy to `skill-creator`
  - Core principle: One output example worth a thousand words of instructions
  - Skills should be example-heavy, instruction-light

### Remaining (Low Priority)
- [ ] Test YouTube Clip Extractor with Phil Donahue/John Holt video
- [ ] Add post-clip import cleanup handling to youtube-clip-extractor
- [ ] youtube-title-creator has 6 broken references (needs audit)
