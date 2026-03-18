---
name: image-generation
description: >
  Image generation mega skill for all AI image creation. Supports Nano Banana Pro (Gemini API),
  Higgsfield Soul ID, and reference-image workflows. Three modes: generate (from scratch),
  reference (match a screenshot's style), style-lock (use a saved client style config).
  Client style configs for Claudia, Ryan Magin, and all Viral Editz clients. Every video script
  gets image gen + video gen prompts for clone era. Triggers: "generate image", "make an image",
  "create a photo", "thumbnail", "style like", "match this style", "Claudia style", "podcast
  photo", image request for any client, reference image dropped, "nano banana", "gemini image".
---

# Image Generation Mega Skill

## Models Supported

| Model | Access Method | Best For | Resolution |
|-------|-------------|----------|------------|
| **Nano Banana Pro** | Gemini API (`gemini-3-pro-image-preview`) via Claude Code | Daily image gen, client content, thumbnails | 1K-4K |
| **Higgsfield Soul** | Higgsfield web UI | Character consistency (Soul ID trained) | Up to 2K |
| **Higgsfield Soul ID** | Higgsfield web UI | Training persistent characters | N/A (training) |
| **Flux** | Higgsfield web UI | Alternative aesthetics | Up to 2K |

**Default: Nano Banana Pro via Gemini API** — this is what we use in Claude Code.

---

## Three Modes

### Mode 1: GENERATE (From Scratch)

Create an image from a text description. No reference needed.

**When to use:** Client needs a new image for a scene that doesn't exist yet.

**Prompt Formula (Nano Banana Pro):**
```
[Identity Anchor] + [Scene Description] + [Wardrobe] + [Action/Pose] +
[Lighting] + [Background] + [Framing] + [Style/Mood]
```

**The Six Variables (Higgsfield Official):**
1. **Subject** — Who/what specifically (not generic)
2. **Composition** — Camera angle, lens, framing
3. **Action** — What's happening (movement, gesture, expression)
4. **Location** — Where, with atmospheric detail
5. **Style** — Art direction (cinematic, editorial, raw UGC, etc.)
6. **Negative guidance** — What to exclude (blur, artifacts, distortion)

### Mode 2: REFERENCE (Match a Screenshot)

User drops a reference image. Extract its DNA and recreate for a different subject.

**When to use:** "I want this same vibe/composition/style but for [different person/scene]"

**Process:**
1. Read the reference image visually
2. Extract: composition, camera angle, lighting setup, color palette, mood, wardrobe style, background, framing
3. Rebuild as a prompt with the new subject inserted
4. Ask user: "Keep everything or change something?"
5. Generate

**Extraction Template:**
```markdown
### Mode 3: STYLE-LOCK (Saved Client Style)

Use a pre-configured client style. Just describe the scene — the style is already defined.

**When to use:** "Give me another Claudia podcast shot" or "Ryan style thumbnail"

**Process:**
1. Load client config from `configs/[client].md`
2. User only needs to describe: scene, pose, wardrobe change (if any)
3. Config provides: lighting, background, camera, mood, framing, identity anchor
4. Merge and generate

---

### Core Pattern
```python
import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Text-to-image
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="9:16",  # Vertical for reels
            image_size="2K"       # Quality
        ),
    ),
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.jpg")  # ALWAYS .jpg — Gemini returns JPEG
```

### Multi-Turn Refinement (Chat Mode)
```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K"
        ),
    )
)

# First generation
response = chat.send_message(["Generate...", ref_img])
# Save image...

# Refine
response = chat.send_message("Make the lighting warmer and add more bokeh")
# Save refined image...
```

### CRITICAL: File Format
Gemini returns JPEG. Always save as `.jpg`. Saving as `.png` creates a JPEG with a PNG extension and causes downstream errors.

```python
# CORRECT
image.save("output.jpg")

# WRONG
image.save("output.png")  # JPEG data with PNG extension!

# If you NEED PNG:
image.save("output.png", format="PNG")
```

---

## Prompt Engineering (Nano Banana Pro Specific)

### Seed Locking
Reuse successful seeds for series consistency. When you get a good result,
note the conversation context — multi-turn chat preserves the style.

## Identity Anchor Pattern (For Character Consistency)

When generating images of a known character (Claudia, Ryan, etc.), always start with:

```
"Generate a new photorealistic image of THIS EXACT [PERSON] from the reference photos.
[He/She] must have the SAME face, same [hair description], same facial features,
same bone structure. NEW SCENE: [scene description]"
```

This is the proven pattern from Claudia's generations. Upload the CANON reference image
alongside this prompt.

## Client Style Configs

Each client gets a config file at `configs/[name].md` that defines their locked style.

## Tattoo Handling (For Characters With Tattoos)

### Soul ID (Best Method)
Upload 15-20 photos with tattoos clearly visible. Soul ID bakes them into the identity.
Placement stays consistent. Fine detail varies but presence is maintained.

## Higgsfield Prompting Guide (When Using Web UI)

### Nano Banana Pro (via Higgsfield)
Same as Gemini API prompting but through the Higgsfield web interface.
Select "Nano Banana Pro" model in the image creation dashboard.

### Soul Model (Higgsfield's Own)
Better for fashion-grade, editorial aesthetic.
Select "Higgsfield Soul" in model dropdown.


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-13]: Context Diet — split 429 lines into routing card (195 lines) + references/full-details.md (273 lines). Zero content deleted. By skill-diet.py.

- 2026-02-06: Created. Source: Luis Carrillo session. Consolidates Nano Banana Pro (Gemini API), Higgsfield Soul/Soul ID, and reference image workflows into one skill. Client configs for Claudia (proven podcast style). Tattoo handling documented. Mandatory video script image+video gen prompts for clone era.
