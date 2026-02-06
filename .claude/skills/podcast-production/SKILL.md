---
name: podcast-production
description: Produce podcast episodes from Notion transcript to a single editor handoff document. Three phases with two human decision points.
---

# Podcast Production Skill (v2)

Transform a podcast transcript into a single **EDITOR_HANDOFF.md** - the one document your video editor needs. Three phases, two human checkpoints, converging on one deliverable.

**Previous version:** `SKILL_v1_archive.md` (4-checkpoint system, retired Feb 2026)

---

## The Pipeline

```
PHASE 1: SETUP (automated, no LLM needed for import)
  Step 0:   Import from Notion → SOURCE.md
  Step 0.5: Guest social research → GUEST_SOCIAL_RESEARCH.md
  Step 1:   SEO keyword research → SEO_Keywords.md

PHASE 2: AUDIT + HUMAN REVIEW
  Step 2:   Audit (angles, clips, cold opens, blog format assessment)
            → Checkpoint_1_Audit.md
  ────────── HUMAN CHECKPOINT: Select angle + approve clips ──────────
  Step 3:   Title + thumbnail variations (YouTube title + blog title)
            → Title_Options_By_Angle.md
  ────────── HUMAN CHECKPOINT: Select title + thumbnail ──────────

PHASE 3: HANDOFF ASSEMBLY (converges to one document)
  Step 4:   On-screen hook generation (3-5 per clip)
  Step 5:   Final clip markup (3 short + 2 long, edit-ready)
  Step 6:   Cold open assembly (2-3 options from selected clips)
  Step 7:   YouTube description + chapters
  Step 8:   Blog post direction + social tagging strategy
            → EDITOR_HANDOFF.md (THE deliverable)
```

---

## Folder Structure

```
Studio/Podcast Studio/[Guest-Name]/
└── prep/
    ├── SOURCE.md                    # Raw transcript from Notion
    ├── GUEST_SOCIAL_RESEARCH.md     # Handles, platforms, reshare strategy
    ├── SEO_Keywords.md              # Keyword volumes + blog direction
    ├── Checkpoint_1_Audit.md        # Angles, clips, cold opens
    ├── Title_Options_By_Angle.md    # Framework-fit titles organized by angle
    └── EDITOR_HANDOFF.md            # THE DELIVERABLE (everything the editor needs)
```

---

## Phase 1: Setup

### Step 0: Import from Notion

```bash
python3 /Users/charliedeist/Desktop/New\ Root\ Docs/.claude/scripts/notion_import.py <page_id> --title -o "Studio/Podcast Studio/[Guest-Name]/prep/SOURCE.md"
```

No LLM tokens. Direct Notion API to markdown. Creates the folder structure automatically.

To find page IDs for recorded episodes, query the Podcast Master Calendar Notion database (`d60323d3-8162-4cd0-9e1c-1fea5aad3801`) filtering for `Status = Recorded`.

### Step 0.5: Guest Social Research

Run a web search sub-agent to find:
- All personal + company handles (LinkedIn, X, IG, TikTok, YouTube)
- Which platform is their strongest (by engagement, not follower count)
- What kind of content they typically post/share
- Mutual connections with OpenEd
- Collaboration history (have they shared our content before?)

Output: `GUEST_SOCIAL_RESEARCH.md`

This informs clip selection (which platforms matter?) and social strategy (tagging, reshare potential).

### Step 1: SEO Keyword Research

Use DataForSEO to research 5-7 keywords related to the guest's topic. Focus on:
- Guest name + company (branded volume)
- Core topic terms (e.g., "microschool", "how to start a microschool")
- Related high-intent queries

Output: `SEO_Keywords.md` - consolidated summary, not individual briefs.

This informs title selection and blog post direction. YouTube title and blog title should be DIFFERENT:
- **YouTube title** = CTR optimized (curiosity, emotion, pattern interrupt)
- **Blog title** = SEO optimized (target keyword in title, search intent match)

---

## Phase 2: Audit + Human Review

### Step 2: Audit

Send to an Opus sub-agent with the full SOURCE.md. The audit produces:

1. **Angles** (3-5 distinct marketing angles, each with a 1-sentence pitch)
2. **Short clips** (5-8 candidates, 30-90 sec each)
   - Verbatim quotes with timestamps
   - Category: Counterintuitive / Memorable / Relatable / Practical / Emotional
3. **Long clips** (3-4 candidates, 2-5 min each)
   - Narrative arc summary
   - Opening hook verbatim
