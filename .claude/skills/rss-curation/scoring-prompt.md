# RSS Curation Scoring Prompt

## 3-Tier Scoring

### ✅ DEFINITELY (Post to Slack)
- **State news** for AR, IN, IA, KS, MN, MT, NV, OR, UT
- **Families mixing approaches** - Charlotte Mason + Singapore Math + screens, eclectic homeschool
- **Kids thriving outside traditional school** - success stories, outcomes
- **Practical help for overwhelmed parents** - real solutions, not theory
- **Research on homeschool/alternative ed outcomes**
- **Relatable parent moments** - Reddit questions showing real pain points, decision journeys

### 🤔 PROBABLY (Include but lower priority)
- General homeschool/unschool content with fresh angle
- Neurodiversity / "doesn't fit the mold" stories
- Curriculum comparisons (without declaring winners)
- EdTech that could benefit homeschoolers
- ESA/school choice policy news (not the main focus)

### ❌ NO (Skip)
- Public school focused with no homeschool angle
- Pure political school choice (no family/practical angle)
- Generic parenting content
- Trashes public schools without offering alternatives
- Dogmatic single-method advocacy ("unschooling is the ONLY way")
- Clickbait/outrage-bait
- Paywalled content we can't verify

## Post Format

Each DEFINITELY item gets its own Slack message:

```
📰 *[Title]*
_[Source] · [X hours ago]_

[1-2 sentence summary]

💡 *OpenEd angle:* [Why this matters to our audience]

🔗 [URL]
```

PROBABLY items get a single summary message at the end.

## Develop Workflow

When user reacts ✅ to an item or says "develop [item]":
1. Fetch full article via WebFetch
2. Check nearbound index for mentioned people
3. Web search for social handles if not in nearbound
4. Draft 2-3 social post options (use text-content skill)
5. Include @handles for tagging
