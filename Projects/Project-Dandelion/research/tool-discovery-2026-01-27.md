# Tool Discovery Research - Jan 27, 2026

**Source:** X/Twitter links from content creator ecosystem
**Purpose:** Find automation tools for ads, video, content

---

## Constraint: No AI Characters

**OpenEd guardrail:** No fake faces or AI-generated "people." Homeschool parents are trust-sensitive. Authenticity matters.

"Faceless" = actual faceless content (text overlays, screen recordings, b-roll, graphics) - NOT fake AI humans.

**Implication:** Skip the AI character generation tools for now. Do things manually until we find what works, then automate the non-character parts.

---

## Top Priority Tools (Investigate This Week)

### 1. n8n - Workflow Automation
**Source:** @mikefutia
**Relevance:** 4/5 (still useful for non-character automation)

**n8n** - Open-source workflow automation (like Zapier but self-hosted)
- Central hub for automations
- Free tier available, self-hostable
- Useful for: scheduling, publishing, tracking, research aggregation

**Skip for now:**
- ~~Nano Banana~~ (AI characters)
- ~~Veo 3 for UGC-style fake people~~ (AI characters)

**Still valuable n8n use cases:**
- Automate posting schedules
- Aggregate research from multiple sources
- Connect tools (Airtable → social platforms)
- Track performance metrics

---

### 2. Apify + Airtable Research Stack
**Source:** @mikefutia
**Relevance:** 5/5

**Apify** - Web scraping platform
- Instagram Reels scraper (analyze trending content)
- YouTube video scraper (research competitors)
- TikTok scraper
- Facebook Ads Library scraper

**Airtable** - Database backend
- Organize scraped content
- Track what's working
- Build swipe files

**Workflows available:**
- [Instagram Reels analysis](https://n8n.io/workflows/10303-generate-viral-instagram-scripts-by-analyzing-trending-reels-with-apify-and-gpt-4/)
- YouTube research automation
- Facebook Ads spy system

**Application for Project Dandelion:**
- Daily competitor ad monitoring
- Trending content analysis (what hooks are working?)
- Build a swipe file automatically

---

### 3. Faceless YouTube Channel Stack
**Source:** @adam_delduca
**Relevance:** 4/5

Adam Del Duca's approach to YouTube automation:

**Tools:**
- **ElevenLabs** - AI voiceover generation
- **Pictory** - AI video editing
- **ChatGPT** - Script writing
- **VidIQ** - YouTube analytics/optimization

**Application for Project Dandelion:**
- If we test YouTube ads, this stack could produce the creative
- Could create "faceless" educational content at scale
- Worth exploring for long-form YouTube strategy

---

## Medium Priority (Explore Later)

### 4. Vercel Agent Browser
**Source:** @shpigford
**Relevance:** 3/5

Browser automation optimized for AI agents. Faster than Playwright.
- Could be useful for scraping, testing, automation
- Worth noting for future infrastructure

### 5. Creator Buddy / Vibe Coding Academy
**Source:** @alexfinn
**Relevance:** 3/5

AI toolkit for content creators built with Claude Code.
- Alex Finn built to $300K revenue
- "Life Operating System" concept interesting
- Could inform our own skill development

### 6. PromptHero
**Source:** @rameerez
**Relevance:** 3/5

Search engine for AI prompts (Midjourney, Stable Diffusion, etc.)
- Useful for finding proven image prompts
- Could speed up creative generation

---

## Unable to Verify

- **@muteeautomation** - No information found. May be private/new.

---

## Immediate Action Items

### For Elijah (This Week)

1. **Sign up for n8n** (free tier) - https://n8n.io/
2. **Explore the UGC workflow template** - See if we can adapt for OpenEd
3. **Set up Apify account** - Test Instagram Reels scraper on homeschool content
4. **Document findings** in `playbooks/` folder

### For Charlie (Research)

1. **Evaluate Nano Banana** - Is the quality good enough for our brand?
2. **Check Fal.ai pricing** - What's the cost at scale?
3. **Review n8n vs. Make vs. Zapier** - Best automation platform for us?

---

## Links to Explore

**n8n Workflow Templates:**
- https://n8n.io/workflows/8205-generate-ugc-ads-from-google-sheets-with-falai-models-nano-banana-wan22-veo3/
- https://n8n.io/workflows/11204-create-ai-viral-videos-using-nanobanana-2-pro-and-veo31-and-publish-via-blotato/
- https://n8n.io/workflows/9200-automate-and-publish-video-ad-campaigns-with-nanobanana-seedream-gpt-4o-veo-3/
- https://n8n.io/workflows/10303-generate-viral-instagram-scripts-by-analyzing-trending-reels-with-apify-and-gpt-4/

**Fal.ai (Nano Banana):**
- https://fal.ai/

**Apify:**
- https://apify.com/

**VidIQ (YouTube):**
- https://vidiq.com/

---

## How This Fits Project Dandelion

| Tool | Applies To | Use Now? |
|------|------------|----------|
| Apify | Competitive research, trend analysis | Yes - low-hanging fruit |
| Airtable | Tracking/organizing content | Yes |
| VidIQ | YouTube research | Yes (if testing YouTube) |
| n8n | Automation backbone | Later - once we know what works |
| ~~Nano Banana + Veo~~ | ~~AI character generation~~ | No - doesn't fit brand |
| ~~ElevenLabs~~ | ~~AI voiceovers~~ | Maybe later - test manually first |

**The approach:** Manual first, automate later.

1. **Now:** Do things by hand, find formats that work
2. **Research:** Use Apify to see what's trending (hooks, formats, topics)
3. **Track:** Use Airtable to document what we test and results
4. **Later:** Automate the repeatable parts with n8n once we've proven them

---

*Research compiled: 2026-01-27*
