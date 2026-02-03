# OpenEd NOW

**Last Updated:** 2026-02-02

---

## OPEN PROBLEM: Newsletter Voice (Pirate Wires + OpenEd)

**Status:** Unsolved. Drafts v1-v5 of "Design Over Delivery" newsletter all fall short.

**The goal:** A subagent should reliably produce newsletter drafts in the modified Pirate Wires voice without needing 5 rounds of human revision.

**What we've tried:**

1. **Front-loaded Pirate Wires examples** in `opened-daily-newsletter-writer/SKILL.md` (4 condensed examples with use-case labels at the very top). Helped - drafts got noticeably closer - but the voice still reads like "someone describing Pirate Wires" rather than writing in it.

2. **Anti-patterns list** (staccato fragments, correlatives, fake questions, hedging). Prevents the worst AI tells but doesn't produce the positive quality we want.

3. **Pattern labels** ("Of course, none of them...", parenthetical asides, strong POV). The LLM recognizes and inserts these but they feel mechanical - like checking boxes rather than internalizing rhythm.

4. **Separate "ai-tells" skill** as a blocking constraint. Good for catching errors in review. Does not help generation.

**What's still wrong:**

- **Rhythm is off.** Pirate Wires sentences vary wildly in length - a 40-word sentence followed by a 4-word sentence. The drafts tend toward uniform medium-length sentences.
- **Asides feel grafted on.** Real Pirate Wires parentheticals are *interruptions* to the writer's own thought. The LLM treats them as decorations added after the fact.
- **Too clean.** The originals have a loose, almost reckless quality - digressions, admissions, self-corrections ("but let's remember," "sorry haters"). The drafts are too structured, too on-message.
- **Missing the "I just noticed this" energy.** Pirate Wires reads like someone thinking in real time. The drafts read like someone who already thought it through and is presenting conclusions.

**Hypotheses for next session:**

1. **More examples, fewer instructions.** The skill currently has 4 Pirate Wires examples + ~20 lines of pattern rules. Ratio should probably be 10:1 examples to rules. The LLM learns voice from examples, not from descriptions of voice.

2. **Full paragraphs, not excerpts.** The current examples are single paragraphs. Maybe we need 2-3 *complete segments* (THOUGHT/TREND/TOOL length) written in the target voice so the model sees the full arc, not just isolated sentences.

3. **Write-then-rewrite pipeline.** Instead of one-shot generation, try: (a) draft in plain voice, (b) run a dedicated "voice transform" pass using the examples as few-shot. The `ghostwriter` and `human-writing` skills exist but aren't chained into the newsletter workflow.

4. **Temperature / sampling.** The "reckless" quality may require a looser generation pass. Consider: first draft at higher temperature, then tighten in editing pass.

5. **Charlie's actual newsletters as examples.** We have an archive at `daily-newsletter-workflow/examples/`. Pull 3-5 of the best and put them in the skill as the primary reference, not Pirate Wires excerpts (which are a different audience and register).

**Key discovery:** The "Homeschool Data Gap" draft (same date folder) is *far* closer to the target voice than any of the "Design Over Delivery" attempts. Compare the two directly. The Data Gap draft has the real rhythm - "I mean, this isn't obscure research. It's been replicated for decades. So why doesn't the coverage match the data? (Rhetorical question. We all know why.)" That's the voice. The Design Over Delivery drafts kept imitating Pirate Wires instead of writing like Charlie.

**Hypothesis #5 is probably the answer.** Use Charlie's own published newsletters as primary examples, not Pirate Wires. The register is different - Pirate Wires is tech/politics snark, OpenEd Daily is education/parent authority. Same energy, different register.

**Files involved:**
- Skill: `.claude/skills/opened-daily-newsletter-writer/SKILL.md`
- Voice examples: Same file, "Voice Priming" section
- Anti-AI: `.claude/skills/ai-tells/SKILL.md`
- Ghostwriter: `.claude/skills/ghostwriter/SKILL.md`
- Test drafts: `Studio/OpenEd Daily Studio/2026-02-03 - Design Over Delivery/Newsletter_DRAFT_v*.md`
- **Reference draft:** `Studio/OpenEd Daily Studio/2026-02-03 - Homeschool Data Gap/Newsletter_DRAFT.md` (this is the voice target)

**What worked well this session (non-voice):**
- Playground HTML selector for social post triage - keep this pattern
- Newsletter-to-social pipeline ran smoothly end-to-end
- HubSpot email draft skill works after BATCH_EMAIL fix
- Comic generation (Ed the Horse) is a good recurring format

