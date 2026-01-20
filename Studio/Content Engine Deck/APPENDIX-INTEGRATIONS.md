# Appendix: Technical Integrations

Detailed documentation of APIs, MCP servers, and external tools.

---

## MCP Servers (Model Context Protocol)

MCP servers extend Claude Code's capabilities by connecting to external services.

### Notion MCP

**Purpose:** Content database access, scheduling, page creation

**Configuration:**
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_*****"
      }
    }
  }
}
```

**Capabilities:**
- Query Master Content Database
- Create new content pages
- Update status (Staging → Approved → Posted)
- Link to Podcast Master Calendar

**Key Database IDs:**
- Master Content Database: `9a2f5189...`
- Podcast Master Calendar: `d60323d3...`
- Content Formats: `2a3afe52...`

### Slack MCP

**Purpose:** Team communication, content sharing

**Use Cases:**
- Pull source material from channels
- Post content notifications
- Alert team to new publications

---

## APIs

### DataForSEO

**Purpose:** Keyword research, SERP analysis, competitor gaps

**Configuration:**
```
Location: .claude/tools/seomachine/data_sources/config/.env
Variables: DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
```

**Endpoints Used:**
- Keyword Data (volume, difficulty, CPC)
- SERP Analysis (current rankings)
- Domain Competitors (gap analysis)

**Example Query:**
```python
# Get keyword metrics
keywords = ["homeschool curriculum", "microschool"]
response = client.keyword_data(keywords, location="United States")
```

### Gemini API

**Purpose:** Image generation, long-context processing

**Model:** `gemini-3-flash-preview` (1M token context)

**Configuration:**
```
Location: .env (vault root)
Variable: GEMINI_API_KEY
```

**Use Cases:**
- Generate thumbnails and headers
- Process large documents
- Style-consistent image series

**Image Generation:**
```bash
python scripts/generate_image.py "prompt" --model pro --aspect 16:9
```

### GetLate API

**Purpose:** Multi-platform social media scheduling

**Platforms Connected:** 8
- Twitter/X
- LinkedIn (personal + company)
- Facebook
- Instagram
- TikTok
- Pinterest
- YouTube
- Threads

**Features:**
- Unified scheduling interface
- No OAuth complexity per platform
- Queue management
- Analytics

### GA4 (Google Analytics 4)

**Purpose:** Traffic analytics, user behavior

**Configuration:**
```
Location: .claude/tools/seomachine/data_sources/config/.env
Variable: GA4_PROPERTY_ID
```

**Metrics Tracked:**
- Page views by content type
- User engagement (scroll depth, time on page)
- Conversion events (newsletter signups)
- Traffic sources

### Google Search Console (Pending)

**Purpose:** Search performance, ranking data

**Status:** Awaiting service account access

**Service Account:**
```
opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com
```

**Planned Uses:**
- Identify SEO quick wins
- Track keyword rankings
- Monitor indexing status

---

## Webflow Integration

**Purpose:** Website content synchronization

**Script:** `agents/webflow_sync.py`

**Capabilities:**
- Pull published content from Webflow
- Sync to local vault
- Update content index

---

## Python Automation

### Agent Scripts

Located in `agents/`:

| Script | Purpose |
|--------|---------|
| `webflow_sync.py` | Sync Webflow content |
| `post_linkedin.py` | Post to LinkedIn |
| `post_tweet.py` | Post to Twitter |
| `post_with_image.py` | Post with images |
| `audit_platforms.py` | Audit connected platforms |

### Image Generation Script

**Location:** `.claude/skills/image-prompt-generator/scripts/generate_image.py`

**Usage:**
```bash
# Basic generation
python generate_image.py "prompt" --model pro

# With options
python generate_image.py "prompt" \
  --model pro \
  --aspect 16:9 \
  --variations 3 \
  --output "./output" \
  --name "thumbnail"
```

**Options:**
- `--model flash|pro` - Speed vs quality
- `--aspect 16:9|1:1|9:16` - Aspect ratio
- `--variations N` - Number of outputs
- `--output PATH` - Save location
- `--name PREFIX` - Filename prefix

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Slack MCP   │  Notion MCP   │  Webflow   │  Podcasts │  GSC    │
└──────┬───────┴───────┬───────┴─────┬──────┴─────┬─────┴────┬────┘
       │               │             │            │          │
       ▼               ▼             ▼            ▼          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│                    Claude Code + Skills                          │
│  ┌──────────────┬──────────────┬──────────────┬───────────────┐ │
│  │ text-content │ podcast-prod │ seo-research │ image-prompt  │ │
│  └──────────────┴──────────────┴──────────────┴───────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  GetLate API  │  Notion DB  │  Webflow  │  Local Vault          │
│  (8 platforms)│  (schedule) │  (CMS)    │  (archive)            │
└───────────────┴─────────────┴───────────┴───────────────────────┘
```

---

## Security & Credentials

### Storage Pattern

Credentials stored in:
1. `.env` files (gitignored)
2. `.claude/settings.local.json` (MCP tokens)
3. Environment variables (session)

### Token Types

| Service | Token Type | Location |
|---------|------------|----------|
| Notion | Integration token (ntn_*) | settings.local.json |
| Slack | xoxc/xoxd tokens | Session context |
| DataForSEO | Login/password | .env |
| Gemini | API key | .env |
| GetLate | API key | TBD |

### Rotation Schedule

- API keys: Quarterly review
- OAuth tokens: Auto-refresh where supported
- Service accounts: Annual audit

---

## Rate Limits & Quotas

| Service | Limit | Notes |
|---------|-------|-------|
| DataForSEO | Pay-per-use | ~$0.01 per keyword |
| Gemini | Varies by model | Flash = higher quota |
| Notion | Varies by plan | Workspace dependent |
| GetLate | Tier dependent | Free tier available |

---

## Error Handling

### Common Issues

**Notion MCP timeout:**
- Cause: Large query or slow connection
- Fix: Paginate queries, retry

**Gemini rate limit:**
- Cause: Too many requests
- Fix: Use Flash model for bulk, Pro for quality

**DataForSEO credit exhaustion:**
- Cause: Large keyword research
- Fix: Monitor usage, batch queries

### Retry Pattern

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(base_delay * (2 ** attempt))
        return wrapper
    return decorator
```

---

*Technical integrations documented - Updated 2026-01-13*
