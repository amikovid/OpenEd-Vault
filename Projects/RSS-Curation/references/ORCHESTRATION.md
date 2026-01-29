# RSS Curation Orchestration Guide

**Purpose:** Multi-platform content routing from curated RSS articles.

---

## Ed the Horse - X/Twitter Persona

**Voice:** Witty, slightly irreverent, horse puns welcome. Curates the best education/homeschool content.

### Voice Guidelines
- Keep it short (under 100 chars when possible)
- Horse references sparingly - maybe 1 per day max
- Strong opinions, no hedging
- Curating = sharing good stuff with a take
- Link always at end
- No hashtags (or 1 max)

### Post Patterns (in order of preference)

1. **Values Pattern** - Strong take, shareable
   > Free-range kids aren't neglected. They're trusted.
   > [link]

2. **Observation Pattern** - Conversational, slight edge
   > Some families homeschool one kid and not the other. Wild concept: doing what works.
   > [link]

3. **Question Pattern** - Opens curiosity
   > Why do homeschool dads still feel like outsiders? This thread gets real.
   > [link]

4. **Practical Share** - Simple, warm
   > Homeschoolers turning the Olympics into a unit study. Love to see it.
   > [link]

5. **Contrarian** - Strong take, makes people think
   > Phone bans are theater. Actual digital literacy is work.
   > [link]

6. **Normalize Pattern** - Use sparingly
   > Normalize kids playing soccer outside.
   > [link]

7. **Horse Voice** - Max 1 per day
   > Even I know foals need to run free.
   > [link]

---

## Platform Routing

Route content based on source type and angle.

| Source Type | Primary Platform | Secondary | Format |
|-------------|------------------|-----------|--------|
| Thought leader article | X | LinkedIn | Hot take one-liner |
| Reddit discussion | Facebook | X | Screenshot + discussion prompt |
| Data/research piece | LinkedIn | X | "I Call BS" or Authority frame |
| Practical how-to | Instagram | X | Carousel or screenshot |
| Trend/timely topic | Newsletter | All | Context piece |

### Platform-Specific Notes

**X/Twitter (Ed the Horse)**
- One-liners, 70-100 chars optimal
- "I wish I said that" test
- Link at end
- Generate 5 options per article, mark best with `***`

**LinkedIn**
- Links in post get punished - put link in first comment
- Use "I Call BS", MYTH/TRUTH, or Hot Take frameworks
- Data-driven content works best
- Longer form OK (200-400 words)

**Facebook**
- Reddit posts work well as screenshots
- Discussion prompts drive engagement
- Community/relatable content

**Instagram**
- Visual-first - need screenshot or carousel
- Quote cards for hot takes
- Carousel for how-to content

**Newsletter (Trend Items)**
- Context pieces with editorial angle
- Can be more nuanced than social
- Good for "PROBABLY" items that need framing

---

## Reddit Content Handling

Reddit posts are tricky because:
1. Links to Reddit threads don't preview well on X
2. Content is often discussion-based, not article-based

### Approach for Reddit
1. Screenshot the best comment or OP
2. Crop to key content
3. Post screenshot with caption
4. Add thread link in reply (X) or comments (LinkedIn)

---

## Scoring to Platform Mapping

| Score | Platform Priority |
|-------|-------------------|
| DEFINITELY - Hot take | X (Ed) + LinkedIn |
| DEFINITELY - Practical | Instagram + X |
| DEFINITELY - Discussion | Facebook + X |
| PROBABLY - Data/research | LinkedIn (if reframable) |
| PROBABLY - Trend | Newsletter backlog |

---

## Draft Output Format

When generating drafts, always include:

```markdown
## Item X: [Title]

**Source:** [Author/Publication]
**URL:** [Full URL from RSS feed]

### 5 Post Options

1. **Pattern Name**
   > Post text here
   > [link]

2. **Pattern Name** ***
   > Post text here (marked as favorite)
   > [link]

[etc.]

**Pick:** #X - [Reason for recommendation]
```

### User Favorites System
- User marks favorites with `***` asterisks
- Pick up these preferences for final drafts
- Use picks for scheduling queue

---

## LinkedIn Frameworks

### "I Call BS" Framework
```
"[Common belief]."

BS.

[Data/evidence that contradicts]

[2-3 paragraphs unpacking the disconnect]

[Reframe toward OpenEd perspective]

[CTA question]
```

### Hot Take Framework
```
[Controversial opening statement]

Here's what nobody's talking about:

[3-5 bullet points with evidence]

[Takeaway for the audience]
```

---

## Daily Workflow

1. **Fetch** - Pull last 24h from feeds
2. **Score** - DEFINITELY/PROBABLY/NO
3. **Draft X Posts** - 5 options per DEFINITELY item
4. **Route** - Identify LinkedIn, Instagram, Newsletter candidates
5. **Subagent** - Spawn platform-specific agents for non-X content
6. **Review** - User marks favorites with `***`
7. **Finalize** - Generate final drafts with full URLs
8. **Schedule** - Queue for posting

---

## Scheduling Cadence (Ed the Horse)

| Time | Post Type |
|------|-----------|
| 9am | Values/hot take |
| 11am | Question/curiosity |
| 1pm | Observation |
| 3pm | Practical share |
| 5pm | Contrarian/strong take |

---

*Related files:*
- `FEEDS.md` - 64 verified feeds
- `PROJECT.md` - Project overview
- `daily/` - Daily curation outputs
