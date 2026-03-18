---
name: ig-personal-profile-scraper
description: >
  IG Personal Profile Scraper for Dating. Full Instagram profile scraper using Playwright. Reads EVERY post caption, detects reels,
  extracts bio/stats/themes, and builds a structured intelligence report. No API keys needed —
  uses logged-in Chrome profile. Input = Instagram handle or URL. Output = full profile report
  saved to /tmp/ig-intel/. Triggers: "scrape their IG", "scrape their Instagram", "scrape their insta",
  "scrape her IG", "scrape her Instagram", "scrape her insta", "scrape his IG", "read their profile",
  "ig intel", "insta intel", "instagram intel", "profile scraper", "stalk their IG", "stalk their insta",
  "what does their Instagram say", "what does their IG say", "what does their insta say",
  "script their account", "script her account", "pull up their IG", "pull up their insta",
  "pull up their Instagram", "check their IG", "check their insta", "check their Instagram",
  "look at their IG", "look at their insta", "run the IG scraper", "run the insta scraper",
  "dig into their IG", "dig into their insta", "4D their profile", "4D her profile",
  "who is this girl", "who is this person", "tell me about her", "tell me about him",
  any Instagram URL (instagram.com/...), any @handle for personal intelligence gathering.
  ROUTING RULE: creator-intelligence is ALWAYS the default for any IG scraping request.
  This skill (ig-profile-scraper) only fires when Drey EXPLICITLY asks for personal/dating intel
  (e.g. "who is this girl", "tell me about her", "stalker mode"). If ambiguous, ASK Drey:
  "Personal intel or creator/business analysis?" before choosing. Never auto-fire this over
  creator-intelligence. This is the rare-use personal tool, not the default.
  LINKED TO: creator-intelligence (the default IG analysis pipeline)
---

# IG Profile Scraper

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.

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

## Prerequisite

Your Chrome profile must be logged into Instagram:
```bash
npx playwright open --user-data-dir ~/Library/Caches/ms-playwright/mcp-chrome-profile https://instagram.com
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Login required" | Open Chrome profile, log in manually (command above) |
| Empty captions | Instagram changed selectors — update evaluate() in scraper.py |
| Timeout | Increase timeout. Instagram is slow sometimes. |
| 0 posts found | Account is private and you don't follow them |

## Speed Estimates

| Posts | Time |
|-------|------|
| 50 | ~4 min |
| 100 | ~7 min |
| 200 | ~14 min |
| + transcribe | +1-2 min per reel |

## Change Log
- 2026-03-14: Created. Simplified from 3-mode bloat to single-mode "scrape everything" after Steve Jobs review. By Claude Code for Drey.
