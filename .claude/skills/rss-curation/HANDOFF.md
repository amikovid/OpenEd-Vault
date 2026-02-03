# RSS Curation Skill - Handoff

**Date:** 2026-02-02
**Status:** Full dashboard workflow operational

---

## Current State

### What's Working Now
- **`serve_dashboard.py`** - Local server at `localhost:8000` with auto-save to `tracking.json`
- **Star system** - Star items you want, they disappear from "New" queue
- **Reject with reason** - Captures feedback for prompt improvement
- **Clear Done** - Bulk removes processed items (keeps reject reasons for learning)
- **47 feeds** in `feeds.json` (Freddie deBoer + Rob Henderson removed as off-topic)

### Dashboard Features
- ★ Star button (persists to JSON)
- ✓ Used / ✗ Skip buttons
- Reject reason modal (for prompt learning)
- Clear Done button
- Filter by: status, score, source
- Stats: Total, Definitely, Probably, New, Used, Skipped, Starred

---

## Files

| File | Location | Purpose |
|------|----------|---------|
| `serve_dashboard.py` | `Projects/RSS-Curation/` | **Main entry point** - run this |
| `tracking.json` | `Projects/RSS-Curation/` | All items + starred/rejected state |
| `rss_curation.py` | `/agents/` | Fetch + score script (updates tracking.json) |
| `feeds.json` | `.claude/skills/rss-curation/` | 47 feeds by tier |
| `scoring-prompt.md` | `.claude/skills/rss-curation/` | Scoring criteria |

---

## Daily Workflow

```bash
# 1. Start the dashboard
cd "OpenEd Vault/Projects/RSS-Curation" && python3 serve_dashboard.py &

# 2. Open browser
open http://localhost:8000

# 3. Review items:
#    - ★ Star items you want to use
#    - ✗ Skip with reason (improves prompt)
#    - ✓ Used when you've actually used it
#    - Click Save

# 4. Ask Claude: "check my RSS changes"
```

---

## Session Learnings (2026-02-02)

### Starred Items (to use)
1. "Good printer for home use?" - r/homeschool
2. "Foreword to Virtual Schools, Actual Learning" - Michael B. Horn
3. "The Importance of Handwriting in the Age of AI" - Brave Writer
4. "A Playful, Low-Stress Way to Celebrate Groundhog Day" - Raising Lifelong Learners

### Reject Reasons (for prompt improvement)
| Item | Reason | Add to NO_KEYWORDS? |
|------|--------|---------------------|
| "Philadelphia school safety officers to get bulletproof vests..." | "off topic" | Yes: "bulletproof", "safety officer", "school police" |

### Previously Learned (in NO_KEYWORDS)
- Freddie deBoer, Rob Henderson (feeds removed entirely)
- Policy/political: ESA, voucher, legislation, trump, biden
- Public school focus: district, superintendent, school board
- Local news: snow day, school closure, pre-k application
- Off-topic: oral health, child care, college admission

---

## Prompt Improvement Queue

When you have 5+ reject reasons, update `scoring-prompt.md`:

```markdown
## NO Keywords (instant reject)
- school safety officer, bulletproof, police equipment
- [add more as patterns emerge]
```

---

## Feed Sources (47 active)

**Tier 1 (must-read):** Kerry McDonald, Fab Fridays, Let Grow, Michael B. Horn, Pam Barnhill
**Tier 2 (high-quality):** EdChoice, The 74, Getting Smart, EdSurge, NHERI, Peter Gray
**Tier 3 (blogs):** Simply Charlotte Mason, r/homeschool, Raising Lifelong Learners, etc.
**Tier 4 (substacks):** Ed3 World, Austin Scholar
**Tier 5 (podcasts):** Future of Ed, Hannah Frankman, NREA
**Tier 6 (Google alerts):** homeschooling news, microschool, hybrid homeschool

---

## Next Session

1. [ ] Fetch new items: `python3 agents/rss_curation.py --no-slack`
2. [ ] Review dashboard at `localhost:8000`
3. [ ] After 5+ reject reasons, update scoring-prompt.md
4. [ ] Consider launchd automation for daily 7am runs

---

## To Resume This Workflow

Say: **"Let's continue RSS curation"**

I'll:
1. Start the dashboard server
2. Check tracking.json for current state
3. Optionally fetch new items from feeds
4. You review in browser, I read your changes

---

*Last updated: 2026-02-02*
