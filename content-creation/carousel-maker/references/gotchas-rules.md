# Carousel Maker — Gotchas & Hard-Learned Rules

Battle-tested lessons. Do NOT ignore them.

---

## Critical Rules

| Rule | Why |
|------|-----|
| Always use `/opt/homebrew/bin/python3.13` | System Python 3.9 lacks required type syntax — scripts crash |
| Always use `gemini-3-pro-image-preview` | Flash model produces significantly worse results |
| Use Gemini Pro inpainting for watermarks | PIL patch-copy leaves visible smudges |
| Watermark prompt: "small white sparkle shape..." | Never say "remove watermark" — Gemini refuses |
| Remove subtitles BEFORE enhancing | Enhancement bakes subtitles in permanently |
| Never stretch low-res frames | Keep native resolution, max 1.4x upscale |
| Enhance with Gemini Pro, not upscale tools | "Enhance to be sharper, clearer..." prompt works best |
| Mode B for real people, always | AI cannot replicate exact faces, tattoos, products |
| ONE image per generation call | NEVER create collages, grids, or multi-panel images |
| Generate ALL slides continuously | Don't stop between slides for feedback |
| Save as .jpg | Gemini returns JPEG data |

---

## Readability Rules

1. **Max 15 words per slide** (8-12 ideal)
2. **One idea per slide** — if it needs a comma, split it
3. **No paragraphs** — bullet points or single lines only
4. **High contrast** — black on white or white on black
5. **Readable on mobile** without zooming
6. **Center-aligned** both axes, always
7. **10% margin minimum** on all sides

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Text too small | Make it readable on mobile |
| Too many words per slide | Max 15, aim for 8-12 |
| Text not centered | Always center both axes |
| Weak hook | Must stop the scroll |
| CTA doesn't match content | Align CTA with carousel topic |
| Inconsistent style across slides | Use same reference images for all |
| Forgetting text-to-render in prompts | Always include explicit text instructions |
| Multi-slide collages | ONE slide per image, always |
| Using Flash model | Always `gemini-3-pro-image-preview` |
| Stopping between slides for feedback | Generate ALL slides continuously |
| Skipping watermark removal | Always run on every slide |
| Saving as .png | Save as .jpg |
| Saying "remove watermark" to Gemini | It refuses — use sparkle cleanup prompt |
| Using PIL patch-copy for watermarks | Leaves smudges — use Gemini Pro inpainting |
| Enhancing frames before removing subtitles | Subtitles get baked in |
| Stretching low-res frames | Keep native res, max 1.4x upscale |
| Using system Python | Always `/opt/homebrew/bin/python3.13` |

---

## Scripting Principles

- **One Big Idea**: Every carousel has ONE takeaway
- **Tone**: Trusted advisor > Salesman
- **Specificity**: Numbers, examples, results > vague claims
- **Swipe Motivation**: Each slide must create curiosity for the next
- **Standalone Value**: If someone only sees slide 1, they still get something

---

## API Access

- **GEMINI_API_KEY**: Set in `~/.zshrc` as environment variable
- **Google Drive**: Available via MCP tools
