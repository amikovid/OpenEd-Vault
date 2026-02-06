---
id: opened-20260206-056
title: Batch update blog post HTML with image SEO attributes
status: todo
project: seo-content
assignee: claude
priority: medium
effort: 4
due: 2026-03-15
tags: [seo, images, html, retrofit]
created: 2026-02-06
updated: 2026-02-06
---

## Context
Existing blog posts have `<img>` tags without `width`/`height` attributes and all use `loading="lazy"` (including hero images). This task batch-updates the `content` HTML field on each post.

**Changes per post:**
1. First `<img>` tag: change `loading="lazy"` to `loading="eager" fetchpriority="high"`
2. All `<img>` tags: add `width` and `height` attributes
3. Empty alt text: populate with descriptive text (from image filename or post title)

**Risk:** Webflow rich text may strip `width`/`height` from `<img>` tags. Need to test with one post first. Fallback: add CSS `aspect-ratio` in the blog template instead.

**Rate limiting:** ~50 posts x 1 PATCH call each. 1-second delay between calls.

## Steps
- [ ] Test with one post: PATCH content HTML with width/height on images
- [ ] Verify Webflow preserves the attributes (check rendered HTML)
- [ ] If stripped: implement CSS fallback in template instead
- [ ] If preserved: write batch update script
- [ ] Update hero image loading attribute on each post
- [ ] Add width/height to all images
- [ ] Fill empty alt text
- [ ] Log changes per post

## Spec Reference
- Webflow API: PATCH `/v2/collections/{POSTS_COLLECTION}/items/{post_id}`
- Posts Collection: `6805bf729a7b33423cc8a08c`
- Audit report: `Studio/SEO Content Production/seo-audit-report.csv`
