---
id: opened-20260206-054
title: Audit all blog post images for SEO issues
status: todo
project: seo-content
assignee: claude
priority: medium
effort: 3
due: 2026-02-28
tags: [seo, images, audit]
created: 2026-02-06
updated: 2026-02-06
---

## Context
~50 blog posts on opened.co have images with zero SEO optimization. This task audits every post to identify issues before the batch fix.

Issues to check per post:
- Missing alt text on images
- Missing width/height attributes (causes CLS)
- Wrong Content-Type (JPEG saved as .png)
- Hero image using `loading="lazy"` instead of `loading="eager"` (hurts LCP)
- Non-descriptive filenames (timestamp-based)

**Webflow API:** Use `GET /v2/collections/{POSTS_COLLECTION}/items` to fetch all posts. Parse the `content` HTML field for `<img>` tags.

**Output:** CSV report at `Studio/SEO Content Production/seo-audit-report.csv` with columns: post_id, slug, issue_type, image_src, current_alt, current_loading

## Steps
- [ ] Write audit script using Webflow API
- [ ] Fetch all ~50 blog posts
- [ ] Parse `content` HTML for `<img>` tags
- [ ] Check each image for: alt text, width/height, loading attribute, filename pattern
- [ ] Check thumbnail field for format mismatch
- [ ] Output CSV report
- [ ] Summarize findings (total issues by type)

## Spec Reference
- Webflow API config: `.claude/skills/webflow-publish/SKILL.md`
- Posts Collection ID: `6805bf729a7b33423cc8a08c`
- Site ID: `67c7406fc9e6913d1b92e341`
