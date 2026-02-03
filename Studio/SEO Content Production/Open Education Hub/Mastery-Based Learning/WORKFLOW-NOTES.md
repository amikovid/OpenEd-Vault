# Workflow Notes: SEO Deep Dive Process

**Purpose:** Capture learnings from this session to improve the SEO deep dive skill.

---

## Workflow Map (Observed)

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: RESEARCH                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. TOPIC VALIDATION                                        │
│     └─ Sub-agent: SEO keyword research                      │
│        • Search volume estimates                            │
│        • 4-test validation                                  │
│        • Competitive landscape                              │
│                                                             │
│  2. EXISTING CONTENT CHECK                                  │
│     └─ Sub-agent: Notion search (always use sub-agent!)     │
│        • What's already published?                          │
│        • Update vs create new?                              │
│                                                             │
│  3. COMPETITIVE ANALYSIS                                    │
│     └─ Sub-agent: Analyze top rankings                      │
│        • Who's ranking                                      │
│        • Content gaps                                       │
│        • H2 structure patterns                              │
│                                                             │
│  4. PROPRIETARY SOURCE GATHERING                            │
│     └─ Sub-agent: Search podcast archive                    │
│     └─ Grep newsletters for relevant content                │
│     └─ Read book chapters                                   │
│     └─ Check nearbound profiles                             │
│                                                             │
│  [CHECKPOINT 1: Proceed with topic?]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 2: PLANNING                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  5. SOURCE COMPILATION                                      │
│     └─ Sub-agent: Extract all quotes with paths             │
│        • Verbatim quotes                                    │
│        • Speaker + role                                     │
│        • File path                                          │
│        • Context                                            │
│        • Suggested use                                      │
│                                                             │
│  6. HOOK PROPOSALS (4-6 options)                            │
│     └─ Based on proprietary content                         │
│     └─ Differentiated from competitors                      │
│                                                             │
│  7. OUTLINE CREATION                                        │
│     └─ SEO-structured H2s                                   │
│     └─ Map to search intent                                 │
│     └─ FAQ from keyword data                                │
│                                                             │
│  [CHECKPOINT 2: Select hook + approve outline]              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 3: DRAFT                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  8. DRAFT v1                                                │
│     └─ Selected hook                                        │
│     └─ Proprietary quotes integrated                        │
│     └─ Internal links (3+)                                  │
│     └─ Resource list                                        │
│     └─ Meta elements                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 4: QUALITY LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  9. FIVE JUDGES (sequential, blocking)                      │
│                                                             │
│     Judge 1: Human Detector                                 │
│     └─ Zero AI tells (correlatives, forbidden words)        │
│     └─ BLOCKING                                             │
│                                                             │
│     Judge 2: Accuracy Checker                               │
│     └─ All facts verified against sources                   │
│     └─ BLOCKING                                             │
│                                                             │
│     Judge 3: OpenEd Voice                                   │
│     └─ Pro-child, not anti-school                           │
│     └─ BLOCKING                                             │
│                                                             │
│     Judge 4: Reader Advocate                                │
│     └─ Engaging throughout, logical flow                    │
│     └─ BLOCKING                                             │
│                                                             │
│     Judge 5: SEO Advisor                                    │
│     └─ Optimization feedback                                │
│     └─ ADVISORY (does not block)                            │
│                                                             │
│  [CHECKPOINT 3: All judges pass?]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 5: PUBLISH                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  10. FINAL STEPS                                            │
│      └─ Update Webflow                                      │
│      └─ Notify nearbound contacts                           │
│      └─ Update tracking                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Learnings

### 1. Sub-Agents Are Critical

| Task | Why Sub-Agent? |
|------|----------------|
| Notion queries | Responses too large for main context |
| SEO keyword research | Multiple web searches, synthesis |
| Competitive analysis | Multiple page fetches, structured output |
| Podcast archive search | Large corpus, pattern matching |
| Source compilation | Reading multiple files, extraction |

**Rule:** Any task involving 3+ file reads or large API responses should be a sub-agent.

### 2. Check Existing Content First

Before planning new content:
- Search Notion for existing coverage
- Check Published Content for related articles
- Decide: UPDATE existing URL vs CREATE new

This session: Found "Beyond A to F" already exists - updating instead of creating duplicate.

### 3. Read Quality Loop BEFORE Drafting

Know the 5 judges and their criteria before writing:
- Human Detector: No AI tells
- Accuracy Checker: Verified facts
- OpenEd Voice: Pro-child stance
- Reader Advocate: Engaging flow
- SEO Advisor: Optimization

Writing with these in mind reduces iteration.

### 4. Hook Selection Is a Hard Checkpoint

Never draft without user approval of hook direction. Present 4-6 options with clear differentiation.

### 5. Source Attribution Matters

For every proprietary quote, track:
- Exact quote (verbatim)
- Speaker name and role
- File path (for verification)
- Context (what were they discussing)
- Suggested use (which section)

This enables accuracy checking later.

---

## Skill Improvement Recommendations

### For `open-education-hub-deep-dives` skill:

1. **Add SEO validation phase** at start (currently missing)
2. **Mandate Notion sub-agent** for content database queries
3. **Add podcast archive search** as standard step
4. **Include hook proposal checkpoint** before drafting
5. **Reference quality-loop criteria** in skill

### For new `seo-deep-dive` skill (proposed):

Create unified skill that orchestrates:
1. SEO research sub-agent
2. Competitive analysis sub-agent
3. Proprietary source sub-agent
4. Source compilation sub-agent
5. Hook proposals
6. Outline generation
7. Quality loop integration

### Folder Structure Standard

```
/Studio/SEO Content Production/ Open Education Hub / Deep Dive Studio/
└── [Topic Name]/
    ├── PROJECT.md          # Planning, outline, SEO research
    ├── compiled-sources.md # All quotes with attribution
    ├── drafts/
    │   ├── v1.md
    │   ├── v2.md
    │   └── final.md
    └── TRACKING.md         # Quality loop status
```

---

## Session Stats

- Sub-agents spawned: 4
- Files read: 15+
- Notion queries: 2
- Web searches: 10+
- Competitive pages analyzed: 10
- Proprietary quotes found: 29+

---

*Captured: 2026-01-28*
