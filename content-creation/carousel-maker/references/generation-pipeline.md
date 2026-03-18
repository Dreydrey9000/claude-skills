# Carousel Maker — Generation Pipeline

Scripts base path: `~/.claude/plugins/cache/every-marketplace/compound-engineering/2.28.0/skills/gemini-imagegen/scripts`

---

## Mode A Pipeline (AI-Generated, Styles 1-6)

### Phase A: Generate All Slides

For EACH slide, generate ONE image at a time:

```bash
SCRIPTS="~/.claude/plugins/cache/every-marketplace/compound-engineering/2.28.0/skills/gemini-imagegen/scripts"

# Without reference images (styles 1-4):
/opt/homebrew/bin/python3.13 "$SCRIPTS/generate_image.py" "[full prompt with text-to-render instruction]" "output.jpg" --model gemini-3-pro-image-preview --aspect [ratio]

# With reference images (styles 5-6, or with character reference):
/opt/homebrew/bin/python3.13 "$SCRIPTS/compose_images.py" "[full prompt with text-to-render instruction]" "output.jpg" character_ref.jpg aesthetic_ref.jpg --model gemini-3-pro-image-preview
```

**Rules:**
- ONE image per generation call. NEVER create collages, grids, or multi-panel images.
- Each image = exactly ONE carousel slide filling the ENTIRE canvas.
- Generate ALL slides without stopping for feedback between slides.
- Always include explicit text-to-render instructions in every prompt.
- All text must be CENTER-ALIGNED, vertically and horizontally.

### Phase B: Watermark Removal

After ALL slides generated, run each through Gemini Pro inpainting:

```bash
/opt/homebrew/bin/python3.13 "$SCRIPTS/edit_image.py" "input.jpg" \
  "Clean up the bottom-right corner of this image. There is a small white sparkle shape that should be replaced with the surrounding paper texture to match the rest of the background." \
  "output.jpg" --model gemini-3-pro-image-preview
```

### Phase C: Rename & Organize

Output folder: `~/Downloads/[carousel-name]/clean/`

File naming: `[number] - [Carousel Title].jpg`

### Phase D: Verification

1. Crop bottom-right corner (120x120px) of every image
2. Visually verify no watermark sparkle remains
3. View each full image to confirm content integrity
4. Present results to user

---

## Mode B Pipeline (Screenshot-Based, Style 7)

### Phase A: Frame Extraction

```bash
# Single frame at specific timestamp
ffmpeg -ss [HH:MM:SS] -i "video.mp4" -frames:v 1 -q:v 2 "frame_01.jpg"

# Multiple frames at intervals
ffmpeg -i "video.mp4" -vf "fps=1/5" -q:v 2 "frames/frame_%03d.jpg"
```

Select frames that best represent each slide's content. Match timestamps to transcript.

### Phase B: Subtitle Removal (BEFORE Enhancement)

```bash
SCRIPTS="~/.claude/plugins/cache/every-marketplace/compound-engineering/2.28.0/skills/gemini-imagegen/scripts"

/opt/homebrew/bin/python3.13 "$SCRIPTS/edit_image.py" "frame_01.jpg" \
  "Remove the subtitle text at the bottom of this image. Replace the text area with the natural background that would be behind it, maintaining the scene's continuity." \
  "frame_01_clean.jpg" --model gemini-3-pro-image-preview
```

### Phase C: Frame Enhancement

```bash
/opt/homebrew/bin/python3.13 "$SCRIPTS/edit_image.py" "frame_01_clean.jpg" \
  "Enhance this image to be sharper, clearer, with better lighting and color balance. Make it look professional and high-quality while keeping the exact same content, composition, and person unchanged." \
  "frame_01_enhanced.jpg" --model gemini-3-pro-image-preview
```

**CRITICAL: Never stretch low-res frames.** Keep native resolution, maximum 1.4x upscale.

### Phase D: Canvas Layout with Pillow

```python
#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# Canvas size (4:5 portrait)
CANVAS_W, CANVAS_H = 1080, 1350

canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), '#FFFFFF')

# Load and place enhanced frame (centered, no stretching)
frame = Image.open('frame_01_enhanced.jpg')
scale = min(CANVAS_W / frame.width, 1.4)
new_w = int(frame.width * scale)
new_h = int(frame.height * scale)
frame = frame.resize((new_w, new_h), Image.LANCZOS)

x = (CANVAS_W - new_w) // 2
y = (CANVAS_H - new_h) // 2
canvas.paste(frame, (x, y))

# Add text overlays, annotations, arrows, highlights as needed
canvas.save('slide_01.jpg', quality=95)
```

### Phase E: Organize & Verify

Same as Mode A — rename, output to `clean/` folder, verify quality.

---

## Standalone: Watermark Removal Only

1. Get source — Google Drive folder or local file path
2. Download all images
3. Run each through Gemini Pro inpainting with sparkle removal prompt
4. Verify all corners are clean
5. Rename: `[number] - [Title].jpg`
6. Output to `clean/` subfolder