---

## RSS Curation Dashboard - NEW

**Status:** Working. Full triage-to-staging pipeline operational.

**Start:** `cd Projects/RSS-Curation && python3 serve_dashboard.py` → http://localhost:8000

**What we built this session:**
- Local Python server with warm sand/Notion theme dashboard
- Star/Used/Skip buttons that persist to `tracking.json`
- Reject-with-reason modal (feeds back into scoring prompt improvement)
- Clear Done button (removes processed items, keeps reject reasons)
- Staging folder: `Projects/RSS-Curation/staging/week-YYYY-MM-DD/`

**Files:**
- Dashboard: `Projects/RSS-Curation/serve_dashboard.py`
- Data: `Projects/RSS-Curation/tracking.json`
- Feeds: `.claude/skills/rss-curation/feeds.json` (47 feeds)
- Handoff: `.claude/skills/rss-curation/HANDOFF.md`
- Staging: `Projects/RSS-Curation/staging/week-2026-02-03/`

**Workflow:** Fetch feeds → Review in dashboard → Star keepers → Save → Claude reads tracking.json → Fetch articles to staging → Route to newsletter/social

**Playground preferences:** `.claude/references/playground-preferences.md` - warm sand theme + local server pattern (not dark theme, not copy/paste prompts). Apply to all future playgrounds.

**Pending:**
- [ ] Add playground preferences note to CLAUDE.md
- [ ] Automate fetching with launchd (daily 7am)
- [ ] After 5+ reject reasons, update scoring-prompt.md
- [ ] LinkedIn post for Michael Horn (drafted, not posted)

---

## QBR Action Items (2026-01-26)

**From Q2 QBR meeting - do not let slip:**

| Action | Owner | When | Status |
| --- | --- | --- | --- |
| Show Melissa Search Console integration | Charlie | Tomorrow (add to agenda) | ⏳ |
| Talk to Melissa about daily cadence | Charlie | Tomorrow | ⏳ |
| Set up Monday morning SEO report to Slack | Charlie | This week | ⏳ |
| Request Databox access from Alex | Charlie | This week | ⏳ |
| Align with Ela on Chavilah task allocation | Charlie + Ela | This week | ⏳ |
| Savvy Learning article → coordinate with Ela | Charlie | Before publish | ⏳ |

**Daily cadence decision pending:** Currently 3-4/week. Trade-off: More bandwidth vs. more nearbound at-bats. Discuss with Melissa tomorrow.

**YouTube ads research:** Complete research saved to `Studio/Analytics & Attribution/youtube-vs-meta-ads-research.md`. Recommendation: Test $1,500-2,000 over 8 weeks for fall enrollment.

---

## Guest Contributor Pipeline - ACTIVE

**Architecture:** Notion database + vault templates

