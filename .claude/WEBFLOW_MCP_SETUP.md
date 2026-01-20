# Webflow MCP Setup - OpenEd Vault Only

This Webflow MCP integration is configured ONLY for the OpenEd Vault workspace. It won't trigger when using Claude in other directories.

## How It Works

1. **Location-specific**: Only active when you run `claude` from within the OpenEd Vault directory
2. **One-time auth**: You'll see the OAuth popup once, then tokens are stored
3. **Full CMS access**: Create, read, update, delete content in Webflow

## When to Use Each Tool

### Python Script (`sync_webflow.py`)
- ✅ Daily content sync
- ✅ No authentication popups
- ✅ Automated/scheduled syncs
- ❌ Read-only access

### Webflow MCP (this setup)
- ✅ Create new blog posts/tools/subjects
- ✅ Full CMS management
- ✅ Stay authenticated between sessions
- ⚠️ One-time OAuth setup required

## First Time Setup

1. Open terminal in OpenEd Vault:
   ```bash
   cd ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/Root\ Docs/OpenEd\ Vault
   claude
   ```

2. When you first use any Webflow command, you'll see the OAuth popup

3. Complete authentication (one time only)

4. Tokens are stored - no more popups!

## Usage Examples

Once authenticated, you can:
- "Create a new blog post in Webflow about [topic]"
- "Update the Webflow tool entry for [tool name]"
- "List recent posts in Webflow"
- "Search Webflow CMS for [keyword]"

## Benefits of This Approach

1. **Isolated**: Won't interfere with Claude in other projects
2. **Clean**: No global OAuth popups
3. **Powerful**: Full CMS access when you need it
4. **Convenient**: Stays authenticated between sessions

## Troubleshooting

If auth expires or you see the popup again:
- Complete the OAuth flow
- Tokens typically last 30-90 days
- Check `~/.mcp-remote/` for stored tokens

## Architecture Summary

**Global (all Claude sessions)**:
- Apify (social scrapers)
- Notion (if added to desktop)

**Root Docs workspace**:
- Notion (research)
- Apify (scrapers)

**OpenEd Vault workspace**:
- Webflow MCP (full CMS access)
- Direct API sync (read-only, no auth)