# Podcast Production SOP

Standard operating procedure for producing an OpenEd podcast episode from recording to publication. Two-person team: Charlie (strategy + Claude sprint) and Chavilah (editing + distribution).

---

## The Four Phases

```
PHASE 1: CLAUDE SPRINT          Charlie     ~2-3 hours    Before editing starts
PHASE 2: DESCRIPT EDITING        Chavilah    ~3-4 hours    Clips first, then full episode
PHASE 3: PUBLISHING              Both        ~1-2 hours    YouTube → Blog → Clips
PHASE 4: NEARBOUND + SOCIAL      Both        ~1 hour       Guest outreach + social posts
```

---

## Phase 1: Claude Sprint

Everything in this phase happens in Claude Code before any editing begins. Goal: produce all the assets the editor needs in one Notion handoff.

### Step 1: Import + Research (automated)

```
Import transcript from Notion → SOURCE.md
Guest social research → handles, platforms, reshare potential
SEO keyword research → target keyword, blog slug
```

**Output:** SOURCE.md, GUEST_SOCIAL_RESEARCH.md, SEO_Keywords.md

### Step 2: Audit + Human Review

```
Full transcript audit → angles, clips, cold opens
```

**Charlie reviews and selects:**
- Primary angle
- 5 clips (3 short + 2 long)
- Cold open preference

### Step 3: Titles + Human Review

```
Title/thumbnail options organized by angle
```

**Charlie selects:**
- YouTube title (CTR optimized)
- Blog title (SEO optimized, different from YouTube)
- Thumbnail direction

### Step 4: Asset Generation

Generate everything and push to Notion as subpages under the episode page:

**Subpage 1: Editor Handoff**
- Cold open options (2-3, with edit markup)
- Short clips (3) with on-screen hook options, verbatim transcripts, edit markup, captions
- Long clips (2) with hooks, narrative arc, captions
- Edit markup key

**Subpage 2: YouTube + Polished Transcript**
- YouTube title + thumbnail options
- YouTube description (single code block, copy-paste ready) including:
  - Episode summary
  - Bullet points
  - Blog post link: `opened.co/blog/[slug]`
  - Transcript link: `opened.co/blog/[slug]#transcript`
  - Guest bio + resources
  - Chapters (integrated at the bottom, not separate)
- Blog slug
- Polished transcript (generated from SOURCE.md, appended to blog post)

**Subpage 3: Blog Post + Social**
- Blog direction (title, target keyword, H2 structure, anchor quotes)
- 5 social quotes with timestamps and use cases
- Social tagging strategy (handles per platform, priority, reshare maximization)

### Step 5: Generate Blog Slug Early

The slug determines URLs that go into the YouTube description and nearbound email. Generate it during the Claude sprint so everything can cross-reference.

**Pattern:** `opened.co/blog/[seo-keyword-slug]`

---

## Phase 2: Descript Editing

### Critical Rule: Cut Clips BEFORE Editing Timeline

All timestamp ranges in the handoff are based on the raw Riverside recording. Once you start cutting filler or inserting the cold open, timestamps shift. So:

1. **Download** aligned video tracks from Riverside (both speakers)
2. **Import** to Descript
3. **Cut clips first** using the timestamp ranges from the Editor Handoff
   - Create each short clip as a new composition (Instagram 9:16 dimensions)
   - Create each long clip as a new composition (YouTube 16:9 dimensions)
4. **Then** edit the full episode timeline (cold open, filler, smoothing)
5. **Export** clips and full episode

### Descript Underlord Instructions

For each clip, give Underlord a prompt like this:

**Short clip creation:**
```
Create a new composition from the current project.

Clip name: "[Clip Name from handoff]"
Timestamp range: [start] to [end]
Aspect ratio: 9:16 (vertical for Instagram/TikTok/Shorts)

From the transcript, find the section starting at [start timestamp]
and ending at [end timestamp].

Cut the following (marked with strikethrough in the handoff):
[paste the specific ~~strikethrough~~ sections]

Apply these word replacements (marked with italics in the handoff):
[paste any *italic* smoothing edits, e.g., change "an action" to "the"]

Keep everything else verbatim.
```

