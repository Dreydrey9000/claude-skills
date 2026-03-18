---
name: swipe-lab
description: Instagram carousel factory. Scrape your profile to extract your brand, study any creator's carousels for inspiration, then generate unlimited on-brand carousels. First run onboards you — after that, just say what you want. Triggers on "swipe lab", "make me a carousel", "carousel for", "make carousels", "generate slides", "new carousel", or any request to create Instagram carousel content.
---

# Swipe Lab — Carousel Content Factory

Your personal carousel factory. Scrape creators for inspiration → generate carousels in YOUR brand and voice.

## First Run — Onboarding

If no brand file exists at `~/.claude/skills/swipe-lab/brands/`, this is a new user. Run onboarding:

### Step 1: Get their brand

Ask: **"What's your Instagram handle?"**

Then scrape their profile to extract:
- Bio, name, handle
- Visual style (photo vs graphic ratio, color patterns, vibe)
- Content themes from recent posts
- Voice/tone from captions

Ask them to confirm or adjust:
- **"Here's what I found about your brand. Does this look right?"**
- Show: colors, voice description, content pillars, audience
- Let them tweak anything

### Step 2: Pick creators to study

Ask: **"Drop 1-3 Instagram handles of creators whose carousels you love."**

Scrape each creator's carousels:
- Screenshot every slide
- Extract topics, hooks, structures, content patterns
- Store in `~/.claude/skills/swipe-lab/knowledge/{handle}/`

### Step 3: Generate brand config

Create `~/.claude/skills/swipe-lab/brands/{handle}.json` using this structure:

```json
{
  "handle": "@theirhandle",
  "name": "Their Name",
  "businesses": ["Business 1", "Business 2"],
  "tagline": "Extracted or provided tagline",
  "niche": "Their niche in one sentence",
  "audience": "Who they serve",

  "brand_colors": {
    "primary_accent": "#hexcolor",
    "background_dark": "#0a0a0a",
    "background_light": "#ffffff",
    "text_dark": "#111111",
    "text_light": "#ffffff",
    "text_muted_dark": "#888888",
    "text_muted_light": "#666666",
    "bottom_bar": "#hexcolor"
  },

  "typography": {
    "font_family": "Inter",
    "heading_weight": "900",
    "body_weight": "400",
    "heading_size": "56px",
    "body_size": "28px"
  },

  "visual_style": {
    "aesthetic": "Description of their visual vibe",
    "layout": "How they lay out content",
    "bottom_bar": "Bottom bar style description"
  },

  "voice": {
    "tone": "Description of how they write",
    "reading_level": "Grade level",
    "phrases_to_use": ["phrase 1", "phrase 2"],
    "phrases_to_avoid": ["phrase 1", "phrase 2"],
    "content_pillars": ["pillar 1", "pillar 2", "pillar 3"]
  },

  "cta_patterns": {
    "dm_keywords": ["KEYWORD1", "KEYWORD2"],
    "format": "DM me \"{keyword}\" to get started.",
    "closing_line": "@handle | Business Name"
  },

  "carousel_defaults": {
    "ratio": "4:5 (1080x1350)",
    "accent_color": "#hexcolor",
    "slide_alternation": "How slides alternate (dark/white, all dark, etc)",
    "bottom_bar_height": "55px"
  },

  "inspiration_creators": ["@creator1", "@creator2"]
}
```

### Step 4: Confirm and go

**"You're set up. From now on, just say 'Swipe Lab' and tell me what you want."**

---

## Returning User — Normal Flow

If a brand file exists at `~/.claude/skills/swipe-lab/brands/`, load it and go.

If MULTIPLE brand files exist, ask: **"Which brand? [list handles]"** — or auto-detect from the current working directory / conversation context.

### Quick Start Examples

- **"Make me a carousel about [topic]"** → generates in their brand
- **"Swipe Lab — scrape @someone and make carousels from their topics"** → scrapes + generates
- **"Give me 5 carousels I can post this week"** → picks topics from knowledge base + generates
- **"[Theme name] carousel about [topic]"** → generates in specific theme
- **"Update my brand"** → re-scrape their profile, update brand.json
- **"Add @newcreator to my inspiration"** → scrape and add to knowledge base

---

## The 7 Themes

| Theme | Code Name | Vibe | Best For |
|-------|-----------|------|----------|
| **Sketch Pad** | `sketch` | Hand-drawn whiteboard, warm off-white, Caveat font | Explainers, breakdowns |
| **Dark Mode** | `dark` | Near-black, red accents, code blocks | Deep-dives, comparisons, bold statements |
| **Clean Sheet** | `clean` | White, blue accents, minimal | Step-by-step, lists, educational |
| **Gradient Wave** | `gradient` | Purple-blue gradient, frosted glass | Motivational, identity posts |
| **Black Card** | `blackcard` | Pure black, white text, NOTHING else | Hot takes, punchy opinions |
| **Apple Keynote** | `keynote` | Cinematic dark, glow effects, big numbers | Premium reveals, dramatic stats |
| **Neon** | `neon` | Dark charcoal, cyan/magenta/lime neon glow | Maximum visual interrupt |

