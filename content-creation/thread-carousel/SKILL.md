---
name: thread-carousel
description: This skill should be used when creating Twitter/X thread-style Instagram carousels. Type a topic and get a fully rendered carousel with profile pics, verified badges, word-wrapped text, emoji support, and embedded images.
---

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.
**Quality Gates:** Follow `~/.claude/skills/_shared/quality-gates.md` for ALL quality checks.

# Thread Carousel Generator

Generate Twitter/X thread-style Instagram carousels from a topic, thread text, or screenshots.

## How It Works

1. You provide a **topic**, paste a **thread**, share **screenshots**, or link to a **reel/video**
2. Claude **verifies the actual source content** (screenshot, transcript, NOT just captions)
3. Claude researches the topic and writes a thread (hook → body → CTA)
4. Claude finds images via search, screenshots, or AI generation
5. Claude builds a `config.json` with all slide data
6. The Python renderer generates 1080x1350 PNG slides

## Quick Start

```
/thread-carousel [topic or thread text]
```

## Profile Config (in CLAUDE.md or provided inline)

```
Thread Carousel Profile:
- Display Name: Luis Carrillo
- Handle: @itsluisc
- Verified: true
- Headshot: ~/.claude/skills/thread-carousel/assets/headshot.png
```

## Thread Structure

Every thread follows this format:

| Position | Type | Rule |
|----------|------|------|
| Tweet 1 | **Hook** | Attention-grabbing. ALWAYS gets its own slide + image |
| Tweets 2-N | **Body** | Core content. Facts, insights, examples |
| Last Tweet | **CTA** | Call to action. Follow, save, share |

## Slide Combination Logic

| Condition | Action |
|-----------|--------|
| First tweet | Own slide + hook image (REQUIRED) |
| Tweet has image | Own slide |
| Tweet > 200 characters | Own slide |
| Two consecutive tweets < 150 chars, no images | Combine onto one slide with gray divider |
| Otherwise | Own slide, text centered |

## Image Priority (in order)

1. **User-provided images** — always use these first
2. **Tavily/web search** — find relevant images online
3. **Live screenshots** — Python script to screenshot a website
4. **AI-generated** — use Gemini/Nano Banana for illustrations

## Rendering

```bash
/opt/homebrew/bin/python3.13 ~/.claude/skills/thread-carousel/scripts/render_carousel.py config.json
```

## Themes

| Theme | Background | Text | Vibe |
|-------|-----------|------|------|
| `dark` | #15202B | #E7E9EA | Twitter/X dark mode |
| `light` | #FFFFFF | #0F1419 | Twitter/X light mode |
| `black` | #000000 | #E7E9EA | AMOLED dark |

## Step-by-Step Workflow

### 1. Create workspace

```bash
mkdir -p ~/Desktop/workspace/carousels/$(date +%Y-%m-%d)/{slug}/references
```

### 2. Research topic (if needed)

Use Tavily or web search to gather facts, stats, and talking points.

### 3. Write the thread

- Hook: Pattern interrupt, bold claim, or surprising stat
- Body: 4-6 tweets with insights, each ~100-250 characters
- CTA: Clear ask (follow, save, share, link)

### 4. Find images

For the hook slide (REQUIRED) and 2-3 body slides:
- Search web for relevant screenshots/graphics
- Download to `references/` folder
- Use descriptive filenames

### 5. Build config.json

Apply the slide combination logic. Write the full config.

### 6. Render

```bash
/opt/homebrew/bin/python3.13 ~/.claude/skills/thread-carousel/scripts/render_carousel.py ~/Desktop/workspace/carousels/$(date +%Y-%m-%d)/{slug}/config.json
```

### 7. Review and iterate

Open the slides. If changes needed:
- Swap images: update config.json image paths, re-render
- Edit text: update config.json tweet text, re-render
- Add images: download new ones to references/, update config, re-render

## Dependencies

```
Pillow >= 12.0
pilmoji >= 2.0
```

Fonts: SF Pro Display Bold + Regular (`~/Library/Fonts/SFPRODISPLAYBOLD.OTF`)

## Assets

| Asset | Path |
|-------|------|
| Luis headshot | `~/.claude/skills/thread-carousel/assets/headshot.png` |
| Render script | `~/.claude/skills/thread-carousel/scripts/render_carousel.py` |


## Trust Enforcement (Inherited — Global Law, Mar 16, 2026)

| Pillar | Rule |
|--------|------|
| **Verify Before Claim** | Tool call before stating facts. Never answer from memory alone. |
| **Data Accuracy** | All handles, URLs, IDs from source files ONLY. Never fabricate. |
| **Complete The Ask** | Do EVERYTHING the user asked. All items. Not just the first one. |
| **Show Your Work** | Open Kitchen — show every step as it happens. No black boxes. |
| **Source Everything** | Cite where information comes from. |
| **Internet-First** | Fetch official docs before advising on any tool/API. |

Enforcement: `trust-guardian.js` hook + `quality-gates.md` Trust Gate. Full: `~/.claude/skills/trust/SKILL.md`

## Gate Protocol
- **Pre-flight:** Verify content brief or topic is defined. Check target platform and format requirements. Load relevant clone/brand voice if client-specific.
- **Mid-flight:** Every piece must have a clear hook, one core message, and a call to action. Check against viral reference patterns.
- **Post-flight:** Run CUB test (Clear, Believable, Works). Verify output matches requested format. Check for brand voice consistency.

## Sources
- Source: Claude Code skills system — original skill creation.

---

## AI AGENT READINESS UPGRADE (10/10)

### Gate 7: Triggers (Clear & Complete)

**Slash Commands:**
- `/thread-carousel`
- `/carousel`
- `/tc`

**Keyword Triggers (any of these = activate this skill):**
- "make a carousel"
- "create a carousel"
- "thread carousel"
- "twitter thread carousel"
- "instagram carousel"
- "turn this into slides"
- "make slides from"
- "carousel from this reel"
- "carousel from this thread"
- "render carousel"

**Context Triggers (activate automatically):**
- User pastes a numbered list of tweets/posts → detect thread format → activate
- User shares IG reel URL + says "carousel" or "slides" → activate
- User shares YouTube URL + says "carousel" or "slides" → activate

---


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-09]: Context Diet — split 590 lines into routing card (185 lines) + references/full-details.md (433 lines). Zero content deleted. By skill-diet.py.
- [2026-03-02]: AI Agent Readiness upgrade — scored 3/10, upgraded to 10/10. Added: decision trees for source routing/image priority/render failures/profile config, typed I/O schema, 8 boolean success criteria, agent-executable steps table, self-contained context/dependency checks, 12-row error handling table, full trigger list (slash + keyword + context), handoff labels (AUTONOMOUS/INFORM/APPROVAL-REQUIRED) for all 10 steps, exact tool call syntax for all tools, 10-step blocking execution order. By Agent Luis.
- [2026-03-02]: War Room Tier 2 — content quality upgrade (gate→content).
- [2026-03-02]: War Room Tier 1 audit — skill structure verified and standardized.
