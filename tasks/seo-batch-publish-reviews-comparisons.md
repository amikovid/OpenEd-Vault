---
id: opened-20260206-001
title: Batch publish tool reviews + comparison articles (full pipeline)
status: todo
project: seo-content
assignee: claude
priority: high
effort: 8
due: 2026-02-14
tags: [tools-directory, comparison, batch, webflow, google-drive, slack]
created: 2026-02-06
updated: 2026-02-06
---

## Context

Grouped workflow to batch-publish tool reviews and comparison articles. The pipeline involves drafting, teacher approval via Google Doc, Slack outreach, and Webflow publishing.

**Tools available:**
- Google Drive MCP → create docs, share with reviewers
- Slack MCP → message teachers for approval
- Webflow API → publish to CMS
- Nano Banana → generate thumbnails

---

## Comparison Articles (Ready to Publish)

These are editorial comparison pieces. May not need teacher sign-off but Charlie should confirm.

| Article | Words | Thumbnail | Draft Location | Status |
|---------|-------|-----------|----------------|--------|
| Khan Academy vs IXL | 1,485 | Done | `Studio/SEO Content Production/Versus/khan-academy-vs-ixl/draft-v1.md` | Ready |
| Saxon vs Math-U-See | 1,607 | Done | `Studio/SEO Content Production/Versus/saxon-vs-math-u-see/draft-v1.md` | Ready |
| IXL vs Exact Path | 1,350 | Done | `Studio/SEO Content Production/Versus/ixl-vs-exact-path/draft-v1.md` | Ready (v2 waiting on Fred) |
| Waldorf vs Montessori | ? | Needs gen | Passed quality loop Jan 29 | Ready |
| Montessori vs Reggio | ? | Needs gen | Draft v1 complete | Ready |

---

## Tool Reviews (Need Drafting + Teacher Approval)

### Authorship model
Pick one teacher as primary author → integrate quotes from others → teacher reviews via Google Doc → teacher approves → publish under their name.

### Reviews with drafts (permission already obtained)

| Tool | Search Vol | Author | Author Webflow ID | Draft Location | Blocker |
|------|-----------|--------|-------------------|----------------|---------|
| Teaching Textbooks | 22.2K | Chelsea Forsythe | TBD - create | `Projects/Tools Directory/drafts/teaching-textbooks.md` | Need external "What Parents Say" quotes |
| Math-U-See | 14.8K | Rachael Davie | `697133d342e4976b0b0f8019` | `Projects/Tools Directory/drafts/math-u-see-v2.md` | Has external quotes, verify Webflow status |
| Saxon Math | 12.1K | Rachael Davie | `697133d342e4976b0b0f8019` | `Projects/Tools Directory/drafts/saxon-math.md` | Need external quotes, verify pricing |
| Beast Academy | 49.5K | Danielle Randall | TBD - create | `Projects/Tools Directory/drafts/beast-academy.md` | Need external quotes, verify pricing |

### Reviews needing drafts (quotes compiled, no draft yet)

| Tool | Search Vol | Current Rank | Author Candidate | Quotes | Quote Source |
|------|-----------|-------------|-----------------|--------|-------------|
| Typing.com | 33K | #11.7 | Karalee Sartin | 4 | `teacher-takes-compilation.md` |
| Lexia | 135K | #17.3 | Rachael Davie | 5 | `teacher-takes-compilation.md` |
| Prodigy Math | 201K | Unranked | Jessica Harter or Chasity Soloman | 6 | `teacher-takes-compilation.md` |
| Reading Eggs | 74K | Unranked | Rachael Davie or Stacy Coplin | 5 | `teacher-takes-compilation.md` |

---

## Approval Pipeline (per review)

```
1. Claude drafts review using TOOL_REVIEW_TEMPLATE.md
   ↓
2. Export draft to Google Doc (Google Drive MCP)
   ↓
3. Share Google Doc with teacher (Google Drive MCP - share by email)
   ↓
4. Send Slack message to teacher:
   "Hey [name], I put together a draft Teacher's Take on [tool]
    using your insights from Slack. Would you mind taking a look
    and letting me know if it captures your experience accurately?
    [Google Doc link]"
   ↓
5. Teacher reviews/edits in Google Doc
   ↓
6. After approval: publish to Webflow Tools collection
```

**Slack contacts for outreach:**
- Rachael Davie (Math-U-See, Saxon, Lexia, Reading Eggs)
- Chelsea Forsythe (Teaching Textbooks)
- Karalee Sartin (Typing.com)
- Danielle Randall (Beast Academy)
- Jessica Harter or Chasity Soloman (Prodigy Math)

---

## Suggested Batch Order

**Wave 1 - Publish immediately (comparisons, no approval needed):**
1. Khan Academy vs IXL
2. Saxon vs Math-U-See
3. Waldorf vs Montessori

**Wave 2 - Drafts ready, send for approval:**
4. Teaching Textbooks → Google Doc → Slack Chelsea
5. Math-U-See → Google Doc → Slack Rachael
6. Beast Academy → Google Doc → Slack Danielle

**Wave 3 - Draft from quotes, then send for approval:**
7. Typing.com (already ranking #11.7 - quick win)
8. Lexia (already ranking #17.3 - quick win, 135K vol)

**Wave 4 - Draft + approval (highest volume):**
9. Prodigy Math (201K vol)
10. Reading Eggs (74K vol)

---

## Key Reference Files
- Template: `Projects/Tools Directory/TOOL_REVIEW_TEMPLATE.md`
- Voice guide: `Projects/Tools Directory/TEACHERS_TAKE_GUIDELINES.md`
- All quotes: `Projects/Tools Directory/teacher-takes-compilation.md`
- Webflow Tools collection: `6811bc7ab1372f43ab83dec6`
- Google Doc for sign-off: `https://docs.google.com/document/d/1omaj39CTcQzP4m1wnVqdsvfC93A3ou4rIu72Y0uUShE/edit`

## Individual Task Files
- `seo-publish-khan-vs-ixl.md`
- `seo-publish-saxon-vs-mathu.md`
- `seo-publish-ixl-vs-exact-path.md`
- `seo-publish-waldorf-vs-montessori.md`
- `seo-montessori-vs-reggio.md`
- `seo-publish-teaching-textbooks.md`
- `seo-tools-math-u-see.md`
- `seo-tools-saxon-math.md`
- `seo-tools-beast-academy.md`
- `seo-tools-typing-lexia.md`
- `seo-tools-prodigy-math.md`
- `seo-tools-reading-eggs.md`