**Theme selection:** Auto-pick based on content type unless the user specifies. Override the theme's default accent color with the user's brand accent color.

---

## How It Works

```
ONBOARDING (first time):
  User's IG handle → scrape profile → extract brand
  Creator handles → scrape carousels → extract knowledge
  → brand.json + knowledge base saved

SCRAPE MODE (anytime):
  IG handle → scrape_carousels.py → screenshot every slide
           → Claude reads screenshots → extracts knowledge + topics
           → stored in knowledge/{handle}/

GENERATE MODE (the main thing):
  Topic + Theme → load user's brand.json
                → pull inspiration from knowledge base (optional)
                → write slides in user's voice
                → generate HTML with user's brand colors/fonts
                → Playwright screenshots at 1080x1350
                → ready-to-post PNGs in output folder
```

---

## File Locations

All files live inside `~/.claude/skills/swipe-lab/`:

| What | Where |
|------|-------|
| This skill | `SKILL.md` |
| Brand configs | `brands/{handle}.json` (one per user) |
| Creator knowledge | `knowledge/{handle}/` (scraped carousels + extracted topics) |
| Scraper script | `scripts/scrape_carousels.py` |
| Renderer script | `scripts/render_carousel.py` |
| Theme configs | `templates/themes.json` |
| HTML templates | `templates/` |
| Generated output | `/tmp/carousel_output/` or user-specified path |

---

## Voice Rules (MANDATORY)

All carousel copy MUST sound like the user — not generic motivational content.

1. **Read their brand.json** — use their tone, phrases, reading level
2. **Match their content pillars** — don't go off-topic
3. **Use their phrases** — the ones listed in `phrases_to_use`
4. **Avoid their anti-phrases** — the ones in `phrases_to_avoid`
5. **Reality check:** Would this person actually post this? If it sounds like a template, rewrite it.

---

## Slide Design Rules

1. **4:5 ratio** (1080x1350) — takes up more feed space
2. **No slide count limits** — 3 slides or 15 slides. Content decides the length. Never pad, never cut short.
3. **Bottom bar on EVERY slide** — swipe teaser + slide counter + @handle
4. **Slide 1 stops the scroll** — big number, provocative question, or bold visual
5. **Use brand colors** — accent from brand.json, not theme defaults
6. **No empty space** — every pixel has a job
7. **Swipe teasers** — "it gets worse →", "here's the fix →", "my take →"

---

## Managing Multiple Brands

Swipe Lab supports multiple brand profiles. Each is a separate JSON in `brands/`.

- `brands/kclavier.json` — Kevin's brand
- `brands/itisdrey.json` — the user's brand
- `brands/someclient.json` — A client's brand

When generating, Claude checks:
1. If user specifies a brand: use that one
2. If only one brand exists: use it automatically
3. If multiple exist: ask which one

To add a new brand: **"Swipe Lab — set up a new brand for @handle"**
To switch brands: **"Swipe Lab — use @handle's brand"**
To remove a brand: **"Swipe Lab — remove @handle"**

---

## Playwright Reference (IMPORTANT — read before scraping or rendering)

### Scrape Instagram (with logged-in Chrome profile)

```python
from playwright.async_api import async_playwright
import asyncio, os

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=os.path.expanduser("~/Library/Caches/ms-playwright/mcp-chrome-profile"),
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await browser.new_page()
        await page.goto("https://www.instagram.com/someone/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        await page.screenshot(path="/tmp/screenshot.png")
        await browser.close()

asyncio.run(scrape())
```

**CRITICAL:** Always use `wait_until="domcontentloaded"` — NEVER `networkidle`. Instagram never finishes loading network requests, so `networkidle` will timeout every time.

### Render HTML slides to PNGs

```python
from playwright.async_api import async_playwright
import asyncio

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.goto("file:///path/to/slides.html", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        slides = await page.query_selector_all(".slide")
        for i, slide in enumerate(slides, 1):
            await slide.screenshot(path=f"/tmp/output/slide_{i}.png")
        await browser.close()

asyncio.run(render())
```

### Chrome profile location
`~/Library/Caches/ms-playwright/mcp-chrome-profile`

### If Instagram scraping fails
Session expired. Tell the user to re-login:
```bash
npx playwright open --user-data-dir ~/Library/Caches/ms-playwright/mcp-chrome-profile https://instagram.com
```
Log in, close the browser. Then scraping works again.

---

## Changelog
- [2026-03-17]: Generic Swipe Lab created. Multi-brand support, onboarding flow, 7 themes. Forked from Kevin Clavier's custom build.
