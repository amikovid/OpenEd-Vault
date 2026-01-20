# Social Media Engine - Project Spec

**Status:** Active (Phase 1)  
**Created:** 2026-01-12  
**Last Updated:** 2026-01-12

---

## Vision

Unified content repurposing pipeline: Source content → AI drafting → Notion staging → Scheduled distribution across all platforms.

---

## Connected Platforms (via Get Late API)

| Platform | Account | Followers | Permissions | Content Types |
|----------|---------|-----------|-------------|---------------|
| **Twitter/X** | @OpenEdHQ | 260 | tweet.write, media.write | Text (280), Images, Threads |
| **LinkedIn** | OpenEd.co | - | w_organization_social, w_member_social | Text, Images, Documents/PDFs, Carousels |
| **Facebook** | OpenEd HQ | 5,122 | pages_manage_posts | Text, Images, Videos, Links |
| **Instagram** | OpenEd | - | content_publish | Images, Carousels, Reels, Stories |
| **TikTok** | OpenEdHQ | - | video.publish, video.upload | Videos only |
| **YouTube** | OpenEd | - | youtube.upload | Videos, Shorts, Community posts |
| **Pinterest** | openedhq | - | pins:write | Images with links |
| **Reddit** | OpenEd | - | submit | Text, Links, Images |

---

## Content Types by Platform

### Text + Link (easiest)
- Twitter, LinkedIn, Facebook, Reddit

### Text + Image
- Twitter, LinkedIn, Facebook, Instagram, Pinterest

### Text + Video
- TikTok (required), Instagram Reels, YouTube Shorts, Facebook

### Carousels
- Instagram, LinkedIn, TikTok

### Documents
- LinkedIn (PDFs)

### Long-form Video
- YouTube

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SOURCE CONTENT                          │
├─────────────────────────────────────────────────────────────┤
│ • Blog posts (Webflow sync)                                 │
│ • Podcasts (episode folders)                                │
│ • Daily newsletters                                         │
│ • Weekly newsletters                                        │
│ • Standalone social posts                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI DRAFTING LAYER                        │
├─────────────────────────────────────────────────────────────┤
│ Skills (Claude Code):                                       │
│ • linkedin-content - Framework-based LinkedIn posts         │
│ • x-article-converter - Blog → X article + handles          │
│ • social-content-creation - Multi-platform templates        │
│ • video-caption-creation - Short-form video captions        │
│                                                             │
│ Future:                                                     │
│ • instagram-carousel - Carousel image generation            │
│ • tiktok-script - Hook + script for video content           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    NOTION STAGING                           │
├─────────────────────────────────────────────────────────────┤
│ Database: Social Content Queue                              │
│                                                             │
│ Properties:                                                 │
│ • Title (text)                                              │
│ • Platform (multi-select: Twitter, LinkedIn, etc.)          │
│ • Content (rich text - the post copy)                       │
│ • Media (files - images, videos)                            │
│ • Source (relation - to source content)                     │
│ • Status (Draft → Review → Approved → Scheduled → Posted)   │
│ • Scheduled Date (date + time)                              │
│ • Posted URL (url - filled after posting)                   │
│ • Notes (text - for collaborators)                          │
│                                                             │
│ Automation trigger:                                         │
│ • When Status → "Approved" AND Scheduled Date is set        │
│   → Push to Get Late API for scheduling                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GET LATE API                             │
├─────────────────────────────────────────────────────────────┤
│ • Receives post from Notion automation                      │
│ • Handles OAuth tokens for all platforms                    │
│ • Schedules or publishes immediately                        │
│ • Returns post URL to update Notion                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PLATFORMS                                │
├─────────────────────────────────────────────────────────────┤
│ Twitter • LinkedIn • Facebook • Instagram • TikTok          │
│ YouTube • Pinterest • Reddit                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Core Text Posts (Current)
- [x] Get Late API connected
- [x] Test tweet successful
- [x] LinkedIn skill exists
- [x] X article converter skill exists
- [ ] Create Notion Social Content Queue database
- [ ] Build Notion → Get Late webhook/automation
- [ ] Test full pipeline with AI Tutoring article

### Phase 2: Image Posts
- [ ] Image generation workflow (existing thumbnail skill)
- [ ] Platform-specific image sizing
- [x] Upload images to Get Late API (presigned URL workflow - see below)
- [ ] Instagram single-image posts

#### Get Late Media Upload Workflow

```python
# 1. Request presigned URL
response = requests.post(f"{base_url}/media/presign", headers=headers, json={
    "filename": "image.png",
    "contentType": "image/png"
})
upload_url = response.json()["uploadUrl"]
public_url = response.json()["publicUrl"]

# 2. Upload directly to presigned URL
with open("image.png", "rb") as f:
    requests.put(upload_url, data=f, headers={"Content-Type": "image/png"})

# 3. Use publicUrl in post
post_data = {
    "platforms": [{"platform": "linkedin", "accountId": account_id}],
    "content": "Post text here",
    "mediaItems": [{"url": public_url}],  # Array of media objects
    "publishNow": True
}
```

**Supported formats:** JPEG, PNG, WebP, GIF (images), MP4, MPEG, QuickTime (video)
**Max size:** 5GB

### Phase 3: Carousels & Docs
- [ ] LinkedIn PDF/document posts
- [ ] Instagram carousel generation
- [ ] Canva integration or alternative

