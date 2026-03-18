---
name: ig-profile-scraper
description: >
  Full Instagram profile scraper using Playwright. Reads EVERY post caption, detects reels,
  extracts bio/stats/themes, and builds a structured intelligence report. No API keys needed —
  uses logged-in Chrome profile. Input = Instagram handle or URL. Output = full profile report
  saved to /tmp/ig-intel/. Triggers: "scrape their IG", "read their profile", "ig intel",
  "profile scraper", "what does their Instagram say", "script their account", any Instagram URL
  for personal intelligence gathering.
---

## What This Is

One command. Full profile intelligence. No modes, no flags, no decisions.

```
Scrape @daniellesmith09
```

That's it. You get EVERYTHING: bio, stats, every post caption, reel detection, timestamps, alt text, screenshots. If reels exist and `--transcribe` is passed, those get downloaded and transcribed too — but that's the ONLY optional flag because downloading video files takes real time.

## Architecture

```
@handle
   │
   ▼
LOAD PROFILE (Playwright + Chrome profile)
  │  Screenshot + bio + stats + name + mutual followers
  ▼
SCROLL GRID (collect ALL post URLs)
  │  Scroll until no new posts load
  ▼
DRILL INTO EVERY POST (open each one, read full caption)
  │  ~3 sec/post with polite delays to avoid blocks
  │  Extract: caption, timestamp, type (photo/reel/carousel), alt text
  ▼
OUTPUT: /tmp/ig-intel/{handle}/
  ├── profile.json       (bio, stats, name)
  ├── posts.json         (every post with full caption)
  ├── post_urls.json     (all URLs)
  ├── grid.json          (thumbnail alt text)
  ├── screenshots/       (profile + grid)
  └── summary.json       (metadata)
```

**Optional:** Add `--transcribe` to also download reels and transcribe audio via groq-transcribe. This adds ~1-2 min per reel.

## How It Works (The 4 Walls + Solutions)

| Wall | Problem | Solution |
|------|---------|----------|
| Rate limiting | Instagram blocks rapid requests | 2-3 sec polite delay between posts |
| DOM changes | Class names change weekly | 4 fallback selectors per element |
| Auth/API bans | Private APIs get blocked | Playwright + YOUR Chrome session (looks like a real user) |
| Video content | No text in video posts | yt-dlp download + groq-transcribe |

## Dependencies

- Playwright MCP (already in pack — installed by quickstart.sh)
- yt-dlp (installed by quickstart.sh)
- groq SDK (installed by quickstart.sh) — only needed for `--transcribe`

## How to Use

Tell your agent any of these:
- "Scrape @username"
- "Script their whole account"
- "Read their IG profile"
- "What does their Instagram say about them?"

The agent uses Playwright MCP tools to:
1. Navigate to the profile using your logged-in Chrome
2. Screenshot the profile page
3. Extract bio, stats, name from the page
4. Scroll the grid to collect all post URLs
5. Open each post individually, read the full caption
6. Save everything to `/tmp/ig-intel/{handle}/`

## Step-by-Step (For the Agent)

1. `browser_navigate` to `https://www.instagram.com/{handle}/`
2. `browser_snapshot` to get profile data (name, bio, stats)
3. `browser_take_screenshot` for visual record
4. Scroll grid: `browser_evaluate` with `window.scrollTo(0, document.body.scrollHeight)` — repeat until no new posts load
5. Collect all post links: `browser_evaluate` with `document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')`
6. For EACH post URL:
   - `browser_navigate` to the post
   - `browser_snapshot` to extract caption text
   - Wait 2-3 seconds (polite delay)
   - Record: caption, timestamp, post type, alt text
7. Save all data to `/tmp/ig-intel/{handle}/`
8. Present structured intelligence report

## No Half Measures Rule

When this skill fires, you open EVERY post. Not 12. Not "a sample." ALL of them.
If there are 63 posts, you open 63 posts. If there are 200, you open 200.
The whole point is COMPLETE data, not inferred guesses from alt text.
