# Webflow Publish Skill - Development Notes

**Purpose:** Publish blog posts with images to Webflow CMS via API

**Date:** 2026-01-14
**Status:** ✅ Successfully tested - full workflow documented

---

## API Configuration

**Token Location:** `.env` file as `WEBFLOW_API_KEY`

**Required Scopes:**
- `assets:read` + `assets:write` - Upload images
- `cms:read` + `cms:write` - Create/edit posts
- `sites:read` - Get site ID (required for asset uploads)

**API Base:** `https://api.webflow.com/v2`

---

## Key IDs (OpenEd Site)

| Resource | ID | Notes |
|----------|-----|-------|
| Site ID | `67c7406fc9e6913d1b92e341` | Confirmed via API |
| Posts Collection | `6805bf729a7b33423cc8a08c` | Main blog content |
| Post Type: Blog Posts | `6805d44048df4bd97a0754ed` | For post-type field |
| Post Type: Podcasts | `6805d42ba524fabb70579f4e` | |
| Post Type: Daily Newsletters | `6805d5076ff8c966566279a4` | |
| Post Type: Announcements | `6812753c2611e43906dc13d6` | |

---

## Complete Workflow (Tested 2026-01-14)

### Step 1: Get Site ID
```bash
curl -s "https://api.webflow.com/v2/sites" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "accept: application/json"
```

Response includes `sites[0].id` - use this for asset uploads.

### Step 2: Upload Asset (Image) - Two-Step Process

**Step 2a: Request presigned upload URL**
```bash
# First, compute MD5 hash of your image
FILE_HASH=$(md5 -q /path/to/image.png)

curl -X POST "https://api.webflow.com/v2/sites/67c7406fc9e6913d1b92e341/assets" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"fileName\": \"my-image.png\", \"fileHash\": \"$FILE_HASH\"}"
```

Response contains:
- `uploadUrl` - S3 presigned URL for upload
- `uploadDetails` - Form fields required for S3 upload
- `id` - The asset ID (use for thumbnail field)

**Step 2b: Upload to S3 using presigned URL**
```bash
# Use the uploadUrl and uploadDetails from response
curl -X POST "$UPLOAD_URL" \
  -F "acl=$ACL" \
  -F "bucket=$BUCKET" \
  -F "X-Amz-Algorithm=$ALGORITHM" \
  -F "X-Amz-Credential=$CREDENTIAL" \
  -F "X-Amz-Date=$DATE" \
  -F "key=$KEY" \
  -F "Policy=$POLICY" \
  -F "X-Amz-Signature=$SIGNATURE" \
  -F "success_action_status=201" \
  -F "Content-Type=image/png" \
  -F "Cache-Control=max-age=31536000, immutable" \
  -F "file=@/path/to/image.png"
```

**Step 2c: Construct CDN URL**
After upload, the asset is available at:
```
https://cdn.prod.website-files.com/{site_id}/{asset_id}_{filename}
```

Example: `https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6967cd433862e2c0a5ac8df0_charlynn-chambers-thumbnail.png`

### Step 3: Create CMS Item (Blog Post)
```bash
curl -X POST "https://api.webflow.com/v2/collections/6805bf729a7b33423cc8a08c/items" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "isArchived": false,
    "isDraft": true,
    "fieldData": {
      "name": "Post Title",
      "slug": "post-slug",
      "post-type": ["6805d44048df4bd97a0754ed"],
      "summary": "Meta description for SEO",
      "published-date": "2026-01-14T00:00:00.000Z",
      "thumbnail": {
        "fileId": "6967cd433862e2c0a5ac8df0",
        "url": "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6967cd433862e2c0a5ac8df0_filename.png"
      },
      "content": "<p>HTML content with embedded images...</p>"
    }
  }'
```

### Step 4: Publish (Optional)
- Set `isDraft: false` to publish immediately
- Or publish via Webflow dashboard for review
- Can also use PATCH to update `isDraft` later

---

## CMS Field Schema (Posts Collection)

| Field Slug | Type | Required | Notes |
|------------|------|----------|-------|
| `name` | PlainText | Yes | Post title |
| `slug` | PlainText | Yes | URL slug |
| `post-type` | MultiReference | Yes | Array of post type IDs |
| `thumbnail` | Image | No | {fileId, url} - both required |
| `summary` | PlainText | No | Meta description |
| `published-date` | DateTime | No | ISO 8601 format |
| `content` | RichText | No | HTML content |
| `author` | Reference | No | Author ID |
| `podcast-embed` | RichText | No | For podcast posts |
| `video-embed` | RichText | No | For video posts |

---

## Image Embedding in Rich Text

Images in the `content` field use Webflow's rich text figure format:

**Centered image:**
```html
<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="https://cdn.prod.website-files.com/..." alt="description" loading="lazy">
  </div>
</figure>
```