### Phase 4: Video Content
- [ ] ClipCat or similar for Reels generation
- [ ] TikTok posting workflow
- [ ] YouTube Shorts
- [ ] DM automation for lead magnets (comment → DM flow)

### Phase 5: Analytics & Optimization
- [ ] Performance tracking
- [ ] Best time to post analysis
- [ ] A/B testing frameworks

---

## Existing Skills to Leverage

| Skill | Purpose | Status |
|-------|---------|--------|
| `linkedin-content` | Framework-based LinkedIn posts | Ready |
| `x-article-converter` | Blog → X with handles | Ready |
| `social-content-creation` | Multi-platform templates | Ready |
| `video-caption-creation` | Short-form captions | Ready |
| `hook-and-headline-writing` | Opening hooks | Ready |
| `ghostwriter` | Voice consistency | Ready |
| `image-prompt-generator` | Thumbnail/image creation | Ready |

---

## Key Decisions Needed

1. **Notion Database Structure** - Confirm properties and workflow
2. **Automation Method** - Notion automations vs. Zapier vs. custom webhook
3. **Image Sizing** - Manual or automated platform-specific resizing
4. **Video Tool** - ClipCat, Canva, or other for Reels/TikToks
5. **Approval Workflow** - Who reviews? How many drafts?

---

## Quick Wins (Today)

1. Post the AI Tutoring article to LinkedIn using `linkedin-content` skill
2. Post to Twitter using the X article version we created
3. Manually track in a simple Notion page before building full database

---

## Files

- `agents/social_media_agent.py` - Get Late API wrapper
- `agents/post_with_image.py` - **NEW** Universal posting script with image support
- `agents/post_tweet.py` - Quick tweet script
- `agents/post_linkedin.py` - Quick LinkedIn script
- `agents/test_tweet.py` - API test script
- `agents/audit_platforms.py` - Platform capabilities audit
- `references/getlate-dev-setup.md` - API setup guide
- `.claude/skills/linkedin-content/` - LinkedIn framework skill
- `.claude/skills/x-article-converter/` - X conversion skill
- `.claude/skills/social-content-creation/` - Multi-platform skill
- `.claude/skills/image-prompt-generator/references/newyorker-cartoon.md` - **NEW** New Yorker cartoon style

---

## Known Limitations & Snags

### Platform Limitations

| Issue | Platform | Workaround |
|-------|----------|------------|
| **No @mentions via API** | LinkedIn | Names appear as plain text. Must manually edit post to tag people. |
| **No X Articles via API** | Twitter/X | X Articles (long-form) require posting through X directly. Only tweets (280 char) supported. |
| **No thread posting** | Twitter/X | Must post tweets individually, not as atomic thread. |
| **Media required** | TikTok, Instagram | Cannot post text-only; always need video (TikTok) or image (Instagram). |

### API Quirks

- **Get Late uses `_id` not `id`** - MongoDB-style field names in responses
- **Presigned URL workflow** - Images must be uploaded first, then referenced by `publicUrl`
- **No tag lookup** - Cannot search for LinkedIn profile URIs programmatically

### Content Lessons (This Session)

- **Arrow bullets (→) are AI tells** - Avoid in social posts
- **"180 hours" unclear** - Use "semester" or familiar time units
- **Question hooks work well** - "How do you compress X into Y?" format
- **Feature people who will RT** - Tag and acknowledge contributors
- **Always include images on LinkedIn** - Significantly higher engagement

---

## API Status

| API | Status | Key Location | Notes |
|-----|--------|--------------|-------|
| Get Late | ✅ Active | `.env` → `GETLATE_API_KEY` | 8 platforms connected |
| Webflow | ✅ Active | `.env` → `WEBFLOW_API_KEY` | Blog sync working |
| Gemini | ✅ Active | `.env` → `GEMINI_API_KEY` | Image generation |
| DataForSEO | ✅ Active | `.env` | Keyword research |
| Slack | ✅ Active | xoxc/xoxd tokens | Direct API |
| Notion | ✅ Active | MCP configured | Content databases |
| GSC | ⚠️ Blocked | Need ops | Service account pending |

---

## Next Steps (Priority Order)

### Immediate
1. **Always post with images** - Use `post_with_image.py` going forward
2. **Manual LinkedIn tagging** - Edit posts to add @mentions after posting

### This Week
3. **Create Notion Social Content Queue** - Database for staging posts before publishing
4. **Test cross-platform posting** - Use `post_with_image.py -p linkedin,twitter`
5. **Document image sizing** - Platform-specific dimensions for thumbnails

### Future
6. **Notion → Get Late automation** - Webhook or Zapier when status = Approved
7. **Instagram single-image workflow** - Test with existing thumbnails
8. **Video content pipeline** - Reels, TikTok, YouTube Shorts

---

## Session Log

### 2026-01-12: Initial Setup
- Tested Get Late API successfully (Twitter + LinkedIn)
- Posted AI Tutoring article to both platforms
- Created `x-article-converter` skill
- Updated `social-content-creation` skill with AI tells section
- Created New Yorker cartoon style reference
- Documented image upload workflow (presigned URLs)
- Created universal `post_with_image.py` script
- **Key learning:** LinkedIn doesn't support @mentions via API - must edit manually
