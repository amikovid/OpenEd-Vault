# MCP Setup Guide for OpenEd Vault

## Currently Configured

| MCP | Status | Config Location |
|-----|--------|-----------------|
| Notion | Configured | Root `.claude/settings.local.json` |
| Slack | Needs Setup | Instructions below |

---

## 1. Notion MCP (Already Working)

Notion is already configured in `/Root Docs/.claude/settings.local.json`.

**Test it:**
```
Use skill_mcp with mcp_name="notion" and a tool_name like "search"
```

---

## 2. Slack MCP Setup

Using `korotovsky/slack-mcp-server` - the most powerful option with stealth mode.

### Step 1: Get Slack Tokens

**Option A: Stealth Mode (Recommended - No Permissions Needed)**

1. Open Slack in browser (not the app)
2. Open DevTools (F12) → Application → Cookies
3. Find cookie named `d` - copy the value (starts with `xoxd-`)
4. In DevTools Console, run: `JSON.parse(localStorage.localConfig_v2).teams[Object.keys(JSON.parse(localStorage.localConfig_v2).teams)[0]].token`
5. Copy the token (starts with `xoxc-`)

**Option B: OAuth Token**
- Create a Slack App at api.slack.com
- Get User OAuth Token (starts with `xoxp-`)

### Step 2: Install via NPM

```bash
npm install -g @anthropics/slack-mcp-server
# OR use npx in the config
```

### Step 3: Add to settings.local.json

Add this to your `/Root Docs/.claude/settings.local.json` mcpServers section:

```json
{
  "mcpServers": {
    "notion": {
      // ... existing notion config
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropics/slack-mcp-server"],
      "env": {
        "SLACK_MCP_XOXC_TOKEN": "xoxc-YOUR-TOKEN-HERE",
        "SLACK_MCP_XOXD_TOKEN": "xoxd-YOUR-TOKEN-HERE"
      }
    }
  }
}
```

**Alternative with korotovsky version (more features):**
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@anthropics/slack-mcp-server@latest", "--transport", "stdio"],
    "env": {
      "SLACK_MCP_XOXC_TOKEN": "xoxc-...",
      "SLACK_MCP_XOXD_TOKEN": "xoxd-..."
    }
  }
}
```

### Step 4: Restart OpenCode

After updating settings.local.json, restart your Claude Code session.

### Slack MCP Tools Available

| Tool | Description |
|------|-------------|
| `conversations_history` | Get messages from channel by ID or #name |
| `conversations_replies` | Get thread replies |
| `conversations_search_messages` | Search messages with filters |
| `channels_list` | List all channels |

### Example Queries (Once Working)

```
Search #recommendations for all mentions of "Saxon Math"
Get last 7 days of messages from #curriculum-feedback
Find all messages containing "Good and the Beautiful"
```

---

## 3. Environment Variables (GEMINI_API_KEY)

For multimodal/PDF analysis, add GEMINI_API_KEY to your shell profile:

**For zsh (default on Mac):**
```bash
echo 'export GEMINI_API_KEY="YOUR-KEY-HERE"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export GEMINI_API_KEY="YOUR-KEY-HERE"' >> ~/.bashrc
source ~/.bashrc
```

Then restart your terminal/OpenCode session.

---

## Troubleshooting

### Notion Not Working
- Check if NOTION_API_KEY is valid
- Ensure the integration has access to the pages you're querying

### Slack Token Expired
- Browser tokens (xoxc/xoxd) expire periodically
- Re-extract from browser when they stop working

### MCP Not Loading
- Check Claude logs: `tail -f ~/Library/Logs/Claude/mcp*.log`
- Verify JSON syntax in settings.local.json

---

*Last Updated: 2026-01-08*
