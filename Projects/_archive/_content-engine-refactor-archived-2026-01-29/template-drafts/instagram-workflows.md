# Instagram Content Workflows

## Carousel Workflow

For educational content, stats, or step-by-step guides.

### Structure

| Slide | Purpose | Content |
|-------|---------|---------|
| 1 | Hook | Bold statement, question, or promise. 3-7 words max. |
| 2-4 | Value | Key points, one per slide. Numbered or bulleted. |
| 5 | CTA | "Save this" or "Link in bio" or engagement prompt. |

### Production Steps

1. **Extract content** - Pull 3-5 key points from source
2. **Write hook** - Make slide 1 scroll-stopping
3. **Format each slide** - One concept per slide, minimal text
4. **Visual direction** - Consistent template, brand colors
5. **Caption** - Summarize + hashtags
6. **Quality gate** - Run Lite Quality Loop

### Example Carousel (from newsletter stat)

**Source snippet:** "72% of homeschool parents report their children are more engaged than in traditional school"

**Carousel:**
- Slide 1: "72% more engaged"
- Slide 2: "Homeschool kids vs. traditional school"
- Slide 3: "Why? Self-paced learning."
- Slide 4: "Why? Interest-led projects."
- Slide 5: "Want the full research? Link in bio."

---

## Quote Card Workflow

For hot takes, memorable quotes, or one-liners.

### When to Use

- Hot take from newsletter
- Guest quote from podcast
- Contrarian statement
- Aspirational one-liner

### Production Steps

1. **Extract quote** - 15 words max for readability
2. **Visual direction** - Provide to image-prompt-generator
3. **Generate image** - Use Gemini API via skill
4. **Write caption** - Context + CTA
5. **Add hashtags** - 5-10 niche tags
6. **Quality gate** - Run Lite Quality Loop

### Visual Specs for Quote Cards

**Text requirements:**
- Max 15 words
- 1-2 sentences
- Large, readable font
- High contrast

**Background options:**
- Solid color (OpenEd blue #1E3A5F or green #4A7C59)
- Subtle texture (paper, concrete)
- Blurred photo

**Layout:**
- Text centered or left-aligned
- Attribution smaller below (if quoting someone)
- OpenEd logo subtle in corner

### Image Prompt Template

```
Create a quote card image for Instagram.

Quote: "[QUOTE TEXT]"
Attribution: [NAME if applicable]

Style:
- Clean, minimal
- Background: [solid color OR subtle texture]
- Text: large, readable, white or dark
- Brand color accent: OpenEd blue (#1E3A5F)
- Aspect ratio: 1:1 (square)
```

### Example Quote Card

**Source snippet:** "The goal isn't to prepare kids for the real world. School IS the real world for 13 years of their life."

**Visual direction:**
```
Quote: "School isn't preparation for the real world. For 13 years, it IS the real world."
Background: Subtle concrete texture
Text: White, centered, bold
Accent: OpenEd blue border
```

**Caption:**
"This shifted everything for me.

For 13 years, school IS their life - not preparation for it.

What would change if we treated those years as real life worth living, not just training?

Link in bio for more unconventional education takes."

**Hashtags:**
#educationfreedom #homeschoollife #alternativeeducation #unschooling #edchoice

---

## Reel Caption Workflow

For video clips from podcasts or short-form video.

### When to Use

- Podcast clip (from youtube-clip-extractor)
- Shot video content
- User-generated content reshare

### Caption Structure

1. **Hook line** (first 150 chars visible)
2. **Context** (1-2 sentences)
3. **CTA** (engagement or link in bio)
4. **Hashtags** (5-10)

### Example Reel Caption

**Video:** Podcast clip about interest-led learning

**Caption:**
"Most kids aren't lazy. They're bored.

This clip from our conversation with [Guest] explains why following a child's interests beats forcing a curriculum every time.

Full episode link in bio.

#interestledlearning #homeschool #alternativeeducation #educationfreedom #kidsfirst"

---

## Instagram Format Decision Tree

```
SOURCE CONTENT
    │
    ├─→ Is it visual/video? → REEL
    │
    ├─→ Is it a list/steps/stats? → CAROUSEL
    │
    ├─→ Is it a quote/hot take? → QUOTE CARD
    │
    └─→ Is it a story? → CAROUSEL (story arc) or REEL (if video)
```

---

## Related Skills

- `image-prompt-generator` - Generate quote cards
- `video-caption-creation` - Triple Word Score for Reels
- `text-content` - Caption templates
- `short-form-video` - Full video production
