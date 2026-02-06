# Webflow Designer SEO Setup (Manual Steps)

These steps must be done manually in Webflow Designer. They cannot be automated via API.

---

## 1. Add `faq-schema` CMS Field

**Where:** CMS > Posts collection > Add Field

1. Open Webflow Designer
2. Go to CMS Collections > Posts
3. Click "Add Field"
4. Field type: **Plain Text** (multi-line)
5. Field name: `faq-schema`
6. Label: "FAQ Schema (JSON-LD)"
7. Help text: "Auto-populated by publish scripts. Contains FAQPage structured data for Google rich results."
8. Save

This field will be populated per-article by the publish scripts with FAQ JSON-LD markup.

---

## 2. Add BlogPosting Schema to Blog Template

**Where:** Blog Post template > Page Settings > Custom Code > Before `</head>`

Paste this in the "Head Code" section:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{wf {"path":"name","type":"PlainText"} }}",
  "description": "{{wf {"path":"summary","type":"PlainText"} }}",
  "datePublished": "{{wf {"path":"published-date","type":"Date"} }}",
  "author": {"@type": "Organization", "name": "OpenEd", "url": "https://opened.co"},
  "publisher": {"@type": "Organization", "name": "OpenEd", "url": "https://opened.co"},
  "mainEntityOfPage": "https://opened.co/blog/{{wf {"path":"slug","type":"PlainText"} }}"
}
</script>
```

**Test:** After publishing, view page source and verify the JSON-LD renders with actual values (not template placeholders).

---

## 3. Inject FAQ Schema from CMS Field

**Where:** Blog Post template > body (as an HTML Embed component)

1. In the blog post template, add an **HTML Embed** component (preferably at the bottom of the page, before the footer)
2. Set it to **conditional** - only show when `faq-schema` is not empty
3. Paste this code:

```html
{{#if faq-schema}}
<script type="application/ld+json">
{{wf {"path":"faq-schema","type":"PlainText"} }}
</script>
{{/if}}
```

**Alternative approach** if Webflow conditional rendering doesn't work cleanly with `<script>` tags:
- Use the "Before `</body>`" custom code area in Page Settings instead
- Or use Webflow's native conditional visibility on the embed component

**Note:** Test with a post that has FAQ schema populated. Verify the JSON-LD appears in page source.

---

## 4. Verify Open Graph / Twitter Card Tags

**Where:** Blog Post template > Page Settings

Webflow typically auto-generates OG tags from:
- `og:title` from page title / `name` field
- `og:description` from SEO description / `summary` field
- `og:image` from `thumbnail` field

**Check:**
1. Publish a test post
2. View page source, search for `og:` meta tags
3. Verify `og:title`, `og:description`, `og:image` are populated
4. Check for `twitter:card` meta tag (should be `summary_large_image`)

**If missing, add to template head code:**
```html
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
```

---

## Verification

After completing all steps:

1. Publish a blog post with FAQ content
2. Run Google's [Rich Results Test](https://search.google.com/test/rich-results) on the URL
3. Should show: BlogPosting (from template) + FAQPage (from CMS field)
4. Check [PageSpeed Insights](https://pagespeed.web.dev/) for LCP and CLS scores

---

## Known Risks

1. **Webflow dynamic embeds in `<head>`** may not work cleanly with JSON-LD. Test with one post first. Fallback: HTML embed in body.
2. **Conditional rendering** of FAQ schema may need Webflow's native visibility controls rather than Handlebars `{{#if}}`.
3. **Webflow rich text may strip `width`/`height`** from `<img>` tags. If so, add CSS `aspect-ratio` in the template stylesheet instead.