4. **Cold open candidates** (2-3 montage arrangements using [SWOOSH] transitions)
5. **Blog format assessment** - Is this a "day-in-the-life" candidate or standard blog?
6. **Timestamp index** - Full chapter-by-chapter breakdown

**CRITICAL RULES:**
- All quotes VERBATIM. Never paraphrase.
- Mine the ENTIRE transcript, not just the first half.
- Bold over safe. Surprising, contrarian moments beat obvious observations.
- Target 5-8 clips in the audit (mine broadly), user will whittle to 5 final.

Output: `Checkpoint_1_Audit.md`

**Sub-agent prompt template:**
```
You are auditing a podcast transcript for content production.

Episode: [Guest Name]
Working directory: [path to prep/]

Read SOURCE.md (the full transcript).

Produce Checkpoint_1_Audit.md with:
- 3-5 angles (1-sentence pitch each)
- 5-8 short clip candidates (30-90 sec, verbatim with timestamps)
- 3-4 long clip candidates (2-5 min, narrative arc + opening hook verbatim)
- 2-3 cold open montage arrangements
- Day-in-the-life assessment (yes/no with reasoning)
- Full timestamp index

Rules: ALL quotes verbatim. Mine the entire transcript. Bold over safe.
```

### HUMAN CHECKPOINT 1

Present the audit summary. User selects:
- **Primary angle** (which direction for the episode)
- **5 clips** (3 short + 2 long) from the candidates
- **Cold open preference** (or direction for assembly)
- **Blog format** (standard or day-in-the-life)

### Step 3: Title + Thumbnail Variations

After angle selection, generate titles using the `youtube-title-creator` skill:
- 5 titles per angle using the 119 Creator Hooks frameworks
- Each title includes: framework reference, psychological principles, thumbnail text suggestion
- Organize by angle so user can see which direction has the strongest title

**VERIFICATION RULE:** Any specific claim in a title (numbers, named concepts, frameworks) must cite the transcript moment that supports it. Never let a framework template inject a claim that isn't in the source.

After user narrows to 3-4 title finalists, produce 3 thumbnail concepts per title:
- Visual description (what the thumbnail image shows)
- On-screen text (2-4 words, complements title - never repeats it)
- Why this pairing works

Output: `Title_Options_By_Angle.md`

### HUMAN CHECKPOINT 2

User selects:
- **YouTube title** (CTR optimized)
- **Blog title** (SEO optimized, different from YouTube)
- **Thumbnail direction**

---

## Phase 3: Handoff Assembly

Everything converges into `EDITOR_HANDOFF.md`. Send to an Opus sub-agent with SOURCE.md + all prep files. The sub-agent builds the complete handoff document.

### EDITOR_HANDOFF.md Structure

```markdown
# EDITOR HANDOFF: [Guest Name], [Company]

## SECTION 1: EPISODE INFO
- Guest, host, duration
- YouTube title (selected)
- Blog title (selected)
- Thumbnail text suggestion

## SECTION 2: COLD OPENS
- 2-3 options, each 25-35 seconds
- Verbatim with ~~strikethrough~~ for cuts, *italics* for smoothing
- [SWOOSH] between unrelated moments
- Source timestamps for each segment

## SECTION 3: SHORT CLIPS (3 total)
For each clip:
- Timestamp range
- On-screen hook options (3-4 per clip, * next to recommended)
- Full verbatim transcript with edit markup
- Caption (universal for FB, TikTok, IG, LinkedIn)
- X variant (shorter, more conversational)

## SECTION 4: LONG CLIPS (2 total)
For each clip:
- Timestamp range
- Narrative arc (setup → tension → payoff)
- On-screen hook options (3 per clip)
- Opening hook verbatim
- Caption + X variant
- Suggested standalone title

## SECTION 5: YOUTUBE DESCRIPTION + CHAPTERS
- Natural description (keyword-enriched, not stuffed)
- Guest bio + links
- Timestamped chapters (keyword-rich, 5-10 words each)

## SECTION 6: SOCIAL QUOTES
- 5 standalone quotes with timestamps
- Use cases (quote cards, newsletter pullquotes, social posts)

## SECTION 7: BLOG POST DIRECTION
- Blog title (SEO optimized)
- Target keyword + search volume
- Standard narrative guide OR day-in-the-life format
- 3-5 section suggestions with supporting transcript moments

## SECTION 8: SOCIAL TAGGING & RESHARE STRATEGY
- Guest handles per platform
- Platform priority (based on guest research)
- Tagging strategy per clip
- Nearbound: what to offer guest to maximize reshare
```

