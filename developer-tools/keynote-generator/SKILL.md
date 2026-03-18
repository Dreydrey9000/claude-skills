---
name: keynote-generator
description: >
  Generate Steve Jobs-style keynote presentations as single-file HTML. Full-screen scroll-driven slides,
  black background, massive typography, fade-in animations, zero clutter. Story arc: Problem → Tension →
  Reveal → How It Works → Demo → Proof → Numbers → One More Thing → Close. Triggers: "keynote",
  "presentation", "pitch deck", "present this", "Steve Jobs style", "make a deck", "show this to [person]",
  "explain this visually", "Taco Bell keynote style".
---

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.
**Quality Gates:** Follow `~/.claude/skills/_shared/quality-gates.md` for ALL quality checks.
**Layer:** Surface (Output / Deliverables)

# Keynote Generator — Steve Jobs Presentation Style

Generate scroll-driven HTML keynote presentations. One idea per screen. Massive text. Zero bullet points. Story-driven.

## References

| File | Contents |
|------|----------|
| `references/gold-standard-keynote.html` | **THE TEMPLATE** — Clone Architecture keynote. Copy this design system exactly. |
| `references/design-system.md` | Colors, typography, components, slide types extracted from gold standard |

## The Story Arc (MANDATORY — Every Keynote Follows This)

```
1. THE PROBLEM     → One sentence. Massive text. Make them FEEL it.
2. THE TENSION     → Old way (red, painful) vs New way (green, magical)
3. THE REVEAL      → Product/concept name. Gradient text. "Introducing..."
4. HOW IT WORKS    → Three steps MAX. Numbered cards. Simple language.
5. THE DEMO        → Terminal mockup, screenshot, or live example.
6. THE ANATOMY     → Layers/components. Emoji + name + one-line description.
7. THE PROOF       → Real example with real numbers. Stats row.
8. THE NUMBERS     → 3-4 massive stats. Nothing else on the screen.
9. THE MAGIC       → The "wow" moment. Short sentences stacking on each other.
10. ONE MORE THING → Surprise feature. Jobs signature move.
11. THE CLOSE      → Tagline. Name. Done.
```

Not every keynote needs all 11. Minimum: Problem → Reveal → How → Proof → Close (5 slides).

## Design System (Copy EXACTLY)

### Colors
```css
:root {
  --black: #000000;     /* background — ALWAYS black */
  --white: #ffffff;     /* primary text */
  --gray: #86868b;      /* secondary text, subtitles */
  --blue: #2997ff;      /* tech, innovation, links */
  --green: #30d158;     /* success, solution, money */
  --purple: #bf5af2;    /* premium, creative, reveal */
  --orange: #ff9f0a;    /* warning, attention, energy */
  --red: #ff453a;       /* problem, pain, old way */
}
```

### Typography
```css
font-family: 'Inter', -apple-system, 'Helvetica Neue', sans-serif;
-webkit-font-smoothing: antialiased;

.hero-text    → clamp(48px, 8vw, 96px), weight 800, letter-spacing -3px
.sub-hero     → clamp(20px, 3vw, 32px), weight 400, color var(--gray)
.section-label → 14px, weight 600, uppercase, letter-spacing 4px, color var(--gray)
.quote        → clamp(24px, 4vw, 42px), weight 300, italic, color var(--gray)
```

### Slide Structure
```html
<div class="slide" data-label="Label">
  <div class="fade-in">
    <!-- ONE idea here. That's it. -->
  </div>
</div>
```
Every slide: `min-height: 100vh`, flex center, `padding: 60px 40px`, `text-align: center`.

### Component Library

| Component | When to Use | Key Classes |
|-----------|-------------|-------------|
| **Hero text** | Main statement per slide | `.hero-text` + `.accent-[color]` |
| **Sub-hero** | Supporting context (1-2 lines max) | `.sub-hero` |
| **Section label** | Tiny category above hero ("How it works") | `.section-label` |
| **VS container** | Old way vs New way comparison | `.vs-container` > `.vs-side.old` + `.vs-side.new` |
| **Steps row** | 2-3 numbered steps | `.steps-row` > `.step-card` with `.step-num` |
| **Stats row** | 3-4 massive numbers | `.stats-row` > `.stat-item` |
| **Layer stack** | Vertical list with emoji | `.layer-stack` > `.layer-row` |
| **Demo terminal** | Fake CLI/code demo | `.demo-terminal` with traffic light dots |
| **Quote** | Someone's words | `.quote` + `.quote-author` |
| **Gradient text** | The big reveal moment | `.accent-gradient` |

### Animations + Navigation
```javascript
// Scroll-driven fade-in (IntersectionObserver, threshold 0.15)
// Nav dots: fixed right side, one per slide, click to scroll
// All in the gold-standard reference — copy the <script> block exactly
```

## Interactive Decision Points

### 1. What Are You Presenting?

Ask the user:
- **Question:** "What's the keynote about?"
- **Options:**
  - "A product/system I built (Recommended)" — Problem → Solution → Demo → Numbers
  - "A concept/framework" — Insight → Architecture → Examples → Implications
  - "A pitch to a client" — Their pain → Our solution → Proof → Pricing
  - "A tutorial/explainer" — Question → Steps → Demo → Recap

### 2. How Many Slides?

Ask the user:
- **Question:** "How deep should the presentation go?"
- **Options:**
  - "Quick pitch (5 slides) (Recommended)" — Problem → Reveal → How → Proof → Close
  - "Full keynote (8-12 slides)" — Complete story arc with demo and one-more-thing
  - "Single wow slide" — One full-screen statement with massive text

## Rules

1. **ONE idea per slide.** If you need a second idea, make a second slide.
2. **Black background ALWAYS.** No white backgrounds. No gray. Pure #000000.
3. **No bullet points.** Ever. Use short sentences, comparisons, or numbers.
4. **No feature lists.** Tell a story. Show don't tell.
5. **Max 3 sentences per slide.** If you're writing paragraphs, you're doing it wrong.
6. **Hero text = the FEELING.** Sub-hero = the context. Never reverse this.
7. **Numbers stand alone.** When showing stats, let them breathe. Nothing else on screen.
8. **The demo is everything.** One real example > ten descriptions.
9. **Gradient text = ONE moment.** The product reveal. Don't overuse it.
10. **"One more thing" is optional** but powerful. Only use when there's a genuine surprise.

## Output

Single HTML file. Self-contained. No external dependencies except Google Fonts (Inter). Save to `~/Desktop/[topic]-keynote.html` and open in browser.

## Gold Standard

The Clone Architecture keynote (`references/gold-standard-keynote.html`) is the template. When in doubt, match that file's structure, style, and pacing exactly.

**Luis's reaction:** "this keynote is mad clean" — that's the bar. Every keynote generated must hit that bar.

## Gate Protocol
- **Pre-flight:** Verify content brief or topic is defined. Check target platform and format requirements. Load relevant clone/brand voice if client-specific.
- **Mid-flight:** Every piece must have a clear hook, one core message, and a call to action. Check against viral reference patterns.
- **Post-flight:** Run CUB test (Clear, Believable, Works). Verify output matches requested format. Check for brand voice consistency.

## Sources
- Source: Claude Code skills system — original skill creation.

## Change Log
- [2026-03-02]: War Room Tier 2 — content quality upgrade (gate→content).
- [2026-03-02]: War Room Tier 1 audit — skill structure verified and standardized.
- [2026-03-12]: Fixed shared tool-stack and quality-gates references to exact file paths. Added layer tag (Surface).
