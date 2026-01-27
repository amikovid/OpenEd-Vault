# Slack Bot Content Curator — Format Routing Enhancement

**Status:** Proposed
**Priority:** High (implement ASAP)
**Related:** `FORMAT_INVENTORY.md`, `tool-directory-screenshots.md`

---

## Current State

The Slack bot curates content into the curation inbox. But it doesn't:
- Know which format fits the content
- Suggest screen shares vs. text posts vs. video formats
- Tag near-bound callout opportunities

---

## Proposed Enhancement

When content is curated, the bot should:

1. **Analyze the content** (article, stat, quote, news item)
2. **Suggest format(s)** based on FORMAT_INVENTORY.md rules
3. **Flag special opportunities** (near-bound callouts, screen share candidates)
4. **Auto-generate screenshots** for screen share content

---

## Format Routing Rules

### Input → Format Mapping

| Content Type | Suggested Format(s) | Platform |
|--------------|---------------------|----------|
| **Trending article/headline** | Pointing, Hot Take + Easel, Ed the Horse | IG, TikTok, YT |
| **Stat/data point** | One-liner text post, Stats Infographic | X, LinkedIn |
| **Quote from authority** | Quote + Commentary | X, LinkedIn |
| **Person/company to tag** | Near-bound callout, Featured Post | X, LinkedIn |
| **Visual/product/tool** | Screen share, Is It Reimbursable? | IG, LinkedIn |
| **Emotional story** | Text + B-Roll, Hidden Genius | IG, FB |
| **Question/poll idea** | Question Post | X, LinkedIn |
| **Contrarian take** | Contrarian Take, Ed the Horse | X, LinkedIn, Video |

---

## Near-Bound Callout Detection

**Trigger:** Content mentions a person or company we could tag on social

**Bot action:**
```
🎯 NEAR-BOUND OPPORTUNITY
Content mentions: [Person/Company]
Social handle: @[handle] (if known)
Suggested format: Featured Post with tag
Platform: X / LinkedIn
```

**Handle lookup:** Build a database of known handles for frequent mentions (homeschool influencers, education thought leaders, brands)

---

## Screen Share Integration

**When to suggest:** 
- Content is about a tool, website, or app
- Visual would enhance understanding
- Good for LinkedIn "here's what I found" posts

**Tool:** Use Shpigford/skills `screenshots` skill with Playwright
- Capture at 2880x1800 retina quality
- Auto-crop to relevant area

**Bot action:**
```
📸 SCREEN SHARE CANDIDATE
URL: [url]
Suggested: Capture screenshot of [specific element]
Format: LinkedIn screen share post / IG carousel
[Generate Screenshot] button
```

**Implementation:** 
```bash
npx skills add Shpigford/skills
# Then use: /screenshots [url]
```

See: `Lead Magnet Project/tool-directory-screenshots.md`

---

## Newsletter Segment Routing

### Thought-Tool-Trend
**Trigger:** Content fits one of:
- **Thought:** Idea, philosophy, perspective shift
- **Tool:** Product, app, resource recommendation
- **Trend:** News, data, market movement

**Bot action:**
```
📰 NEWSLETTER SEGMENT: [Thought/Tool/Trend]
Suggested for: OpenEd Weekly
Angle: [brief suggestion]
```

---

## Implementation Plan

### Phase 1: Format Tagging (This Week)
- [ ] Add format suggestion logic to Slack bot
- [ ] Pull from FORMAT_INVENTORY.md rules
- [ ] Output format recommendation with each curated item

### Phase 2: Near-Bound Detection (Week 2)
- [ ] Build handle lookup database
- [ ] Detect @-mention opportunities
- [ ] Flag in curation output

### Phase 3: Screenshot Integration (Week 2-3)
- [ ] Install Shpigford/skills on OpenEd system
- [ ] Add "Generate Screenshot" action to bot
- [ ] Auto-attach to screen share suggestions

### Phase 4: Newsletter Routing (Week 3)
- [ ] Classify as Thought/Tool/Trend
- [ ] Route to newsletter draft folder
- [ ] Suggest angle/hook

---

## Bot Output Format (Enhanced)

```
📥 CURATED: [Title]
Source: [URL]
Type: [Article/Stat/Quote/Tool/News]

📋 FORMAT SUGGESTIONS:
1. [Primary format] → [Platform]
2. [Secondary format] → [Platform]

🎯 SPECIAL FLAGS:
- [ ] Near-bound: Tag @[handle]
- [ ] Screen share candidate
- [ ] Newsletter: [Thought/Tool/Trend]

💡 ANGLE: [One-line hook suggestion]
```

---

## Files to Reference

- `FORMAT_INVENTORY.md` — Full format rules and decision tree
- `Lead Magnet Project/tool-directory-screenshots.md` — Screenshot tool setup
- Platform Insights folder — Platform-specific guidelines

---

*Created: 2026-01-26*
*For: OpenEd Social Media / Slack Bot Enhancement*
