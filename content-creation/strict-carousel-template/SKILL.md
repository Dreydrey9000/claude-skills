---
name: strict-carousel-template
description: Create strict Instagram carousel templates from reels/transcripts and render 1080x1350 slides. Use when the user wants near-verbatim slide copy, a reusable carousel template, or asks to "run this" into carousel images. Always convert written number words to digits (for example, "seven" to "7", "twenty one" to "21").
---

# Strict Carousel Template

Build near-verbatim Instagram carousels from transcript text and export post-ready slides.

## Workflow

1. Gather transcript text or a prepared slide list.
2. Keep wording strict (minimal rewriting).
3. Convert number words to digits on every slide.
4. Export 4:5 images (`1080x1350`) with centered readable text.

## Run the Template

Use the bundled script:

```bash
/opt/homebrew/bin/python3.13 scripts/render_strict_carousel.py \
  --transcript-file /absolute/path/transcript.txt \
  --output-dir /absolute/path/output-folder \
  --slide-count 10
```

Use a prewritten slide list (one slide per line):

```bash
/opt/homebrew/bin/python3.13 scripts/render_strict_carousel.py \
  --slides-file /absolute/path/slides.txt \
  --output-dir /absolute/path/output-folder
```

## Output

- `01.png ... NN.png` (carousel images)
- `slides.final.txt` (final slide copy with digit conversion applied)

## Non-Negotiables

- Keep transcript language strict unless user asks for rewriting.
- Convert all number words to digits before rendering.
- Keep high-contrast, centered text for mobile readability.
