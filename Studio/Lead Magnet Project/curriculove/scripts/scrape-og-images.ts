/**
 * Scrape og:image (and fallback meta images) for curricula missing imageUrl
 *
 * Run with: npx ts-node scripts/scrape-og-images.ts
 * Or: npx tsx scripts/scrape-og-images.ts
 */

import * as fs from 'fs';
import * as path from 'path';

interface Curriculum {
  slug: string;
  name: string;
  website: string;
  imageUrl: string | null;
  [key: string]: unknown;
}

const DATA_PATH = path.join(__dirname, '../src/data/curricula-convex.json');

// Selectors to try for images, in order of preference
const IMAGE_SELECTORS = [
  'meta[property="og:image"]',
  'meta[name="og:image"]',
  'meta[property="twitter:image"]',
  'meta[name="twitter:image"]',
  'meta[property="image"]',
  'meta[name="image"]',
  'link[rel="image_src"]',
];

async function fetchWithTimeout(url: string, timeout = 10000): Promise<Response> {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      },
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    throw error;
  }
}

function extractImageUrl(html: string, baseUrl: string): string | null {
  // Try each selector pattern
  for (const selector of IMAGE_SELECTORS) {
    // Build regex for meta tag content
    const isLinkTag = selector.startsWith('link');
    const attrMatch = selector.match(/\[([^\]=]+)(?:="([^"]+)")?\]/g);

    if (!attrMatch) continue;

    // Extract attribute conditions
    const conditions = attrMatch.map(m => {
      const match = m.match(/\[([^\]=]+)(?:="([^"]+)")?\]/);
      return match ? { attr: match[1], value: match[2] } : null;
    }).filter(Boolean) as { attr: string; value?: string }[];

    // Build regex pattern
    let pattern: RegExp;
    if (isLinkTag) {
      // <link rel="image_src" href="...">
      pattern = /<link[^>]*rel=["']?image_src["']?[^>]*href=["']([^"']+)["'][^>]*>/gi;
    } else {
      // <meta property="og:image" content="...">
      const [{ attr, value }] = conditions;
      pattern = new RegExp(
        `<meta[^>]*${attr}=["']?${value}["']?[^>]*content=["']([^"']+)["'][^>]*>|` +
        `<meta[^>]*content=["']([^"']+)["'][^>]*${attr}=["']?${value}["']?[^>]*>`,
        'gi'
      );
    }

    const match = pattern.exec(html);
    if (match) {
      const imageUrl = match[1] || match[2];
      if (imageUrl) {
        // Resolve relative URLs
        try {
          return new URL(imageUrl, baseUrl).href;
        } catch {
          return imageUrl;
        }
      }
    }
  }

  return null;
}

async function scrapeImage(curriculum: Curriculum): Promise<string | null> {
  if (!curriculum.website) {
    return null;
  }

  try {
    // Normalize URL
    let url = curriculum.website;
    if (!url.startsWith('http')) {
      url = 'https://' + url;
    }

    console.log(`  Fetching: ${url}`);
    const response = await fetchWithTimeout(url);

    if (!response.ok) {
      console.log(`  ❌ HTTP ${response.status}`);
      return null;
    }

    const html = await response.text();
    const imageUrl = extractImageUrl(html, url);

    if (imageUrl) {
      console.log(`  ✅ Found: ${imageUrl.substring(0, 60)}...`);
      return imageUrl;
    } else {
      console.log(`  ⚠️  No og:image found`);
      return null;
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.log(`  ❌ Error: ${message.substring(0, 50)}`);
    return null;
  }
}

async function main() {
  // Load curricula
  const data: Curriculum[] = JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));

  // Filter to those needing images
  const needsImage = data.filter(c => c.imageUrl === null && c.website);
  console.log(`\nFound ${needsImage.length} curricula with website but no image\n`);

  let updated = 0;
  let errors = 0;

  // Process in batches to avoid overwhelming servers
  const BATCH_SIZE = 5;
  const DELAY_MS = 1000;

  for (let i = 0; i < needsImage.length; i += BATCH_SIZE) {
    const batch = needsImage.slice(i, i + BATCH_SIZE);
    console.log(`\n--- Batch ${Math.floor(i / BATCH_SIZE) + 1} of ${Math.ceil(needsImage.length / BATCH_SIZE)} ---\n`);

    const results = await Promise.all(
      batch.map(async (curriculum) => {
        console.log(`[${curriculum.slug}] ${curriculum.name}`);
        const imageUrl = await scrapeImage(curriculum);
        return { slug: curriculum.slug, imageUrl };
      })
    );

    // Update data
    for (const result of results) {
      if (result.imageUrl) {
        const curriculum = data.find(c => c.slug === result.slug);
        if (curriculum) {
          curriculum.imageUrl = result.imageUrl;
          updated++;
        }
      } else {
        errors++;
      }
    }

    // Delay between batches
    if (i + BATCH_SIZE < needsImage.length) {
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
    }
  }

  // Save updated data
  fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2));

  console.log(`\n========================================`);
  console.log(`Done! Updated ${updated} curricula with images`);
  console.log(`Errors/not found: ${errors}`);
  console.log(`========================================\n`);
}

main().catch(console.error);
