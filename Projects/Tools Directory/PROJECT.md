---
name: Tools Directory
description: SEO-optimized curriculum reviews with real teacher voices from OpenEd staff
status: active
parent: OpenEd Vault
created: 2026-01-01
updated: 2026-02-02
---

# Tools Directory

**Goal:** Parent- and teacher-reviewed curriculum database. Real voices, real opinions, SEO-optimized.

**Published:** 3 / 20 target | **Drafted:** 4 | **Quotes compiled:** 8 tools

---

## Current State

| Tool | Status | Author | Search Volume |
|------|--------|--------|---------------|
| Math-U-See | Published | Rachael Davie | 14.8K |
| Saxon Math | Published | Rachael Davie | 12.1K |
| Beast Academy | Published | Danielle Randall | 49.5K |
| Teaching Textbooks | Drafted | Chelsea Forsythe | 22.2K |
| Typing.com | Quotes ready | TBD | 33K |
| Lexia | Quotes ready | TBD | 135K |
| Prodigy Math | Quotes ready | TBD | 201K |
| Reading Eggs | Quotes ready | TBD | 74K |

---

## SEO-Prioritized Queue

Prioritized by: search volume, current ranking position, marketplace presence, quote availability.

### Tier 1: Quick Wins (Already Ranking - Push to Page 1)

| Tool | Position | Volume | Quotes | Action |
|------|----------|--------|--------|--------|
| **Typing.com** | #11.7 | 33K | 4 | Add Teacher's Take, optimize |
| **Lexia** | #17.3 | 135K | 5 | Add Teacher's Take, optimize |

### Tier 2: High Volume + In Marketplace

| Tool | Volume | Competition | Quotes | Action |
|------|--------|-------------|--------|--------|
| **Prodigy Math** | 201K | 0.01 | 6 | Draft Teacher's Take |
| **Reading Eggs** | 74K | 0.16 | 5 | Draft Teacher's Take |
| **Beast Academy** | 49.5K | 0.25 | 8 | Published (add more quotes) |

### Tier 3: Publish Existing Drafts

| Tool | Volume | Status |
|------|--------|--------|
| **Teaching Textbooks** | 22.2K | Draft ready, needs Webflow item |

### Tier 4: Future (Compile quotes, then draft)

| Tool | Volume | Notes |
|------|--------|-------|
| Khan Academy | 2.24M | Massive volume, review/comparison angle |
| All About Reading | 14.8K | Rachael has quotes |
| Singapore Math | 18.1K | Rachael has quotes |
| Life of Fred | 1.9K | Lower volume but niche audience |
| Classical Conversations | 22.2K | Not in marketplace |
| Abeka | 74K | Not in marketplace |

---

## Prioritization Heuristic

```
Priority = (Search Volume x Marketplace_Multiplier) / (Competition + 0.1) x Ranking_Bonus
```

- **Marketplace Multiplier:** 2x if in marketplace, 1x if not
- **Ranking Bonus:** 3x if position 11-20, 1.5x if 21-50, 1x if unranked
- **Competition:** 0-1 from DataForSEO

---

## Curriculove Flywheel

```
Curriculove quiz -> User reviews -> Feed Tools Directory -> SEO traffic -> Discover Curriculove
```

| Curriculove | Tools Directory |
|-------------|-----------------|
| Quick voice reviews | Long-form written reviews |
| User-generated | Staff-authored (E-E-A-T) |
| Quantity play | Quality play |
| Lead capture | SEO traffic |

---

## Review Template

Each review uses the toggle-based Webflow template:

| Section | Content |
|---------|---------|
| **Quick Verdict** | One-paragraph OpenEd take |
| **Teacher's Take** | Named author + headshot, narrative with woven colleague quotes |
| **What Parents Say** | External community quotes (blogs, forums) |
| **How It Works** | Subjects, grades, materials, lesson structure |
| **Pricing** | Costs + cost-saving tips |
| **FAQs & Alternatives** | Common questions + linked alternatives |

Full writing guidelines: `TEACHERS_TAKE_GUIDELINES.md`

---

## Webflow CMS

- **Site:** opened.co/tools
- **Tools Collection:** `6811bc7ab1372f43ab83dec6`
- **Authors Collection:** `68089af9024139c740e4b922`

### Published Authors

| Author | Webflow ID | Specialty |
|--------|------------|-----------|
| Rachael Davie | `697133d342e4976b0b0f8019` | Math, former HS teacher |
| Danielle Randall | TBD | Gifted learners |
| Chelsea Forsythe | TBD | Independent curricula |

---

## Workflow

1. **Identify target tool** (use SEO priority queue above)
2. **Pull Slack quotes** (check `teacher-takes-compilation.md` first)
3. **Draft Teacher's Take** using `TEACHERS_TAKE_GUIDELINES.md`
4. **Send for teacher approval** via DM (see `permission-requests/`)
5. **Publish to Webflow** via API
6. **Monitor rankings** via weekly SEO report

---

## Folder Structure

```
Tools Directory/
├── PROJECT.md                       <- You are here
├── TEACHERS_TAKE_GUIDELINES.md      <- Writing voice + structure
├── TOOL_REVIEW_TEMPLATE.md          <- Full review template
├── Interview Template.md            <- Ella interview questions
├── teacher-takes-compilation.md     <- Slack quotes by tool (Feb 2, 2026)
├── webflow_tools_inventory.json     <- All 76 Webflow tool entries
├── drafts/
│   ├── math-u-see-v2.md             PUBLISHED
│   ├── saxon-math.md                PUBLISHED
│   ├── beast-academy.md             PUBLISHED
│   ├── teaching-textbooks.md        READY
│   └── khan-academy-review-draft.md Older format
├── permission-requests/             <- Teacher sign-off records
├── slack-reports/                   <- Raw Slack mining data
├── Webflow Tools Redesign/          <- Page spec + design
└── _archive/                        <- Old audit files
```

---

## Key People

| Person | Role in Project |
|--------|----------------|
| **Rachael Davie** | Lead reviewer, math specialist, most quotes |
| **Danielle Randall** | Beast Academy champion, gifted learners |
| **Chelsea Forsythe** | Independent curricula perspective |
| **Karalee Sartin** | Curriculum team, marketplace knowledge |
| **Keely Shaw-Kueper** | Math-U-See expert (personal + professional) |
| **Fred** (SEO consultant) | Template feedback, SEO strategy |

---

## Dependencies

- [ ] Teaching Textbooks Webflow item needs creating before publish
- [ ] Author profile linking (currently hardcoded)
- [ ] Teacher permission for Typing.com + Lexia + Prodigy + Reading Eggs reviews
- [ ] External "What Parents Say" quotes for new reviews

---

## Google Doc (Teacher Review Drafts)

Existing draft with Math-U-See, Saxon, Beast Academy, Teaching Textbooks sent to teachers for sign-off:
`https://docs.google.com/document/d/1omaj39CTcQzP4m1wnVqdsvfC93A3ou4rIu72Y0uUShE/edit`

---

*Updated: 2026-02-02*