### On-Screen Hook Standards

On-screen text is the #1 visual element. It does the PRIMARY work of stopping a scroll.

**Requirements per clip:**
- 3-4 hook options per clip
- Star (*) next to recommended pick
- No category labels, no rationale - just the options

**Hook categories:**
- **Polarizing** - Takes a side. "Schools trap families?"
- **Counter-Intuitive** - Surprises. "The school choice argument nobody makes"
- **Direct Challenge** - Confronts viewer. "Your kid's teacher hates their job"
- **Curiosity Gap** - Opens a loop. "55% want to quit"

**Complementarity principle:** On-screen text should ADD context that makes the audio land harder, not just label the clip. The gap between what you read and what you hear creates curiosity.

**"First 3 words" test:** The first 3 words someone reads do 80% of the work. Front-load the punch.

### Edit Markup Convention

```
~~strikethrough~~ = cut this (editor removes)
*italics* = minor smoothing edit (change spoken word)
[SWOOSH] = visual transition between unrelated segments
[AMAR] = speaker label
```

---

## Key Principles

1. **Verbatim only.** All quoted transcript exactly as spoken. Cut and rearrange, never paraphrase.
2. **One deliverable.** Everything flows into EDITOR_HANDOFF.md. Don't over-generate intermediate docs.
3. **Mine the whole transcript.** The strongest moment might be at minute 48.
4. **Bold over safe.** Contrarian > obvious. Tension > comfort.
5. **5 clips total.** 3 short (30-90 sec) + 2 long (2-5 min). Quality over quantity.
6. **Same caption everywhere.** One caption per clip for FB/TikTok/IG/LinkedIn. Optional X variant.
7. **Title + thumbnail are a pair.** Design them together. Thumbnail complements, never repeats.
8. **YouTube title != blog title.** YouTube = CTR. Blog = SEO.
9. **On-screen hooks are the #1 priority.** 3-5 variations per clip, not afterthoughts.
10. **Guest research informs everything.** Know their platforms before selecting clips.

---

## Skill Dependencies

| Step | Skills Used |
|------|-------------|
| Step 0 | `notion_import.py` (script, not skill) |
| Step 1 | `seo-research` / DataForSEO |
| Step 3 | `youtube-title-creator` (119 frameworks) |
| Step 4 | `video-caption-creation` (hook categories, Triple Word Score) |
| Step 6 | `cold-open-creator` (optional reference) |
| Step 8 | `podcast-blog-post-creator`, `day-in-the-life` (if applicable) |
| Quality | `quality-loop` (for blog post draft) |

---

## Common Mistakes

- Fabricating claims in titles (e.g., "6 Levels of Teaching" when transcript has no such framework)
- Single on-screen hook per clip instead of 3-5 options
- Generating platform-specific captions (same caption everywhere, X variant only)
- Thumbnail text that repeats the title
- Ignoring guest's social presence until the end
- SEO research after title selection instead of before
- Cold opens before clip selection (cold opens are assembled FROM clips)
- 25+ snippet inventory when 5-8 targeted clips is better

---

## Next Priorities (Skill Improvements Backlog)

- [ ] Build `youtube_autocomplete.py` using DataForSEO for YouTube search suggestions
- [ ] Research exemplar podcast YouTube/IG channels for on-screen hook reference library
- [ ] Improve `video-caption-creation` skill with complementarity principle + real education creator examples
- [ ] Build dedicated title+thumbnail sub-agent with better variation examples from Creator Hooks
- [ ] Add internal linking step (scan Master Content Index for backlinks in blog post + YouTube description)

---

## References

- `references/checkpoint-1-template.md` - Detailed audit template
- `references/checkpoint-2-example.md` - Cold open + clip example (Claire Honeycutt)
- `references/checkpoint-3-example.md` - YouTube strategy example
- `references/checkpoint-4-example.md` - Polished transcript + blog example
- `references/day-in-the-life-format.md` - Day-in-the-life blog template
- `SKILL_v1_archive.md` - Previous 4-checkpoint system

---

*Rewritten Feb 6, 2026 after Amar Kumar session. See `Studio/Podcast Studio/Amar-Kumar/prep/SKILL_IMPROVEMENT_NOTES.md` for detailed rationale.*
