#!/usr/bin/env python3
"""
IG Profile Scraper — Full Instagram profile intelligence using Playwright.
No API keys. Uses your logged-in Chrome profile. One mode: EVERYTHING.

Usage:
    python3 scraper.py daniellesmith09                # Full scrape (every caption)
    python3 scraper.py daniellesmith09 --transcribe   # + download & transcribe reels

Output: /tmp/ig-intel/{handle}/
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime

CHROME_PROFILE = os.path.expanduser("~/Library/Caches/ms-playwright/mcp-chrome-profile")
OUTPUT_DIR = "/tmp/ig-intel"

# Multiple selectors per element — when Instagram changes their DOM, fallbacks catch it
CAPTION_SELECTORS = [
    'article div > ul > div span[dir="auto"]',
    'article span[dir="auto"]',
    'div[class*="Caption"] span',
    'h1 ~ div span[dir="auto"]',
]


async def scrape_profile(handle: str, transcribe_reels: bool = False):
    from playwright.async_api import async_playwright

    handle = handle.lstrip("@").split("/")[-1].split("?")[0]
    out_dir = f"{OUTPUT_DIR}/{handle}"
    os.makedirs(f"{out_dir}/screenshots", exist_ok=True)

    print(f"\n{'='*50}")
    print(f"  IG Profile Scraper — @{handle}")
    print(f"  Full scrape{' + reel transcription' if transcribe_reels else ''}")
    print(f"{'='*50}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await browser.new_page()

        # ── LOAD PROFILE ──
        print("[1/3] Loading profile...")
        url = f"https://www.instagram.com/{handle}/"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        await page.screenshot(path=f"{out_dir}/screenshots/profile.png")

        profile = await page.evaluate('''() => {
            const getName = () => {
                const h2 = document.querySelector('header h2');
                return h2 ? h2.textContent.trim() : '';
            };
            const getBio = () => {
                const spans = document.querySelectorAll('header section span');
                for (const s of spans) {
                    if (s.textContent.length > 3 && !s.closest('a') && !s.textContent.match(/^\\d/)) {
                        return s.textContent.trim();
                    }
                }
                return '';
            };
            const getStats = () => {
                const items = document.querySelectorAll('header section ul li');
                const stats = {};
                items.forEach(li => {
                    const text = li.textContent.trim().toLowerCase();
                    if (text.includes('post')) stats.posts = li.querySelector('span span, span')?.textContent?.trim() || '';
                    if (text.includes('follower') && !text.includes('following')) stats.followers = li.querySelector('span span, a span span')?.textContent?.trim() || '';
                    if (text.includes('following')) stats.following = li.querySelector('span span, a span span')?.textContent?.trim() || '';
                });
                return stats;
            };
            return {
                username: getName(),
                bio: getBio(),
                stats: getStats(),
                scraped_at: new Date().toISOString()
            };
        }''')

        print(f"  @{profile.get('username', handle)}")
        stats = profile.get('stats', {})
        print(f"  Posts: {stats.get('posts', '?')} | Followers: {stats.get('followers', '?')} | Following: {stats.get('following', '?')}")
        print(f"  Bio: {profile.get('bio', '(none)')[:80]}")

        # ── SCROLL GRID — COLLECT ALL POST URLS ──
        print("\n[2/3] Scrolling grid...")
        post_urls = []
        last_count = 0

        for i in range(50):  # safety limit
            new_urls = await page.evaluate('''() => {
                const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
                return [...new Set(Array.from(links).map(a => a.href))];
            }''')
            post_urls = list(dict.fromkeys(post_urls + new_urls))

            if len(post_urls) == last_count:
                # One more try
                await page.evaluate('window.scrollBy(0, 3000)')
                await page.wait_for_timeout(3000)
                retry = await page.evaluate('''() => {
                    const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
                    return [...new Set(Array.from(links).map(a => a.href))];
                }''')
                post_urls = list(dict.fromkeys(post_urls + retry))
                if len(post_urls) == last_count:
                    break

            last_count = len(post_urls)
            await page.evaluate('window.scrollBy(0, 2000)')
            await page.wait_for_timeout(2000)

        # Grab alt text from grid thumbnails
        grid_data = await page.evaluate('''() => {
            const posts = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
            return Array.from(posts).map(a => ({
                href: a.href,
                alt: a.querySelector('img') ? a.querySelector('img').alt : '',
                is_reel: a.href.includes('/reel/')
            }));
        }''')

        await page.screenshot(path=f"{out_dir}/screenshots/grid_end.png")
        print(f"  Found {len(post_urls)} posts")

        # ── DRILL INTO EVERY POST ──
        print(f"\n[3/3] Reading every caption ({len(post_urls)} posts)...")
        posts = []
        retry_queue = []  # Posts that got redirected
        for i, post_url in enumerate(post_urls):
            try:
                await page.goto(post_url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(3500)

                # Detect redirect: if URL doesn't contain /p/ or /reel/, we got bounced
                current_url = page.url
                if '/p/' not in current_url and '/reel/' not in current_url:
                    retry_queue.append((i, post_url))
                    if len(retry_queue) % 5 == 0:
                        print(f"  {len(retry_queue)} posts redirected (will retry with longer delays)")
                    await page.wait_for_timeout(3000)  # Cool down before next attempt
                    continue

                post_data = await page.evaluate('''(postUrl) => {
                    // Extract username from URL: instagram.com/{username}/p/...
                    const urlParts = postUrl.replace(/https?:\\/\\/[^/]+\\//, '').split('/');
                    const username = urlParts[0];

                    // 2026 Instagram DOM: caption lives in span[dir="auto"] that starts
                    // with "username" + time indicator (e.g. "11w") + caption text.
                    // Strategy: find that span, then extract caption child OR strip prefix.
                    const spans = document.querySelectorAll('span[dir="auto"]');
                    let caption = '';

                    for (const span of spans) {
                        const text = span.textContent || '';
                        if (text.startsWith(username) && text.length > username.length + 3) {
                            // Found the caption container. Strip username + time prefix.
                            // Time prefixes: "11w", "2d", "3h", "1y", "52w", etc.
                            let remainder = text.substring(username.length);
                            remainder = remainder.replace(/^\\s*\\d+[smhdwy]\\s*/, '').trim();
                            if (remainder.length > 0) {
                                caption = remainder;
                                break;
                            }
                        }
                    }

                    // Fallback: look for caption-specific class spans
                    if (!caption) {
                        const captionSpans = document.querySelectorAll('span.x193iq5w');
                        const skip = ['Notifications', 'Also from Meta', 'View all', '©', 'Consumer Health',
                                      'Instagram Lite', 'Contact Uploading', 'Meta Verified', 'Verified'];
                        for (const s of captionSpans) {
                            const t = s.textContent.trim();
                            if (t.length > 10 && !t.startsWith(username) &&
                                !skip.some(x => t.startsWith(x)) && !t.includes('cookie')) {
                                // Check it's not a comment (comments come after caption)
                                caption = t;
                                break;
                            }
                        }
                    }

                    const timeEl = document.querySelector('time[datetime]');
                    const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';
                    const timeText = timeEl ? timeEl.textContent.trim() : '';

                    const img = document.querySelector('article img[alt]:not([alt=""])') ||
                                document.querySelector('main img[alt]:not([alt=""])');
                    const alt = img ? img.alt : '';

                    const isVideo = !!document.querySelector('video');

                    // Also grab comments
                    const comments = [];
                    let foundCaption = false;
                    for (const span of spans) {
                        const text = span.textContent || '';
                        // Comments also follow the username + time + text pattern
                        // but from different usernames
                        if (text.startsWith(username) && !foundCaption) {
                            foundCaption = true;
                            continue;
                        }
                        if (foundCaption && text.length > 5 && !text.startsWith('View all') &&
                            !text.startsWith('Notifications') && !text.includes('©')) {
                            const match = text.match(/^([\\w.]+).*?\\d+[smhdwy]\\s*(.+)/);
                            if (match && comments.length < 5) {
                                comments.push({ user: match[1], text: match[2].trim() });
                            }
                        }
                    }

                    return { caption, timestamp, time_text: timeText, alt, is_video: isVideo, top_comments: comments };
                }''', post_url)

                post_data['url'] = post_url
                post_data['index'] = i + 1
                post_data['is_reel'] = '/reel/' in post_url
                posts.append(post_data)

                if (i + 1) % 10 == 0 or (i + 1) == len(post_urls):
                    print(f"  {i + 1}/{len(post_urls)} done")

                # Polite delay — extra pause every 5 posts to stay safe
                await page.wait_for_timeout(1500 + (1000 if (i + 1) % 5 == 0 else 0))

            except Exception as e:
                posts.append({'url': post_url, 'index': i + 1, 'error': str(e)})

        # ── RETRY REDIRECTED POSTS ──
        if retry_queue:
            print(f"\n  Retrying {len(retry_queue)} redirected posts with longer delays...")
            for idx, (orig_i, post_url) in enumerate(retry_queue):
                try:
                    await page.wait_for_timeout(5000)  # Longer cooldown
                    await page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(5000)

                    current_url = page.url
                    if '/p/' not in current_url and '/reel/' not in current_url:
                        posts.append({'url': post_url, 'index': orig_i + 1, 'caption': '', 'note': 'redirected_twice'})
                        continue

                    post_data = await page.evaluate('''(postUrl) => {
                        const urlParts = postUrl.replace(/https?:\\/\\/[^/]+\\//, '').split('/');
                        const username = urlParts[0];
                        const spans = document.querySelectorAll('span[dir="auto"]');
                        let caption = '';
                        for (const span of spans) {
                            const text = span.textContent || '';
                            if (text.startsWith(username) && text.length > username.length + 3) {
                                let remainder = text.substring(username.length);
                                remainder = remainder.replace(/^\\s*\\d+[smhdwy]\\s*/, '').trim();
                                if (remainder.length > 0) { caption = remainder; break; }
                            }
                        }
                        const timeEl = document.querySelector('time[datetime]');
                        const img = document.querySelector('article img[alt]:not([alt=""])') ||
                                    document.querySelector('main img[alt]:not([alt=""])');
                        return {
                            caption,
                            timestamp: timeEl ? timeEl.getAttribute('datetime') : '',
                            time_text: timeEl ? timeEl.textContent.trim() : '',
                            alt: img ? img.alt : '',
                            is_video: !!document.querySelector('video'),
                            top_comments: []
                        };
                    }''', post_url)
                    post_data['url'] = post_url
                    post_data['index'] = orig_i + 1
                    post_data['is_reel'] = '/reel/' in post_url
                    post_data['retried'] = True
                    posts.append(post_data)

                    if (idx + 1) % 5 == 0:
                        print(f"  {idx + 1}/{len(retry_queue)} retries done")

                except Exception as e:
                    posts.append({'url': post_url, 'index': orig_i + 1, 'error': str(e)})

        # Sort posts by index so they're in order
        posts.sort(key=lambda p: p.get('index', 999))

        await browser.close()

    # ── SAVE ──
    print("\nSaving...")
    for fname, data in [
        ("profile.json", profile),
        ("grid.json", grid_data),
        ("post_urls.json", post_urls),
        ("posts.json", posts),
    ]:
        with open(f"{out_dir}/{fname}", "w") as f:
            json.dump(data, f, indent=2)

    # ── OPTIONAL: TRANSCRIBE REELS ──
    reel_urls = [p['url'] for p in posts if p.get('is_reel') or p.get('is_video')]
    if transcribe_reels and reel_urls:
        print(f"\nDownloading + transcribing {len(reel_urls)} reels...")
        os.makedirs(f"{out_dir}/reels", exist_ok=True)
        for j, reel_url in enumerate(reel_urls):
            try:
                subprocess.run(
                    ["/opt/homebrew/bin/yt-dlp", "-f", "bestvideo[height<=720]+bestaudio/best",
                     "--cookies-from-browser", "chrome",
                     "-o", f"{out_dir}/reels/%(id)s.%(ext)s", reel_url],
                    capture_output=True, text=True, timeout=60
                )
                for fname in os.listdir(f"{out_dir}/reels"):
                    fpath = f"{out_dir}/reels/{fname}"
                    txt_path = fpath.rsplit('.', 1)[0] + '.txt'
                    if not os.path.exists(txt_path) and not fname.endswith('.txt'):
                        subprocess.run(["groq-transcribe", fpath],
                                       capture_output=True, text=True, timeout=120)
                if (j + 1) % 5 == 0:
                    print(f"  {j + 1}/{len(reel_urls)} reels done")
            except Exception as e:
                print(f"  Reel {j + 1} failed: {e}")

    # ── SUMMARY ──
    summary = {
        'handle': handle,
        'profile': profile,
        'total_posts': len(post_urls),
        'captions_scraped': len([p for p in posts if p.get('caption')]),
        'reels_detected': len(reel_urls),
        'output_dir': out_dir,
        'scraped_at': datetime.now().isoformat()
    }
    with open(f"{out_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*50}")
    print(f"  Done! @{handle}")
    print(f"  Posts: {len(post_urls)} | Captions: {summary['captions_scraped']} | Reels: {len(reel_urls)}")
    print(f"  Output: {out_dir}/")
    print(f"{'='*50}\n")
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scraper.py <handle> [--transcribe]")
        sys.exit(1)

    handle = sys.argv[1]
    transcribe = "--transcribe" in sys.argv
    asyncio.run(scrape_profile(handle, transcribe_reels=transcribe))
