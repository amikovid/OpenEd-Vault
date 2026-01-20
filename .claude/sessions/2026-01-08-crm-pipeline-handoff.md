# OpenEd CRM & Guest Contributor Pipeline - Session Handoff

**Date:** 2026-01-08
**Project:** OpenEd Vault / Guest Contributors
**Status:** CRM Complete, 4 Email Drafts Ready

---

## Summary

Completed full CRM audit of 382 contacts extracted from Google Takeout email exports. Identified high-value contributor prospects and created 4 ready-to-send email pitches for guest contributor outreach.

---

## What Was Accomplished

### 1. CRM Review Complete (382/382 contacts)

All contacts in `/OpenEd Vault/CRM/contacts/` have been reviewed and categorized with:
- `type:` provider, contributor, partner, vendor, internal, contact
- `status:` active, warm, dormant, cold, skip
- `priority:` high, medium, low
- Rich notes with relationship context and next steps

### 2. High-Value Contributors Identified

**Tier 1 Ready (Drafts Complete):**

| Contact | Company | Topic | Draft |
|---------|---------|-------|-------|
| Mason Pashia | Getting Smart | Marketplace data collab | `Drafts/mason-pashia-email-draft.md` |
| Kathleen Ouellette | VictoryXR | VR education | `Drafts/kathleen-ouellette-followup.md` |
| Robin Smith | Surge Academy | Coding/game design | `Drafts/robin-smith-pitch.md` |
| Jon England | Libertas Institute | Microschools | `Drafts/jon-england-pitch.md` |

**High-Engagement Contacts Discovered:**

| Contact | Company | Exchanges | Specialty |
|---------|---------|-----------|-----------|
| Sara Jean Kwapien | Outschool | 7 | Online classes, manuscript review |
| Ryhen Miller-Hollis | Education Reimagined | 10 | Learner-centered (blog collab DONE) |
| Robin Smith | Surge Academy | 11 | Coding/tech for homeschoolers |
| Local Artisan Collective | - | 8 | Arts/maker education |
| Sarah Harmeling | Unknown | 9 | ESA/scholarship expert |

### 3. Research Completed

**Robin Smith / Surge Academy:**
- Specialty: Coding, Game Design, Digital Arts, Tech Training
- Location: Bountiful, UT (local!)
- Programs: Homeschool Tech Creators, Unity/C#, Scratch, CompTIA certs

**Jon England / Libertas Institute:**
- Expertise: Microschool POLICY (not just entrepreneurship)
- Authored "Utah's New Microschool Law: a Model for Other States"
- Worked on SB 13 simplifying microschool startup rules
- "How to Start a Microschool" = high-value SEO keyword

### 4. Mbox Sampling (Archived-002.mbox)

Sampled the 3GB archived mail export:
- **Date range:** Dec 11-29, 2025 (very recent)
- **Content:** Mostly newsletters, notifications, receipts
- **Verdict:** NOT worth full processing - would mostly add spam contacts
- **Recommendation:** The Sent.mbox CRM is the valuable data source

---

## File Locations

### CRM System
```
/OpenEd Vault/CRM/
├── _CRM Dashboard.md          # Overview and stats
└── contacts/                  # 382 individual contact files
    ├── {contact-name}.md      # Each with frontmatter + notes
    └── ...
```

### Guest Contributor Pipeline
```
/OpenEd Vault/Studio/SEO Content Production/Guest Contributors/
├── Pipeline.md                # Master tracking document
└── Drafts/
    ├── mason-pashia-email-draft.md      # READY TO SEND
    ├── kathleen-ouellette-followup.md   # READY TO SEND
    ├── robin-smith-pitch.md             # READY TO SEND
    └── jon-england-pitch.md             # READY TO SEND
```

### Source Data
```
/OpenEd Vault/Studio/Email Sorting CRM project/
└── Mail/
    ├── Sent.mbox              # Primary source (processed)
    └── Archived-002 (1).mbox  # Sampled, mostly noise
```

---

## Next Actions (Priority Order)

### Immediate (This Week)
1. **Send Mason Pashia email** - Fresh relationship, major publication
2. **Send Kathleen Ouellette follow-up** - Contributor already pitched, just needs bump
3. **Send Robin Smith pitch** - Highly engaged, local, hot topic
4. **Send Jon England pitch** - Microschool expert, high SEO value

### Follow-Up Queue
5. Sara Jean Kwapien (Outschool) - Manuscript feedback, pitch article
6. Ryhen Miller-Hollis (Education Reimagined) - Reciprocal blog post?
7. Research & revive: The Good and the Beautiful, Rainbow Resource

### Major Partnerships to Revive
- **The Good and the Beautiful** - MAJOR curriculum brand, responded then dormant
- **Rainbow Resource (Zach Smith)** - LARGEST retailer, responded then dormant
- **Tristan Scott / Daylight Computer** - ACTIVE partnership on screen time

---

## Context for Next Session

The "nearbound" strategy is working: ghostwrite articles for industry contacts who get byline credit. This gives OpenEd SEO content from credible sources, and contributors get exposure without doing the writing.

**Key insight:** Focus on contacts with 1:1 send/receive ratios - these are genuine relationships, not one-way outreach.

**Pipeline.md** is the master document - it tracks all tiers, topics, and status.

---

## Workflow Documentation

This CRM was built from scratch using:
1. Google Takeout export of Gmail
2. Python mbox parsing (inline, not saved as scripts)
3. Contact extraction with exchange counts
4. Manual review and categorization
5. Pipeline prioritization

A portable version of this workflow is documented in:
`/skill-stack/content/drafts/email-audit-to-crm-workflow.md`

---

*Last updated: 2026-01-08 08:45*
