/**
 * Scrape hero images from curriculum websites
 *
 * Usage: npx tsx scripts/scrape-images.ts
 *
 * Strategy:
 * 1. Try og:image meta tag first (most reliable)
 * 2. Fall back to twitter:image
 * 3. Fall back to largest visible image on page
 */

import { chromium, Browser, Page } from "playwright";
import * as fs from "fs";
import * as path from "path";

const DATA_PATH = path.join(__dirname, "../src/data/curricula-convex.json");
const BATCH_SIZE = 5; // Concurrent scrapes
const TIMEOUT = 15000; // 15 seconds per site

interface Curriculum {
  slug: string;
  name: string;
  imageUrl: string | null;
  logoUrl: string | null;
  website: string;
  [key: string]: unknown;
}

async function scrapeImage(page: Page, url: string): Promise<string | null> {
  if (!url || url.trim() === "") {
    return null;
  }

  try {
    // Normalize URL
    let normalizedUrl = url.trim();
    if (!normalizedUrl.startsWith("http")) {
      normalizedUrl = "https://" + normalizedUrl;
    }

    await page.goto(normalizedUrl, {
      waitUntil: "domcontentloaded",
      timeout: TIMEOUT,
    });

    // Try og:image first
    const ogImage = await page.$eval(
      'meta[property="og:image"]',
      (el) => el.getAttribute("content")
    ).catch(() => null);

    if (ogImage && isValidImageUrl(ogImage)) {
      return resolveUrl(ogImage, normalizedUrl);
    }

    // Try twitter:image
    const twitterImage = await page.$eval(
      'meta[name="twitter:image"], meta[property="twitter:image"]',
      (el) => el.getAttribute("content")
    ).catch(() => null);

    if (twitterImage && isValidImageUrl(twitterImage)) {
      return resolveUrl(twitterImage, normalizedUrl);
    }

    // Try to find a hero image (large image near top of page)
    const heroImage = await page.evaluate(() => {
      const images = Array.from(document.querySelectorAll("img"));

      // Filter and score images
      const candidates = images
        .filter((img) => {
          const src = img.src || img.getAttribute("data-src") || "";
          const rect = img.getBoundingClientRect();

          // Skip tiny images, icons, tracking pixels
          if (rect.width < 200 || rect.height < 100) return false;
          if (src.includes("pixel") || src.includes("tracking")) return false;
          if (src.includes(".svg") || src.includes("icon")) return false;

          return true;
        })
        .map((img) => {
          const rect = img.getBoundingClientRect();
          const src = img.src || img.getAttribute("data-src") || "";

          // Score based on size and position (prefer larger images near top)
          const sizeScore = rect.width * rect.height;
          const positionScore = Math.max(0, 1000 - rect.top);

          return {
            src,
            score: sizeScore + positionScore * 100,
          };
        })
        .sort((a, b) => b.score - a.score);

      return candidates[0]?.src || null;
    });

    if (heroImage && isValidImageUrl(heroImage)) {
      return resolveUrl(heroImage, normalizedUrl);
    }

    return null;
  } catch (error) {
    console.error(`  Error scraping ${url}:`, (error as Error).message);
    return null;
  }
}

function isValidImageUrl(url: string): boolean {
  if (!url) return false;
  const lower = url.toLowerCase();
  return (
    lower.includes(".jpg") ||
    lower.includes(".jpeg") ||
    lower.includes(".png") ||
    lower.includes(".webp") ||
    lower.includes(".gif") ||
    lower.includes("image") ||
    lower.includes("photo") ||
    lower.includes("cdn") ||
    lower.includes("static") ||
    lower.includes("media")
  );
}

function resolveUrl(imageUrl: string, baseUrl: string): string {
  try {
    // Already absolute
    if (imageUrl.startsWith("http")) {
      return imageUrl;
    }
    // Protocol-relative
    if (imageUrl.startsWith("//")) {
      return "https:" + imageUrl;
    }
    // Relative URL
    const base = new URL(baseUrl);
    return new URL(imageUrl, base.origin).href;
  } catch {
    return imageUrl;
  }
}

async function main() {
  console.log("Loading curricula data...");
  const data: Curriculum[] = JSON.parse(fs.readFileSync(DATA_PATH, "utf-8"));

  // Find curricula that need images
  const needsImage = data.filter(
    (c) => !c.imageUrl && c.website && c.website.trim() !== ""
  );

  console.log(`Found ${needsImage.length} curricula needing images`);
  console.log(`Starting browser...`);

  const browser = await chromium.launch({ headless: true });

  let updated = 0;
  let failed = 0;

  // Process in batches
  for (let i = 0; i < needsImage.length; i += BATCH_SIZE) {
    const batch = needsImage.slice(i, i + BATCH_SIZE);
    console.log(`\nBatch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(needsImage.length / BATCH_SIZE)}`);

    const results = await Promise.all(
      batch.map(async (curriculum) => {
        const context = await browser.newContext({
          userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        });
        const page = await context.newPage();

        console.log(`  Scraping: ${curriculum.name}`);
        const imageUrl = await scrapeImage(page, curriculum.website);

        await context.close();

        return { slug: curriculum.slug, imageUrl };
      })
    );

    // Update data
    for (const result of results) {
      const curriculum = data.find((c) => c.slug === result.slug);
      if (curriculum && result.imageUrl) {
        curriculum.imageUrl = result.imageUrl;
        console.log(`  ✓ ${curriculum.name}: ${result.imageUrl.slice(0, 60)}...`);
        updated++;
      } else if (curriculum) {
        console.log(`  ✗ ${curriculum.name}: No image found`);
        failed++;
      }
    }

    // Save progress after each batch
    fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2));
  }

  await browser.close();

  console.log(`\n=== Complete ===`);
  console.log(`Updated: ${updated}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total with images: ${data.filter((c) => c.imageUrl).length}/${data.length}`);
}

main().catch(console.error);
