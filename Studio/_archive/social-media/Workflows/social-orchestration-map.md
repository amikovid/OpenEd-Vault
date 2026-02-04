# Social Media Orchestration Map

## Core Insight

We have 100+ proven social media post structures in `social-content-creation/references/post-structures.md`. The goal is to match content to these native formats, not create AI-sounding posts.

## The Real Elements

### Text-Based Posts (Primary)
**Source:** `post-structures.md` - 100+ templates including:
- Heavy Hitting One Liner
- 2x3 Comparison
- The Hard Truth Post
- Problem-Solution Format
- If-Then sequences
- Transformation Journey
- Contrast evaluations
- Lists with punch lines

**Key:** These work because they're human patterns, not AI patterns.

### Visual Formats (Secondary)
**Source:** Content Formats folder
- Text on background (iPhone notes, graph paper, plain)
- Screenshot posts (tweets, reddit)
- Memes (match concept to format)
- Carousels (step-by-step)
- Reels (text reveals)

### Platform Elements
- **Captions**: Instagram, TikTok, YouTube
- **Descriptions**: YouTube (long), Pinterest (SEO)
- **On-screen text**: Reels, TikTok
- **Headlines**: Articles, YouTube titles
- **CTAs**: Comment prompts, DM triggers

## The Workflow

```
CONTENT → EXTRACT → MATCH → ADAPT → DISTRIBUTE
```

1. **Extract** core message from hub content
2. **Match** to post structure from the 100+ templates
3. **Adapt** for platform constraints
4. **Add** visual format if needed
5. **Distribute** via Get Late API

## Progressive Disclosure

When creating a post:
1. Load relevant section of `post-structures.md`
2. Pick 3-5 matching structures
3. Create variations
4. Test which feels most native

## Anti-Pattern Detection

Avoid these AI tells:
- "In today's fast-paced world"
- "It's not about X, it's about Y"
- Correlative constructions
- Perfect grammar/punctuation
- Overly helpful tone

## Next Steps

1. Create skill that properly references post-structures.md
2. Build matcher that connects content → structure
3. Test with Text Heavy format first
4. Add visual layer with Banner Bear
5. Scale to video with ClipCat