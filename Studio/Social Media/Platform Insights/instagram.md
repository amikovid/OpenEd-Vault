# Instagram - Platform Insights

**Status:** Draft - consolidating from multiple sources

---

## Success Heuristic

**Visual-first, Reels dominate** - Instagram has shifted heavily toward video. Reels get 2-3x the reach of static posts. Carousels are second best.

The audience here is further up the funnel - problem aware but not solution aware. They're discovering alternatives, not yet committed.

---

## What Works

### Content Priority (in order)
1. **Reels** - Algorithm heavily favors video
2. **Carousels** - Educational, swipeable content
3. **Static images** - Lowest reach but still useful

### Reel Formats (from video arsenal)
- Text on B-roll
- Podcast clips with captions
- Greenscreen reactions
- iPhone notes style
- POV formats

### Carousel Formats
- Step-by-step guides
- Before/after transformations
- "5 Things" lists
- Quote collections
- Myth vs. Reality

---

## Anti-Patterns

- Text-only posts (no reach)
- Long captions without visual hook
- Over-produced content (authenticity wins)
- Hashtag stuffing in caption body

---

## Platform-Specific Voice

- Friendly, authentic
- Micro-story format
- Less formal than LinkedIn
- Visual storytelling first

---

## Specifications

### Captions
- 30-125 characters optimal for feed
- Longer captions work with strong hook
- Hashtags: 5-10 relevant tags

### Reels
- 9:16 vertical
- 15-60 seconds optimal
- Hook in first 1-3 seconds
- Trending audio helps discovery

### Stories
- Screenshot shares
- Behind-the-scenes
- Polls and questions for engagement

---

## API Notes (Get Late)
- Images supported
- Carousels supported
- Reels require video upload
- Media always required (no text-only)

---

## OpenEd-Specific Notes

- Audience: Earlier in journey, discovery phase
- Goal: Awareness, not conversion
- Repurpose Reels to TikTok and YouTube Shorts
- Use visual content from podcast production

---

---

## ManyChat DM Automation Strategy

**Why this matters for Instagram:** Email gets ~20% open rates. Instagram DMs via ManyChat get **90% open rates** and **60% reply rates**. This is the highest-engagement channel available.

### Core Mechanics

1. **Comment-to-DM Triggers**
   - Post contains a keyword trigger (e.g., "Comment GUIDE for our free homeschool curriculum guide")
   - User comments with keyword → ManyChat auto-DMs the resource
   - Algorithm boost: Comment activity signals engagement, increases reach

2. **Follow-to-DM** (New 2025 Feature)
   - New follower → Automated welcome DM with resource
   - Currently has some Meta-side reliability issues
   - Test before scaling

3. **Story Mention Triggers**
   - User mentions you in story → Auto-DM thank you + resource

### Implementation for OpenEd

**Lead Magnet Delivery:**
- Free curriculum comparisons
- State-specific requirement guides
- Quick-start PDFs

**Keyword Pattern:**
- Post educational content
- End with: "Comment [KEYWORD] and I'll DM you..."
- Keywords: GUIDE, FREEBIE, CHECKLIST, COMPARE, START

**Example Flow:**
```
Post: "5 questions to ask before choosing a curriculum"
CTA: "Comment COMPARE and I'll send you our free curriculum comparison chart"
Result: Comment → ManyChat DM → Link to Notion guide or HubSpot form → Lead captured
```

### Why This Works

1. **Algorithm loves comments** - More engagement = more reach
2. **Permission-based delivery** - User initiates interaction
3. **Instant gratification** - Resource delivered in seconds
4. **List building** - Every DM recipient is a warm lead

### Technical Setup

1. ManyChat account connected to Instagram
2. Keywords configured in Automation → Triggers
3. Flow: Keyword detected → Send message with resource link
4. Optional: Collect email in DM before delivering resource

### Anti-Patterns

- Don't make every post a DM trigger (spammy)
- Don't use generic keywords others might accidentally type
- Don't over-promise in the DM ("you WON'T believe this guide!")
- Don't forget to track conversions (UTM parameters)

### Metrics to Track

- Comment-to-DM conversion rate
- DM-to-click rate
- Click-to-form-submit rate (if collecting emails)
- Overall reach increase from comment activity

---

## Sources
- Studio/Social Media Transformation/Content Formats/Reel
- video-caption-creation skill
- social-media-strategy.md reference
- ManyChat Instagram automation research (2025)
