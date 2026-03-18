# Recreate YouTube Thumbnails with Nick Saraev

## Goal
Face-swap YouTube thumbnails to feature Nick Saraev using Nano Banana Pro (Gemini image model). The system:
- Analyzes face direction (yaw/pitch) in the source thumbnail
- Finds the best-matching reference photo of Nick by pose
- Generates 3 variations by default
- Supports iterative edit passes for refinements

## Quick Start

```bash
# Generate 3 variations from a YouTube video
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --youtube "https://youtube.com/watch?v=VIDEO_ID"

# Generate from a local thumbnail
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --source ".tmp/thumbnails/source_yt_thumb.jpg"

# Edit pass on a generated thumbnail
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --edit ".tmp/thumbnails/recreated_v3.png" \
  --prompt "Change colors to teal. Change 'AI GOLD RUSH' to 'AGENTIC FLOWS'."
```

## Full Workflow

### Step 2: Generate Thumbnails

```bash
# From YouTube URL (auto-analyzes face, finds best reference, generates 3 variations)
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --youtube "https://youtube.com/watch?v=VIDEO_ID"

# From local image
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --source "path/to/thumbnail.jpg"

# Custom variation count
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --source "thumbnail.jpg" -n 5

# Skip direction matching (use default references)
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --source "thumbnail.jpg" --no-match
```

**What happens:**
1. Downloads/loads source thumbnail
2. Analyzes face direction using MediaPipe (yaw/pitch in degrees)
3. Finds best-matching reference by Euclidean distance in pose space
4. Loads 2 reference photos (best match + one other)
5. Sends to Gemini with face swap prompt
6. Generates 3 variations (results vary between runs)

### Step 3: Select Best & Edit

Pick your favorite variation, then refine with edit passes:

```bash
# Single edit
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --edit ".tmp/thumbnails/recreated_v3.png" \
  --prompt "Change colors to teal brand colors. Change 'AI GOLD RUSH' to 'AGENTIC FLOWS'."

# Chain multiple edits (each builds on the previous)
python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --edit ".tmp/thumbnails/edited_1.png" \
  --prompt "Change background to pure white. Make the graph show two bounces instead of one."

python ~/.claude/skills/_youtube-execution/recreate_thumbnails.py --edit ".tmp/thumbnails/edited_2.png" \
  --prompt "Make 'AGENTIC FLOWS' text bigger. Change 'The Moment' to 'its happening'."
```

**Edit pass tips:**
- Be specific about what to change
- Reference exact text strings when changing copy
- Colors, text, graphs, backgrounds all work well
- Each edit is a separate API call (~$0.14-0.24)

## File Locations

| Path | Purpose |
|------|---------|
| `.tmp/reference_photos/` | Direction-labeled reference photos (nick_yawR20_pitchD45.jpg) |
| `.tmp/reference_photos/raw/` | Drop new photos here for analysis |
| `.tmp/thumbnails/YYYYMMDD/` | Generated thumbnails organized by date |
| `~/.claude/skills/_youtube-execution/recreate_thumbnails.py` | Main script |
| `~/.claude/skills/_youtube-execution/analyze_face_directions.py` | Reference photo analyzer |

## Output Organization

Thumbnails are stored in date-based folders:
```
.tmp/thumbnails/
├── 20251205/              # December 5, 2025
│   ├── 104016_1.png       # Generated at 10:40:16, variation 1
│   ├── 104016_2.png       # Generated at 10:40:16, variation 2
│   ├── 104016_3.png       # Generated at 10:40:16, variation 3
│   ├── 104532_edited.png  # Edit pass at 10:45:32
│   └── 110000_1.png       # Another run at 11:00:00
└── 20251206/              # December 6, 2025
    └── 090000_1.png
```

- Same-day runs go to the same folder
- New day creates a new folder
- Files named with HHMMSS timestamp + variation number (or `_edited` for edit passes)

### recreate_thumbnails.py

| Flag | Description |
|------|-------------|
| `--youtube`, `-y` | YouTube video URL |
| `--source`, `-s` | Source thumbnail path or URL |
| `--edit`, `-e` | Image to edit (enables edit mode) |
| `--prompt`, `-p` | Additional instructions (required for edit mode) |
| `--variations`, `-n` | Number of variations (default: 3) |
| `--refs` | Number of reference photos (default: 2) |
| `--output`, `-o` | Custom output filename |
| `--no-match` | Skip face direction matching |
| `--style` | Style description (rarely needed) |

### analyze_face_directions.py

| Flag | Description |
|------|-------------|
| `--preview`, `-p` | Show analysis without renaming |
| `--single`, `-s` | Analyze a single image |
| `--find` | Find closest reference for yaw,pitch (e.g., `--find "-30,10"`) |

## API Notes

- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Cost:** ~$0.14-0.24 per generation/edit
- **Latency:** 10-60+ seconds per image
- **Output resolution:** ~1376x768 (close to 16:9, model rounds slightly)
- **API key:** `NANO_BANANA_API_KEY` in `.env`

## Naming Convention

Reference photos use this format:
```
nick_yaw{L/R}{degrees}_pitch{U/D}{degrees}.jpg
```

| Component | Meaning |
|-----------|---------|
| `yaw` | Left/right rotation |
| `L`/`R` | Direction (L=left, R=right, omit for 0) |
| `pitch` | Up/down tilt |
| `U`/`D` | Direction (U=up, D=down, omit for 0) |
| `_1`, `_2` | Suffix for duplicates at same angle |

Examples:
- `nick_yawL30_pitchU10.jpg` — looking 30° left, 10° up
- `nick_yawR45_pitch0.jpg` — looking 45° right, level
- `nick_yaw0_pitch0.jpg` — dead center

## Learnings

- **Face direction matching reduces uncanny valley** — using a reference with similar pose to the target dramatically improves results
- Uses native 1280x720 input resolution for crisp output on large displays
- **2 reference photos is optimal** — 1 loses likeness, 3+ can cause full image regeneration
- **Must explicitly request 16:9 format** in prompt or model outputs squares
- **Label images explicitly** in prompt ("IMAGE 1: Reference photo, IMAGE 2: Thumbnail") to prevent confusion
- Keep prompts simple and direct — complex instructions cause regeneration instead of editing
- Generate 3 variations by default since results vary between runs
- "100% exact duplicate except face" instruction works well for pure face swaps
- Edit passes work well for text, colors, graphs, backgrounds
- Multiple edit passes can be chained (each builds on previous output)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No face detected | Falls back to default references (alphabetical order) |
| High distance match | Add more reference photos covering that angle |
| API timeout | Try again; reduce image sizes if persistent |
| Poor face blending | Lighting/angle mismatch; try different reference photos |
| Text garbled | Be more explicit in edit prompt; try simpler wording |
| Wrong aspect ratio | Model outputs ~1376x768; close enough for YouTube |


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
