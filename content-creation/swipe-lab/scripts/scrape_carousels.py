#!/usr/bin/env python3
"""
Content Scraper — Instagram Carousel Scraper
Scrapes carousel posts from an IG profile, clicks through EVERY slide,
screenshots each one, and extracts text/captions.

Usage:
    python3 scripts/scrape_carousels.py --handle @greatfrontend --output /tmp/carousels
    python3 scripts/scrape_carousels.py --handle @greatfrontend --output /tmp/carousels --max 20
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime

CHROME_PROFILE = os.path.expanduser("~/Library/Caches/ms-playwright/mcp-chrome-profile")
DELAY_BETWEEN_POSTS = 3.0
DELAY_BETWEEN_SLIDES = 1.5


async def scrape_carousels(handle, output_dir, max_posts=None):
    from playwright.async_api import async_playwright

    handle = handle.lstrip("@").split("/")[-1].split("?")[0]
    os.makedirs(f"{output_dir}/slides", exist_ok=True)

    print("=" * 60)
    print("  CAROUSEL SCRAPER — Instagram")
    print("=" * 60)
    print(f"\n  Target: @{handle}")
    if max_posts:
        print(f"  Max posts to check: {max_posts}")

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = await browser.new_page()

        # ── STEP 1: LOAD PROFILE ──
        print(f"\n[1/3] Loading profile...")
        url = f"https://www.instagram.com/{handle}/"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)

        # Extract profile info
        profile = await page.evaluate('''() => {
            const getName = () => {
                const h2 = document.querySelector('header h2');
                return h2 ? h2.textContent.trim() : '';
            };
            const getStats = () => {
                const items = document.querySelectorAll('header section ul li');
                const stats = {};
                items.forEach(li => {
                    const text = li.textContent.trim().toLowerCase();
                    if (text.includes('post')) stats.posts = li.querySelector('span span, span')?.textContent?.trim() || '';
                    if (text.includes('follower') && !text.includes('following')) stats.followers = li.querySelector('span span, a span span')?.textContent?.trim() || '';
                });
                return stats;
            };
            return { username: getName(), stats: getStats() };
        }''')
        stats = profile.get('stats', {})
        print(f"  @{profile.get('username', handle)} | Posts: {stats.get('posts', '?')} | Followers: {stats.get('followers', '?')}")

        # ── STEP 2: SCROLL GRID — COLLECT POST URLS ──
        print(f"\n[2/3] Scrolling grid...")
        post_urls = []
        last_count = 0
        stall_count = 0

        for _ in range(80):
            new_urls = await page.evaluate('''() => {
                const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
                return [...new Set(Array.from(links).map(a => a.href))];
            }''')
            post_urls = list(dict.fromkeys(post_urls + new_urls))

            if max_posts and len(post_urls) >= max_posts:
                post_urls = post_urls[:max_posts]
                break

            if len(post_urls) == last_count:
                stall_count += 1
                if stall_count >= 3:
                    break
            else:
                stall_count = 0
            last_count = len(post_urls)

            await page.evaluate('window.scrollBy(0, 2000)')
            await page.wait_for_timeout(2000)

        print(f"  Found {len(post_urls)} posts to check for carousels")

        # ── STEP 3: VISIT EACH POST — DETECT & SCRAPE CAROUSELS ──
        print(f"\n[3/3] Scanning posts for carousels...")
        carousels = []
        carousel_count = 0
        total_slides = 0

        for i, post_url in enumerate(post_urls):
            try:
                await page.goto(post_url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2500)

                # Detect if this is a carousel (has the next arrow button)
                is_carousel = await page.evaluate('''() => {
                    // Multiple ways to detect carousel
                    const nextBtn = document.querySelector('button[aria-label="Next"]')
                        || document.querySelector('div[role="button"] svg[aria-label="Next"]')
                        || document.querySelector('button svg[aria-label="Next"]');
                    // Also check for dot indicators
                    const dots = document.querySelectorAll('div[style*="transform"] > div[role="tablist"] > div, div._acnb');
                    return !!(nextBtn || dots.length > 1);
                }''')

                if not is_carousel:
                    pct = int((i + 1) / len(post_urls) * 100)
                    print(f"  [{pct:3d}%] skip — not a carousel")
                    await page.wait_for_timeout(1500)
                    continue

                # It's a carousel — extract caption first
                caption = await page.evaluate('''(handle) => {
                    const allSpans = [...document.querySelectorAll('span[dir="auto"]')]
                        .filter(s => !s.closest('nav') && !s.closest('footer'));

                    const isNoise = (t) => {
                        const l = t.trim().toLowerCase();
                        return l.startsWith('and ') || l.startsWith('liked by')
                            || /^\\w+ and (\\d+ others|\\w+)$/i.test(l)
                            || l.includes('was invited') || l.includes('explore insights')
                            || l.length < 5;
                    };

                    // Find caption starting with any username
                    for (const span of allSpans) {
                        const text = span.textContent.trim();
                        const match = text.match(/^(\\w+)(?:Verified)?\\s+(?:Edited[•·]?)?\\s*\\d+[smhdwy](.+)/);
                        if (match && match[2].trim().length > 10 && !isNoise(match[2].trim())) {
                            return match[2].trim();
                        }
                    }

                    // Fallback: longest non-noise span
                    const candidates = allSpans.map(s => s.textContent.trim())
                        .filter(t => t.length > 20 && !isNoise(t))
                        .sort((a, b) => b.length - a.length);
                    return candidates[0] || '';
                }''', handle)

                timestamp = await page.evaluate('''() => {
                    const t = document.querySelector('time[datetime]');
                    return t ? t.getAttribute('datetime') : '';
                }''')

                # Get post ID for file naming
                post_id = post_url.rstrip("/").split("/")[-1]
                post_dir = f"{output_dir}/slides/{post_id}"
                os.makedirs(post_dir, exist_ok=True)

                # Screenshot slide 1
                slide_num = 1
                await page.screenshot(path=f"{post_dir}/slide_{slide_num:02d}.png")

                # Click through remaining slides
                while True:
                    # Try to click "Next" button
                    clicked = await page.evaluate('''() => {
                        // Find the next button by aria-label
                        const btns = document.querySelectorAll('button');
                        for (const btn of btns) {
                            const svg = btn.querySelector('svg[aria-label="Next"]');
                            if (svg) { btn.click(); return true; }
                        }
                        // Fallback: find by class pattern
                        const nextBtn = document.querySelector('button[aria-label="Next"]');
                        if (nextBtn) { nextBtn.click(); return true; }
                        return false;
                    }''')

                    if not clicked:
                        break

                    await page.wait_for_timeout(int(DELAY_BETWEEN_SLIDES * 1000))
                    slide_num += 1
                    await page.screenshot(path=f"{post_dir}/slide_{slide_num:02d}.png")

                    # Safety limit
                    if slide_num >= 20:
                        break

                carousel_data = {
                    "url": post_url,
                    "post_id": post_id,
                    "caption": caption,
                    "published": timestamp[:10] if timestamp else "",
                    "slide_count": slide_num,
                    "slide_dir": post_dir,
                    "slides": [f"slide_{s:02d}.png" for s in range(1, slide_num + 1)],
                }
                carousels.append(carousel_data)
                carousel_count += 1
                total_slides += slide_num

                pct = int((i + 1) / len(post_urls) * 100)
                print(f"  [{pct:3d}%] CAROUSEL #{carousel_count} — {slide_num} slides | {caption[:50]}")

            except Exception as e:
                pct = int((i + 1) / len(post_urls) * 100)
                print(f"  [{pct:3d}%] error: {str(e)[:50]}")

            await page.wait_for_timeout(int(DELAY_BETWEEN_POSTS * 1000))

        await browser.close()

    # ── SAVE INDEX ──
    index = {
        "handle": handle,
        "total_posts_checked": len(post_urls),
        "carousels_found": carousel_count,
        "total_slides": total_slides,
        "avg_slides_per_carousel": round(total_slides / carousel_count, 1) if carousel_count else 0,
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "carousels": carousels,
    }
    index_path = f"{output_dir}/carousel_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"  DONE! @{handle}")
    print(f"  Posts checked:    {len(post_urls)}")
    print(f"  Carousels found:  {carousel_count}")
    print(f"  Total slides:     {total_slides}")
    print(f"  Avg slides/post:  {index['avg_slides_per_carousel']}")
    print(f"  Output:           {output_dir}/")
    print(f"{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(description="Scrape Instagram carousel posts — every slide")
    parser.add_argument("--handle", required=True, help="Instagram handle")
    parser.add_argument("--output", default="/tmp/carousels", help="Output directory")
    parser.add_argument("--max", type=int, default=None, help="Max posts to check")
    args = parser.parse_args()

    asyncio.run(scrape_carousels(args.handle, args.output, args.max))


if __name__ == "__main__":
    main()
