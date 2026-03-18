# Carousel Maker — Styles & Templates

---

## 6 Carousel Formats

| # | Format | Hook Pattern | Best For |
|---|--------|-------------|----------|
| 1 | The List | "[Number] [Things] that [Result]" | Educational, high saves |
| 2 | Myth-Bust | "You've been told X. Here's the truth." | Contrarian, high comments |
| 3 | Before/After | "I used to... Now I..." | Transformation, high shares |
| 4 | Story Arc | "This one decision changed everything." | Narrative, high watch time |
| 5 | Framework Reveal | "The [Number]-Step System for [Result]" | Authority, high follows |
| 6 | Hot Take | "Unpopular opinion: X is wrong." | Debate, high engagement |

---

## 7 Visual Styles

| # | Style | Description |
|---|-------|-------------|
| 1 | Cards Against Humanity | Stark white card, thick black border, bold Helvetica, max 10 words |
| 2 | iPhone Text Messages | iOS message bubble interface, blue/gray bubbles, authentic UI |
| 3 | Editorial Illustration | Hand-drawn ink, New Yorker aesthetic, cross-hatching |
| 4 | Handwritten Whiteboard | Multi-colored markers, yellow highlighter, slightly imperfect |
| 5 | Custom / Brand Match | User uploads reference image, clone the exact vibe |
| 6 | Specific Reference | User names a movie, show, creator, or aesthetic |
| 7 | Screenshot + Annotation (Mode B) | Real frames enhanced with text overlays, arrows, highlights |
| 8 | Keynote (Luis Carrillo Original) | Black bg (#000), Inter 800, Apple accent colors, one idea per slide, Jobs story arc |

---

## Hook Templates by Format

| Format | Hook Examples |
|--------|-------------|
| List | "[Number] [Things] that [Result]", "Stop doing [X]. Do [Y] instead." |
| Myth-Bust | "You've been lied to about [Topic]", "[Common Belief] is completely wrong" |
| Before/After | "[Time] ago, I [Problem]. Now I [Result]." |
| Story Arc | "This one [decision] changed everything" |
| Framework | "The [Number]-Step System for [Result]" |
| Hot Take | "Unpopular opinion: [Contrarian Statement]" |

---

## Slide Structure (8-10 slides)

| Slide | Purpose | Notes |
|-------|---------|-------|
| 1 | HOOK | Pattern interrupt, one line, bold, creates curiosity |
| 2-3 | SETUP | Establish the problem or context |
| 4-7 | VALUE | The meat — framework, list items, story beats |
| 8-9 | PAYOFF | Resolution, summary, or proof |
| 10 | CTA | Exactly as selected |

### Slide Plan Format
```
Slide 1 (Hook)
Text: [Hook — max 10 words]
Visual: [Description of the image composition]

Slide 2 (Setup)
Text: [Max 15 words]
Visual: [Description]

[Continue for all slides...]
```

---

## 5 CTA Options (Final Slide)

| # | CTA Type | Example |
|---|----------|---------|
| 1 | DM Automation | "DM me [WORD] for [Asset]" |
| 2 | Comment Automation | "Comment [WORD] for [Asset]" |
| 3 | Follow CTA | "Follow @[Handle] for more [Topic]" |
| 4 | Discussion | Ask a question to spark debate |
| 5 | Save CTA | "Save this for later" |

---

## Style 8: Keynote (Luis Carrillo Original)

**The Steve Jobs carousel.** Black background, massive typography, one idea per slide. Every slide is a full-screen statement.

### Design Rules
```
Background:  #000000 (ALWAYS pure black)
Font:        Inter, weight 800 for hero, 400 for sub
Colors:      white (#fff), gray (#86868b), blue (#2997ff), green (#30d158),
             purple (#bf5af2), orange (#ff9f0a), red (#ff453a)
Alignment:   Center (both axes)
Max words:   10 per slide (even fewer than standard carousels)
One rule:    ONE idea per slide. No exceptions.
```

### Keynote Story Arc (Carousel Format)
```
Slide 1 (Hook):     THE PROBLEM — massive text, make them FEEL it
Slide 2 (Tension):  Old way (red) vs New way (green) — contrast
Slide 3 (Reveal):   Your solution — gradient text (blue→purple), "Introducing..."
Slide 4-5 (How):    Three steps MAX — numbered, simple language
Slide 6 (Proof):    One real example with real numbers
Slide 7 (Numbers):  3-4 massive stats, nothing else on screen
Slide 8 (Magic):    The "wow" — short sentences stacking
Slide 9 (Close):    Tagline + CTA
```

### Generation Method
When using Keynote style: generate each slide as a **4:5 portrait HTML div** rendered to PNG. Do NOT use Gemini — render directly from the design system CSS. Each slide = standalone downloadable image.

### Cross-Reference
Full design system: `/keynote-generator/references/design-system.md`
Gold standard HTML: `/keynote-generator/references/gold-standard-keynote.html`

---

## Reference Image System

### How References Work

1. **Character Reference** — Photo of person to feature. Ask user on first use. Store as `references/characters/[name].jpg`
2. **Aesthetic Reference** — Screenshot or image showing visual style to match. Can come from video, existing carousel, or named brand.
3. **Mixing** — Combine any character with any aesthetic. Example: "Ryan Magin's content + Modern Wisdom's aesthetic"

When generating with references, use `compose_images.py` to pass reference images + slide prompt together.
