---
id: opened-20260206-057
title: Generate and populate FAQ schema for all existing blog posts
status: todo
project: seo-content
assignee: claude
priority: medium
effort: 3
due: 2026-03-15
tags: [seo, schema, faq, retrofit]
created: 2026-02-06
updated: 2026-02-06
---

## Context
After the `faq-schema` CMS field is created in Webflow Designer (manual step by Charlie), this task generates FAQPage JSON-LD for each existing blog post and populates the field via API.

**Depends on:** Webflow Designer setup (faq-schema field must exist first). See `Studio/SEO Content Production/seomachine/references/webflow-designer-seo-setup.md`.

**Workflow per post:**
1. GET post content HTML from Webflow API
2. Run `generate_faq_schema(html_content)` from `seo_schema_generator.py`
3. If FAQ pairs found, PATCH the post with `faq-schema` field data
4. Skip posts with no question-pattern H3s

**BlogPosting schema** is handled by the template (injected via Webflow custom code in `<head>`), so only FAQ needs per-post population.

## Steps
- [ ] Verify `faq-schema` CMS field exists in Webflow
- [ ] Write batch script to process all posts
- [ ] Fetch each post's content HTML
- [ ] Generate FAQ schema using `seo_schema_generator.py`
- [ ] PATCH posts that have FAQ content
- [ ] Log: posts with FAQ schema (count), posts skipped (no FAQs)
- [ ] Verify with Google Rich Results Test on 2-3 posts

## Spec Reference
- Schema generator: `Studio/SEO Content Production/seomachine/tools/seo_schema_generator.py`
- Designer setup: `Studio/SEO Content Production/seomachine/references/webflow-designer-seo-setup.md`
- Posts Collection: `6805bf729a7b33423cc8a08c`
