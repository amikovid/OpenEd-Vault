# Meta API Integration Setup Guide
**For OpenEd Analytics**

---

## Overview

This is **not an MCP** - it's a direct integration with Meta's Graph API using a custom Python module. The module (`meta.py`) makes authenticated HTTP requests to Meta's API endpoints.

**Architecture:**
```
Claude Code → Python Script (meta.py) → Meta Graph API → Facebook/Instagram Data
```

---

## What We Have Access To

### Facebook Page (@openedhq)
| Data Type | Available | Notes |
|-----------|-----------|-------|
| Page info (name, followers, about) | ✅ Yes | |
| Recent posts | ✅ Yes | With reactions, comments, shares |
| Page insights (reach, impressions) | ⚠️ Limited | Some metrics deprecated in v22+ |
| Contact info (phone, email, website) | ✅ Yes | |

### Instagram Business Account (@openedhq)
| Data Type | Available | Notes |
|-----------|-----------|-------|
| Account info (followers, bio, posts) | ✅ Yes | |
| Recent media (posts, reels, carousels) | ✅ Yes | With likes, comments |
| Post reach | ✅ Yes | Per-post reach data |
| Follower demographics | ✅ Yes | Country, age, gender breakdown |
| Online followers (peak hours) | ✅ Yes | When audience is most active |
| Impressions | ❌ Deprecated | Removed in API v22+ |
| Video plays | ❌ Deprecated | Removed in API v22+ |

---

## The "Private App" Setup

### What It Is
A **Meta App** registered in the Facebook Developer Console. This app holds the API credentials that allow programmatic access to your Facebook Page and Instagram Business Account.

**App Details:**
- **App Name:** OpenEd Analytics
- **App ID:** 1447631986927271
- **Type:** Business App
- **Portal:** https://developers.facebook.com/apps/1447631986927271/

### Permissions Granted
These "scopes" determine what data the app can access:

| Permission | What It Allows |
|------------|----------------|
| `pages_show_list` | See list of Pages you manage |
| `pages_read_engagement` | Read Page engagement data (reactions, comments) |
| `pages_read_user_content` | Read posts on the Page |
| `instagram_basic` | Read Instagram profile info |
| `instagram_manage_insights` | Read Instagram analytics |
| `business_management` | Access business-level data |

---

## Authentication: Access Tokens

### How It Works
Meta uses **OAuth 2.0 access tokens** to authenticate API requests. There are different token types:

| Token Type | Duration | Use Case |
|------------|----------|----------|
| Short-lived User Token | ~1 hour | Generated from Graph API Explorer |
| Long-lived User Token | ~60 days | Exchanged from short-lived token |
| Page Access Token | Same as user token | For Page-specific operations |
| System User Token | Never expires | For production apps (requires Business Manager) |

### Current Setup
- **Token Type:** Long-lived User Token
- **Expires:** April 3, 2026 (60 days from generation)
- **Stored In:** `.env` file as `META_ACCESS_TOKEN`

### How to Refresh the Token

**Every ~60 days, you need to refresh:**

