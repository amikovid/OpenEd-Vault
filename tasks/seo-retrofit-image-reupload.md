---
id: opened-20260206-055
title: Convert and re-upload all blog thumbnails as WebP
status: todo
project: seo-content
assignee: claude
priority: medium
effort: 5
due: 2026-03-15
tags: [seo, images, webp, retrofit]
created: 2026-02-06
updated: 2026-02-06
---

## Context
Existing blog post thumbnails are JPEG-as-PNG files with timestamp-based names. This task downloads them, converts to WebP with descriptive filenames, and re-uploads to update the CMS.

**Depends on:** `seo-retrofit-image-audit.md` (use the audit CSV to identify which posts need updates)

**Rate limiting:** Webflow API has 60 req/min limit. Build in 1-second delays between API calls.

**Workflow per post:**
1. Download current thumbnail from CDN URL
2. Convert to WebP using `image_optimizer.py --use thumbnail`
3. Rename to `{article-slug}-thumbnail.webp`
4. Upload to Webflow with descriptive name
5. PATCH the post to update thumbnail field with new asset ID/URL

## Steps
- [ ] Write batch script for thumbnail retrofit
- [ ] Download existing thumbnails from CDN
- [ ] Convert each to WebP with `image_optimizer.py`
- [ ] Re-upload with descriptive filenames
- [ ] Update CMS thumbnail fields via PATCH
- [ ] Verify images render correctly on live site
- [ ] Log results (success/fail per post)

## Spec Reference
- Image optimizer: `.claude/skills/nano-banana-image-generator/scripts/image_optimizer.py`
- Webflow publish: `.claude/skills/webflow-publish/SKILL.md`
- Audit report: `Studio/SEO Content Production/seo-audit-report.csv` (created by audit task)
