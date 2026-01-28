# Screenshots Skill

Generate marketing-quality screenshots using Playwright at true HiDPI (2x retina) resolution.

## Invocation

User says: "take screenshot of [url]", "screenshot this article", "/screenshots [url]"

## Prerequisites

Playwright installed at:
```
/Users/charliedeist/Desktop/New Root Docs/.claude/tools/playwright/
```

Chromium browser cached at:
```
~/Library/Caches/ms-playwright/chromium-1208/
```

If browser missing: `cd /path/to/playwright && npx playwright install chromium`

## Quick Screenshot (Single URL)

Use the pre-installed screenshot script:

```bash
cd "/Users/charliedeist/Desktop/New Root Docs/.claude/tools/playwright"
node screenshot.mjs "https://example.com/article" "/path/to/output.png"
```

Output: 2880x1800 retina-quality PNG

For OpenEd social screenshots, save to:
```
/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/Studio/Social Screenshots/YYYY-MM-DD/
```

## Full Page Screenshot

For scrollable content:
```javascript
await page.screenshot({ path: OUTPUT, fullPage: true });
```

## Element-Focused Screenshot

To capture a specific element (headline, quote, etc.):
```javascript
const element = await page.locator('h1.article-title');
await element.screenshot({ path: 'headline.png' });
```

## Dark Mode

```javascript
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  colorScheme: 'dark',
});
```

## Use Cases for RSS Curation

When developing an article into social content:
1. Screenshot the article headline for quote cards
2. Capture any data visualizations or charts
3. Screenshot author info for attribution

## File Naming

```
screenshots/
├── 2026-01-27-edchoice-headline.png
├── 2026-01-27-edchoice-chart.png
└── 2026-01-27-kerry-mcdonald-article.png
```

## Output Location

Default: `./screenshots/` or specify in command.

## Integration

Referenced by:
- `rss-curation` - Screenshot articles when developing into social posts
- `text-content` - Create visual assets for posts