**Long clip creation:**
```
Create a new composition from the current project.

Clip name: "[Clip Name from handoff]"
Timestamp range: [start] to [end]
Aspect ratio: 16:9 (landscape for YouTube)

From the transcript, find the section starting at [start timestamp]
and ending at [end timestamp].

Cut the following sections:
[paste ~~strikethrough~~ sections]

Keep everything else verbatim. This is a longer narrative clip -
preserve the full arc from setup through payoff.
```

**Cold open creation:**
```
Create a new composition called "Cold Open [Option A/B]".
Total target length: 25-35 seconds.

This is a montage of 3 segments from different parts of the episode.
Between each segment, leave a 0.5 second gap (we'll add a SWOOSH transition).

Segment 1: [timestamp] - [paste verbatim with cuts noted]
Segment 2: [timestamp] - [paste verbatim with cuts noted]
Segment 3: [timestamp] - [paste verbatim with cuts noted]
```

### What Underlord Can't Do (Yet)

- Apply branded templates (do manually)
- Add on-screen text overlays (do in CapCut or manually)
- Add [SWOOSH] transitions (add manually between cold open segments)
- Adjust audio levels between speakers

---

## Phase 3: Publishing

Order matters here because of cross-linking dependencies.

### Step 1: Upload Full Episode to YouTube
- Paste title, description, chapters from the YouTube subpage (single code block, copy-paste)
- Set thumbnail
- **Get the YouTube URL** - needed for blog post embed and nearbound email

### Step 2: Publish Blog Post on Webflow
- Use blog direction from subpage 3
- Embed YouTube video at the top
- Append polished transcript at the bottom with `#transcript` anchor
- Slug matches what's already in the YouTube description
- **Confirms the blog URL is live** - YouTube description link now works

### Step 3: Upload Clips
- YouTube Shorts (vertical clips)
- Instagram Reels (same vertical clips, caption from handoff)
- TikTok (same clips, same caption)
- Facebook Reels (same clips, same caption)
- LinkedIn (for guests with LinkedIn presence, post natively)

Use the **same caption** for all platforms. Only X gets a shorter variant.

---

## Phase 4: Nearbound + Social

### Guest Email

Send within 24 hours of publishing. Keep it to **3 links max** for the guest personally.

**For solo guests (no team):**
```
Subject: Your OpenEd episode is live!

Hey [Name],

Your episode just went live - here are the links:

[YouTube link]
[Blog post link]

We also created a few clips for social - would love if you shared
your favorite: [link to best clip on their strongest platform]

Thanks for a great conversation!
```

**For guests with a team (like Amar/KaiPod):**
Same email to the guest, plus a P.S.:

```
P.S. We put together some social copy and clips your team can use
to make sharing easy. Happy to send that over if helpful!
```

If they say yes, send the social quotes + captions from subpage 3.

### Social Posts

- Post clips with captions from handoff
- Tag guest handles on every post (per platform from tagging strategy)
- LinkedIn: lead with data/stats for guests like Amar
- X: use the shorter X variant caption

---

## Production Calendar

| Episode | Guest | Publish | Status |
|---------|-------|---------|--------|
| Mason Ember | Mason Ember | Feb 5 | PUBLISHED |
| Claire Honeycutt R2 | Claire Honeycutt | **Feb 12** | Needs full sprint |
| Amar Kumar | Amar Kumar | Feb 19 | Sprint done, needs editing |
| Bria Bloom | Bria Bloom | Feb 26 | Needs full sprint |

---

## Handoff Checklist

Before handing off to editor, confirm all of these exist in Notion:

- [ ] Editor Handoff subpage (cold opens, clips with markup, captions)
- [ ] YouTube subpage (title, thumbnail options, description as single code block with chapters + blog link + transcript link)
- [ ] Blog + Social subpage (blog direction, social quotes, tagging strategy)
- [ ] Blog slug generated and embedded in YouTube description
- [ ] Guest handles verified and included

---

*Created Feb 6, 2026. Based on Charlie/Chavilah workflow discussion.*