1. Go to **Graph API Explorer**: https://developers.facebook.com/tools/explorer/
2. Select your app (**OpenEd Analytics**) from the dropdown
3. Click **Generate Access Token**
4. Check required permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_read_user_content`
   - `instagram_basic`
   - `instagram_manage_insights`
   - `business_management`
5. Click **Generate Access Token** and approve
6. Copy the token

**To get a 60-day token (instead of 1-hour):**

Exchange the short-lived token for a long-lived one:

```bash
curl "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN"
```

Or ask Claude to do it - just provide the App Secret.

**App Secret Location:**
https://developers.facebook.com/apps/1447631986927271/settings/basic/
(Click "Show" next to App Secret)

---

## File Locations

| File | Purpose |
|------|---------|
| `seomachine/data_sources/modules/meta.py` | Python module with API calls |
| `seomachine/data_sources/config/.env` | Stores `META_ACCESS_TOKEN`, `META_PAGE_ID`, `META_INSTAGRAM_ID` |

### .env Variables
```
META_ACCESS_TOKEN=<your-token-here>
META_PAGE_ID=275774935831705
META_INSTAGRAM_ID=17841402982733196
```

---

## How to Set This Up From Scratch

### Step 1: Create a Meta App

1. Go to https://developers.facebook.com/apps/
2. Click **Create App**
3. Choose **Business** type
4. Name it (e.g., "Your Company Analytics")
5. Select your Business Portfolio

### Step 2: Connect Your Facebook Page

1. In App Dashboard → Settings → Basic
2. Scroll to **Business** section
3. Connect your Facebook Page
4. Grant the app access to manage the Page

### Step 3: Connect Instagram Business Account

Your Instagram must be:
- A **Business** or **Creator** account (not personal)
- Linked to a Facebook Page

In Meta Business Suite:
1. Go to Settings → Linked Accounts
2. Connect Instagram to your Facebook Page

### Step 4: Generate Access Token

1. Go to Graph API Explorer
2. Select your app
3. Add permissions (see list above)
4. Generate token
5. Exchange for long-lived token (60 days)

### Step 5: Store Credentials

Create a `.env` file:
```
META_ACCESS_TOKEN=your_long_lived_token
META_PAGE_ID=your_page_id
META_INSTAGRAM_ID=your_instagram_business_id
```

**To find your IDs:**
- Page ID: Graph API Explorer → `GET /me/accounts` → copy `id`
- Instagram ID: Graph API Explorer → `GET /{page-id}?fields=instagram_business_account` → copy `id`

---

## Using with Claude Code

Once set up, you can ask Claude to:
- "Pull my Instagram analytics"
- "Get my recent Facebook posts"
- "Show me follower demographics"
- "Get engagement data for the last month"

Claude will use the `meta.py` module to make API calls and return the data.

---

## Using with Claude.ai (Web/Desktop)

For Claude.ai without terminal access, you have two options:

### Option 1: MCP Server (More Setup)
Install an MCP server like `ig-mcp` that connects to Meta's API:
- GitHub: https://github.com/jlbadano/ig-mcp
- Handles Instagram Business accounts
- Still requires the same token/permissions

### Option 2: Manual Data Pull
1. Use Graph API Explorer to pull data manually
2. Copy/paste into Claude conversation
3. Ask Claude to analyze

---

## Current Audience Demographics (OpenEd)

### Instagram Followers by Country
| Country | Followers | % |
|---------|-----------|---|
| US | 2,109 | 95% |
| Canada | 14 | 0.6% |
| India | 6 | 0.3% |
| Philippines | 6 | 0.3% |

### Instagram Followers by Age/Gender
| Demographic | Followers | % |
|-------------|-----------|---|
| Women 35-44 | 877 | 39% |
| Women 45-54 | 419 | 19% |
| Women 25-34 | 275 | 12% |
| Unknown 35-44 | 135 | 6% |
| Unknown 45-54 | 92 | 4% |
| Men 35-44 | 85 | 4% |

**Key Insight:** 70%+ of followers are women aged 25-54, primarily in the US.

---

## Troubleshooting

### "Invalid OAuth Access Token"
- Token expired - regenerate and update `.env`

### "The value must be a valid insights metric"
- Meta deprecated some metrics - use newer metric names
- Try `reach` instead of `impressions`

### "This endpoint requires the 'xyz' permission"
- Regenerate token with that permission checked

### Token Only Lasts 1 Hour
- You have a short-lived token
- Exchange it for a long-lived token (see above)

---

## Resources

- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **API Reference:** https://developers.facebook.com/docs/graph-api/
- **Instagram API Docs:** https://developers.facebook.com/docs/instagram-api/
- **Permissions Reference:** https://developers.facebook.com/docs/permissions/reference/

---

*Last Updated: February 2, 2026*
