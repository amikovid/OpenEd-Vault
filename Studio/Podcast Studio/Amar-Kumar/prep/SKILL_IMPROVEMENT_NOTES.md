# Podcast Production Skill - Improvement Notes
**Session: Amar Kumar (Feb 6, 2026)**

## What Worked Well
1. **Notion import script** (`notion_import.py`) - Direct API → file, no LLM tokens burned on transcript copying. 60KB in 5 seconds. Should be the standard first step.
2. **Streamlined Checkpoint 1** - Raw audit format (angles + clips + cold opens) instead of formal checkpoint structure. Faster to produce, easier to react to.
3. **Framework-fit titles by angle** - Generating title options per angle lets you see which direction has the strongest title before committing.
4. **Parallel research** - SEO keyword research + YouTube API research running simultaneously while reviewing clips.

## What Needs Fixing

### 1. Title Generator Must Not Fabricate Content
- "Amar Kumar Reveals: The 6 Levels of Teaching" sounded great but "6 levels" was invented by the framework template, not from the transcript.
- **Rule**: Any specific claim in a title (numbers, named concepts, frameworks) must be verified against the source material.
- **Fix**: Add a verification step to the title generator: "For each title, cite the transcript moment that supports the specific claim."

### 2. Cold Open Should Come After Clip Selection, Not Before
- In the 4-checkpoint system, cold open creation was a separate step. But cold opens are assembled FROM the best clips. More natural to select clips first, then arrange snippets from those clips into cold opens.
- **Fix**: Merge cold open creation into the clip selection step.

### 3. Five Clips Total Is Better Than Eight
- Original skill asked for 25-30 snippets in Checkpoint 1. Too many. Charlie wants 3 short + 2 long = 5 total. Quality over quantity.
- **Fix**: Target 5-8 in the audit (mine broadly), then whittle to 5 in the final selection.

### 4. SEO Research Should Precede Title Finalization
- Currently titles are generated without keyword data. Should run DataForSEO/Keywords Everywhere first, then use search volume and related queries to inform title choices.
- **New step**: SEO keyword research → inform title direction → finalize title
- YouTube title and blog post title should be DIFFERENT (YouTube = CTR optimized, blog = SEO optimized)

### 5. YouTube Search Intent API Gap
- No YouTube-specific search volume tool yet. DataForSEO can do YouTube autocomplete. Keywords Everywhere ($10 one-time) adds estimated YouTube search volume.
- **Action**: Install Keywords Everywhere API, build a youtube_keyword_research.py script.

### 6. Social Posts Use Same Caption Across Platforms
- Don't need platform-specific captions for each clip. Same on-screen text and caption for FB, TikTok, IG, LinkedIn, X.
- Maybe slightly different for X (shorter, more conversational).
- **Fix**: Generate ONE caption per clip + optional X variant. Not 5 platform-specific versions.

### 7. Day-in-the-Life Decision Point
- Some episodes are better suited to a day-in-the-life blog format vs. standard blog. This should be a flagged decision in the audit, not assumed.
- **Fix**: Add a "Day-in-the-Life candidate?" assessment to Checkpoint 1 audit.

### 8. Notion Import Should Be Step 0
- Currently the skill starts with "you already have the transcript." The actual first step is importing from Notion.
- **Fix**: Add Step 0: `python3 notion_import.py <page_id> --title -o <output_path>`
- Auto-creates folder structure: `Studio/Podcast Studio/[Guest]/prep/SOURCE.md`

## Proposed Revised Flow

```
Step 0: Import from Notion (notion_import.py - seconds, no LLM)
Step 1: Audit (angles, clips, cold opens, day-in-the-life assessment)
Step 2: SEO keyword research (DataForSEO - automated)
Step 3: Title selection (YouTube title + blog title, informed by SEO)
Step 4: Final clip markup (3 short + 2 long, edit-ready with ~~strikethrough~~)
Step 5: Cold open assembly (from selected clips)
Step 6: Blog post / day-in-the-life draft
Step 7: Social posts (one caption per clip + X variant)
Step 8: YouTube description + chapters
```

### 9. On-Screen Hooks Are the #1 Priority - Currently Treated as Afterthought
**The problem:** In the handoff doc, each clip got ONE on-screen hook, and they're all 2-word labels ("You've lost.", "Kids know.", "No kid is lost."). These are thumbnail text, not video hooks.

**Why this matters:** On-screen text is doing the PRIMARY work of the visual hook. It's the first thing processed before audio registers. A viewer scrolling sees the text and decides in <1 second whether to stop.