**Full-width image:**
```html
<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth" data-rt-type="image" data-rt-align="fullwidth">
  <div>
    <img src="https://cdn.prod.website-files.com/..." alt="description" loading="lazy">
  </div>
</figure>
```

---

## Markdown to HTML Conversion

**CRITICAL:** Webflow rich text fields require clean HTML. Converting markdown incorrectly causes rendering issues.

### Common Mistakes (V1 - BROKEN)

1. **Line-by-line processing** - Markdown paragraphs span multiple lines; processing line-by-line breaks them
2. **Wrong conversion order** - Converting bold before links breaks `**[link](url)**` patterns
3. **Missing paragraph wrappers** - Lines starting with `<strong>` or `<a>` weren't wrapped in `<p>`

### Correct Approach (V2 - WORKING)

```python
import re

def convert_inline(text):
    """Convert inline markdown to HTML - LINKS FIRST, then bold/italic."""
    # Links FIRST (so **[link](url)** works)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Then bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Then italic
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    return text

def convert_block(block):
    """Convert a single paragraph block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Headers
    if block.startswith('### '):
        return f'<h3>{convert_inline(block[4:])}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:])}</h2>'
    elif block.startswith('# '):
        return f'<h1>{convert_inline(block[2:])}</h1>'

    # Unordered list
    if block.startswith('- '):
        items = []
        for line in block.split('\n'):
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Blockquote
    if block.startswith('>'):
        return f'<blockquote>{convert_inline(block[1:].strip())}</blockquote>'

    # Regular paragraph - JOIN LINES WITH SPACE
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'

# Split by blank lines (paragraph boundaries)
blocks = re.split(r'\n\s*\n', content)
html = '\n\n'.join(convert_block(b) for b in blocks if convert_block(b))
```

### Key Principles

1. **Split by blank lines first** - Paragraphs in markdown are separated by blank lines
2. **Join multi-line paragraphs** - Lines within a paragraph should be joined with spaces
3. **Convert links before bold** - So `**[text](url)**` becomes `<strong><a href="...">text</a></strong>`
4. **Wrap everything in tags** - Every content block needs `<p>`, `<h2>`, `<ul>`, etc.

---

## Testing Log

### 2026-01-14: Charlotte Mason Article - V2 Fix

**Post:** Charlotte Mason Method
**Post ID:** `6967fb0c1f6ba4d3652f0f03`
**Slug:** `charlotte-mason`

**V1 Issues (BROKEN):**
- Links stripped out (Meg Thomas, Sonya Shafer, Whitney Newby, curriculum links)
- Bold headers orphaned (Children are born persons, etc.)
- Bullet list content disappeared

**V2 Fix:** Rewrote markdown-to-HTML converter with paragraph-based processing
- Used PATCH to update existing post with corrected HTML

---

### 2026-01-14: Full Workflow Test - SUCCESS

**Post:** Charlynn Chambers "Day in the Life" - Menu Method
**Post ID:** `6967d33ca96b6c2fd187053e`
**Slug:** `charlynn-chambers-day-in-the-life`

**Assets Uploaded:**
1. Thumbnail (16:9): `6967cd433862e2c0a5ac8df0`
2. New Yorker Cartoon (1:1): `6967ce3e056baa60d5dad790`
3. Infographic (1:1): `6967d06ba785dcb54f54d0a8`

**Issues Resolved:**
- Initial API key missing `sites:read` scope - user created new key with all required scopes
- Collection ID confusion - `6805d44048df4bd97a0754ed` is post-type, `6805bf729a7b33423cc8a08c` is collection

**Key Learnings:**
1. Asset upload is always two-step: request presigned URL, then POST to S3
2. Thumbnail field requires both `fileId` AND `url`
3. CDN URL pattern: `https://cdn.prod.website-files.com/{site_id}/{asset_id}_{filename}`
4. Rich text images need full `<figure>` wrapper with Webflow classes
5. Create as draft first (`isDraft: true`), review in Webflow, then publish

---

## Author Detection

**Authors Collection ID:** `68089af9024139c740e4b922`

**Known Authors:**
- Charlie Deist: `68089b4d33745cf5ea4d746d`

**Default:** If no author specified, use Charlie Deist.

---

## Thumbnail Handling

**CRITICAL:** The thumbnail image should NOT be included in the article body content. Webflow automatically displays the thumbnail above the article header based on the template design.

If the markdown has a header image at the top:
1. Upload it as the thumbnail (via `thumbnail` field with `fileId` and `url`)
2. Remove it from the HTML body content before creating the post

---

## Future Enhancements

- [x] Convert to formal skill with JSON payload generation (see SKILL.md)
- [x] Add update/PATCH workflow for existing posts
- [x] Author detection and handling
- [ ] Script to batch-add email subscribe embeds to old posts (CMS operation)
- [ ] Integrate with existing `webflow_sync_agent.py` for bidirectional sync
- [ ] Create new authors when not found in Authors collection