- **Notion:** [Guest Contributor Pipeline](https://www.notion.so/2f4afe52ef5981bc8d7accc5e00e1a17) - tracking, source material, article angles

- **Vault:** `Studio/SEO Content Production/Guest Contributors/` - PROJECT.md, outreach templates, examples

### Wave 1 - Ready to Send

| Contact | Company | Topic | Status |
| --- | --- | --- | --- |
| Justin Skycak | Math Academy | Math acceleration | HOT LEAD - praised our AI tutoring article |
| Mason Pashia | Getting Smart | Marketplace data | Active convo Dec 2025, SEND EMAIL |
| Michael Vilardo | Subject.com | Netflix of high school | TED transcript + pitch ready, via Hollie |
| Janssen Bradshaw | Everyday Reading | Literacy/reading | AGREED - needs SEO topic |
| Matt Beaudreau | Apogee | Microschooling | Full Apogee blueprint in Notion |
| Savvy Learning founder | Savvy Learning | TBD | NEW - coordinate with Ela on partnership angle |

### Wave 2 - Warm Leads

| Contact | Company | Topic | Notes |
| --- | --- | --- | --- |
| Robin Smith | Surge Academy | Coding education | Highly engaged (5 replies) |
| Kathleen Ouellette | VictoryXR | VR education | Follow up needed |
| Jon England | Libertas | Microschool policy | Pitch drafted |
| Peter Gray | Self-Directed Ed |  | Podcast done |
| Michael Horn | Disruption |  | Gave book blurb |

**Full content in Notion:** Transcripts, source material, pitch emails, article angles for all Wave 1-2 contributors.

---

## Content Engine Refactor - ARCHIVED

**Archived to:** `Projects/_archive/_content-engine-refactor-archived-2026-01-29/`

All phases complete. Valuable parts moved:
- Sub-agent prompts → `.claude/skills/content-repurposer/references/sub-agents/`
- Architecture map → `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md`

### What Was Done

**New Skills Created:**

- `newsletter-to-social` - Router for hub-to-spoke workflow

- `archive-suggest` - Daily suggestions from content archive

- `slack-social-distribution` - Post to #market-daily as threads

- `newsletter-subject-lines` - Dedicated subject line skill (split from hook-writing)

- `article-titles` - SEO-focused headline skill (split from hook-writing)

- `work-summary` - Translate git commits to Slack-friendly updates

**Skills Refactored (8,400 words removed):**

| Skill | Reduction |
| --- | --- |
| ghostwriter | 64% |
| meta-ads-creative | 63% |
| cold-open-creator | 61% |
| hook-and-headline-writing | 59% (then split) |
| opened-daily-newsletter-writer | 37% |
| podcast-production | 29% |

**Architecture Documented:**

- `SKILL_ARCHITECTURE_MAP.md` - Visual map of entire content engine

- "Examples Over Instructions" philosophy added to skill-creator

- Fixed 7 broken skill references

**Infrastructure:**

- Work summaries folder: `.claude/work-summaries/`

- Nearbound profiles: 8 updated with social handles

### Next Session Approach

**Test skills through actual workflows** rather than isolated audits:

- Run a newsletter → social spoke workflow

- Run a podcast clip extraction

- Note friction points in real use

---

## SEO Comparison Articles - ACTIVE

**New initiative (2026-01-29):** Pedagogy comparison SEO strategy.

**Master keyword list:** `Studio/SEO Content Production/Open Education Hub/Deep Dive Studio/PEDAGOGY_COMPARISON_KEYWORDS.md`

| Article | Volume | Status | Notes |
| --- | --- | --- | --- |
| Waldorf vs Montessori | 2,900/mo | ✅ Ready to publish | Passed 5-judge quality loop |
| Montessori vs Reggio Emilia | 1,900/mo | 📋 Brief created | Next priority |
| Khan Academy vs IXL | 590/mo | 📋 Queued | Ed-tech comparison |
| Unschooling vs Homeschooling | 320/mo | 📋 Queued | Strong OpenEd angle |

**Production cadence:** 2 articles/week using established template.

---

## Active Projects (Studio/)

| Project | Location | Status | Priority |
| --- | --- | --- | --- |
| Lead Magnet | Lead Magnet Project/PROJECT.md | Active dev (curriculove) | HIGH |
| Meta Ads | Meta Ads/PROJECT.md | 100 concepts ready | HIGH |
| SEO Content | SEO Content Production/PROJECT.md | Comparison series active | HIGH |
| Eddie Awards | Eddie Awards/PROJECT.md | Website planning | MEDIUM |
| KPI Discussions | KPI Discussions/PROJECT.md | Q1 bonus planning | MEDIUM |
| Social Media | Social Media/FORMAT_INVENTORY.md | Format inventory done | LOW |
| Project Dandelion | Project-Dandelion/PROJECT.md | Active | HIGH |
| ↳ Retargeting | Project-Dandelion/retargeting-strategy/ | Pillar 1 Feb 16 | HIGH |

### Ongoing Workflows

| Workflow | Location | Cadence |
| --- | --- | --- |
| OpenEd Daily | OpenEd Daily/ | Mon-Thu |
| Podcasts | Open Ed Podcasts/ | Weekly |
| Open Education Hub | Open Education Hub/ | As needed |

---

## Blocked Items

- **GSC Access** - Need ops to add service account for SEO quick wins

  - Account: `opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com`

---

## Key Dates (Q3)

| Date | Event | Impact |
| --- | --- | --- |
| Feb 10 | Enrollment tasks open | Interest → Application conversion focus |
| Feb 16 | Retargeting Pillar 1 launch | 4-6 ad variations needed |
| Q3 | 4 new states launching | State pages become critical path |
| Fall 2026 | Enrollment cycle | YouTube ads test window |

---

---

## API Access

| Service | Status | Notes |
| --- | --- | --- |
| Slack | ✅ | xoxc/xoxd tokens |
| Notion | ✅ | ntn_* token |
| DataForSEO | ✅ | Keyword research |
| GSC | ⚠️ | Service account pending |
| GA4 | ✅ | Analytics access |
| GetLate | ✅ | 8 platforms connected |
| Gemini | ✅ | gemini-3-flash-preview |

---

*Update this file at session end. For project context, see PROJECT.md in each Studio folder.*