**What the video-caption-creation skill already says to do (but we're not doing):**
- Generate 3-5 hook options per clip
- 4 hook categories: Polarizing, Counter-Intuitive, Direct Challenge, Curiosity Gap
- McDonald's test
- Quality check: "Would this make ME stop scrolling?"

**What's missing from the skill:**
- **Complementarity principle**: The on-screen text should ADD context that makes the audio land harder, not just label the clip. It should work like title + thumbnail - together they create a fuller picture.
- **Real examples from high-performing education creators**: The skill has generic examples. We need to study what actually works on education TikTok/Reels/Shorts and build a reference library of proven hooks.
- **The "first 3 words" test**: What are the first 3 words someone reads? Those do 80% of the work.
- **Tension between on-screen text and spoken words**: The best hooks create a gap between what you read and what you hear. Example: On-screen says "Kids know." but what the viewer hears is about teachers being dissatisfied. That gap creates curiosity. But "Kids know." is too vague to create a useful gap.

**Better hook examples for our clips:**
- Clip 1 ("Trapped Families"): Instead of "You've lost." → "Schools trap families?" or "His argument silenced the room" or "School choice in 45 seconds"
- Clip 2 ("Nobody Is Ever Lost"): Instead of "No kid is lost." → "Why phone bans don't work" or "The real reason kids scroll" or "Lost kids find screens"
- Clip 3 ("Dissatisfied Teacher"): Instead of "Kids know." → "55% want to quit" or "Your kid's teacher hates their job" or "A kindergartner can tell"

**Fix:**
1. Dedicate a sub-agent step to on-screen hook generation with 3-5 options per clip
2. Each option should include the hook category and a one-line rationale for why it complements the audio
3. Update the video-caption-creation skill with complementarity principle and real examples
4. Build a reference library of proven education creator hooks

### 10. Guest Social Research Must Come Early in Pipeline
**The problem:** We got to the end of asset creation without knowing Amar's social handles, which platforms he's active on, what his audience engages with, or how to maximize reshare potential.

**What we need per guest:**
- All personal + company handles (LinkedIn, X, IG, TikTok, YouTube, FB)
- Which platform is their strongest (by engagement, not just follower count)
- What kind of content they typically post/share
- Key hashtags they use
- Audience demographics if visible
- Mutual connections with OpenEd
- Collaboration history (have they shared our content before?)

**Why it matters:**
- Tagging strategy for social posts (tag the right handle on the right platform)
- Caption voice should align with where we expect the most reshare potential
- If the guest is big on LinkedIn but small on X, we optimize LinkedIn first
- Nearbound strategy: what can we offer them that makes them WANT to reshare?

**When:** This should run as Step 0.5 - right after Notion import, before the audit. It takes 2-3 minutes as a web search sub-agent and the output informs clip selection and social strategy.

**Fix:** Add `GUEST_SOCIAL_RESEARCH.md` as a standard deliverable. Run it automatically via sub-agent using the guest name + company from the Notion page.

### 11. YouTube Title + Thumbnail Need Dedicated Variation Step
**The problem:** We generated 30 title options but only ONE thumbnail text per title. Title + thumbnail are a PAIR - they work together. Need 3 thumbnail concepts per title finalist, each with different complementarity strategies.

**What the YouTube title skill already says:**
- 5 titles, 3 thumbnail options each
- Thumbnail should NOT repeat title
- Visual rules: shock > recognition, stock > illustrations, show outcome/situation

**What actually happened:** We generated titles and thumbnail text separately, one-to-one. No variation testing.

**Fix:** After title selection (narrow to 3-4 finalists), run a dedicated title+thumbnail sub-agent that produces 3 visual concepts per title with:
- Visual description (what the thumbnail image shows)
- On-screen text (2-4 words, complements title)
- Why this pairing works (which complementarity strategy)

### 12. DataForSEO Is Sufficient - No Need for Keywords Everywhere
- DataForSEO already provides Google Ads keyword volume (same data source Keywords Everywhere uses)
- YouTube autocomplete available via DataForSEO's Google Autocomplete API with `client=youtube`
- **Revised action:** Build a `youtube_autocomplete.py` script using existing DataForSEO credentials. Skip Keywords Everywhere purchase.

## Proposed Revised Flow (v2)

```
Step 0: Import from Notion (notion_import.py - seconds, no LLM)
Step 0.5: Guest social research (sub-agent web search → GUEST_SOCIAL_RESEARCH.md)
Step 1: SEO keyword research (DataForSEO - automated, quick)
Step 2: Audit (angles, clips, cold opens, day-in-the-life assessment)
  - Informed by SEO data (which keywords have volume?)
  - Informed by guest research (which platforms matter?)
Step 3: Human review of audit → select angle + clips
Step 4: Title + thumbnail variations (3-4 title finalists × 3 thumbnail concepts)
Step 5: On-screen hook generation (3-5 options per clip, dedicated sub-agent)
Step 6: Final clip markup (3 short + 2 long, edit-ready with ~~strikethrough~~)
  - Includes: verbatim transcript, on-screen hook (selected), caption, X variant
Step 7: Cold open assembly (from selected clips)
Step 8: Blog post / day-in-the-life draft (SEO-optimized title, different from YouTube)
Step 9: YouTube description + chapters (keyword-enriched)
Step 10: Social quote cards + nearbound tagging strategy
```

**Key changes from v1:**
- Guest research moved to Step 0.5 (before audit)
- SEO research moved to Step 1 (before audit, informs angles)
- On-screen hooks get their own dedicated step (Step 5)
- Title + thumbnail pairing is a dedicated step (Step 4)
- Nearbound tagging added as part of social output (Step 10)

## Charlie's Preferences (Captured)
- Teacher exodus = strongest angle for this episode
- Likes titles: "How to Build 1,000,000 Schools," "The Reality of Starting Your Own Microschool," "Built 80 Schools Now Wants a Million More"
- Wants KaiPod in some titles
- Different title for YouTube vs blog
- Blog title = SEO optimized
- 5 clips total (3 short, 2 long)
- 2-3 cold open variations max
- Same caption across all short-form platforms (maybe X variant)
- Someone else does the actual video editing in Descript
- On-screen hooks are THE most important visual element - need 3-5 variations per clip, not just one label
- Guest research (handles, platforms, audience) should come early to inform social strategy
- Title + thumbnail are a PAIR - need to be designed together with variations
- Don't over-generate intermediate documents - focus on the final handoff assets
- The handoff doc IS the deliverable - everything flows into one document the editor can use
