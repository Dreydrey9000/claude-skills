# Multi-Cam Split Screen Compositor

Composite 2 vertical camera angles + 1 horizontal audio source into split screen layouts at production quality. Built for 3-camera podcast/interview setups (2 close-up iPhones + 1 wide camera).

## When User Says "Split Screen", "Multi-Cam", or "Composite These Videos"

1. Find the 3 video files (2 vertical + 1 horizontal)
2. Identify who is in each vertical (extract frame, look at it)
3. **ASK which audio to keep and which to silence**
4. Ask which layout they want (show the menu below)
5. **ALWAYS export BOTH formats** — ProRes master AND H.264 sharing copy:
   - `--format prores` → `.mov` (master quality, ~2-3 GB/min)
   - `--format h264` → `.mp4` (sharing quality, ~100-200 MB/min)
   - Deliver both files to the user's Desktop (or specified location)
6. Extract a preview frame — verify faces are visible and within safe zone
7. Open the output for review and present both files with sizes

---

## Layout Menu

| Layout | Aspect | Description |
|--------|--------|-------------|
| `top-bottom` | 9:16 | Person A on top, Person B on bottom (vertical split) |
| `side-by-side` | 16:9 | Person A on left, Person B on right (horizontal split) |
| `side-by-side-9x16` | 9:16 | Both people side by side in vertical frame, center-cropped strips |
| `pip-left` | 16:9 | Wide shot with Person A as small picture-in-picture (bottom-left) |
| `pip-right` | 16:9 | Wide shot with Person B as small picture-in-picture (bottom-right) |
| `wide-only` | 16:9 | Just the horizontal camera, no split |

---

## Quick Start

```bash
# Vertical split — side by side 9:16 (recommended for TikTok/Reels)
python3 ~/.claude/skills/_youtube-execution/multicam_split.py \
    --left "person_A.mov" \
    --right "person_B.mov" \
    --audio "wide_shot.mov" \
    --layout side-by-side-9x16

# Top/bottom vertical split
python3 ~/.claude/skills/_youtube-execution/multicam_split.py \
    --left "person_A.mov" \
    --right "person_B.mov" \
    --audio "wide_shot.mov" \
    --layout top-bottom

# Horizontal split — side by side 16:9
python3 ~/.claude/skills/_youtube-execution/multicam_split.py \
    --left "person_A.mov" \
    --right "person_B.mov" \
    --audio "wide_shot.mov" \
    --layout side-by-side

# List all layouts
python3 ~/.claude/skills/_youtube-execution/multicam_split.py --list-layouts
```

---

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--left`, `-l` | required | Left/top person video (vertical 9:16) |
| `--right`, `-r` | required | Right/bottom person video (vertical 9:16) |
| `--audio`, `-a` | required | Main audio source (horizontal 16:9 camera) |
| `--output`, `-o` | auto | Output file path (auto-names based on layout) |
| `--layout` | top-bottom | Layout preset (see menu above) |
| `--format` | prores | `prores` (max quality), `h264` (hardware), `h264-software` (fallback) |
| `--left-crop-y` | auto | Custom vertical crop offset for left/top person |
| `--right-crop-y` | auto | Custom vertical crop offset for right/bottom person |
| `--list-layouts` | - | Show available layouts and exit |

---

## Quality Formats

| Format | Codec | Quality | File Size | Use Case |
|--------|-------|---------|-----------|----------|
| `prores` | ProRes 422 HQ + PCM 24-bit | Lossless-grade | ~2-3 GB/min | Master file, NLE import |
| `h264` | H.264 VideoToolbox 15Mbps + AAC 320k | Very high | ~100-150 MB/min | Sharing, direct upload |
| `h264-software` | libx264 CRF 12 + AAC 320k | Very high | ~80-120 MB/min | Fallback if no Apple Silicon |

**Default is `prores` — always export masters at max quality, compress later.**

---

## Workflow

### Standard 3-Camera Setup

**Equipment:**
- Camera 1 (vertical): iPhone on Person A — close-up
- Camera 2 (vertical): iPhone on Person B — close-up
- Camera 3 (horizontal): Main camera — wide shot, best audio (lav mic or shotgun)

**File naming convention from DaVinci Resolve:**
- `*_V1-*.mov` — horizontal (wide shot, main audio)
- `*_V2-*.mov` — vertical (Person A)
- `*_V3-*.mov` — vertical (Person B)

### Post-Production

1. **Ask about audio** — which track to use, which to silence
2. Run this script to composite desired layout
3. **Verify safe zone** — extract frame, overlay template, check faces
4. Import the ProRes output into CapCut/Premiere/DaVinci
5. Add text overlays, transitions, effects
6. Export final

---

## Crop Tuning

If a person's head is cut off or framing is wrong, adjust the Y crop offset:

```bash
# Move Person A's crop down (show more of their body, less ceiling)
python3 ~/.claude/skills/_youtube-execution/multicam_split.py \
    --left A.mov --right B.mov --audio main.mov \
    --layout top-bottom \
    --left-crop-y 350

# Move Person B's crop up (show more headroom)
python3 ~/.claude/skills/_youtube-execution/multicam_split.py \
    --left A.mov --right B.mov --audio main.mov \
    --layout top-bottom \
    --right-crop-y 100
```

Default crop values are tuned for standard seated interview framing.

---

## Output

- **Deliverable:** Composited video at specified output path
- **Default location:** `~/.tmp/{filename}_split_{layout}.mov`
- **Format:** ProRes 422 HQ (.mov) or H.264 (.mp4)
- **Audio:** From whichever source the user specifies (always ask first)
- **Resolution:** Matches layout (1080x1920 for 9:16, 1920x1080 for 16:9)
- **FPS:** Matches source (typically 30fps)

---

## Dependencies

```bash
brew install ffmpeg  # macOS (already installed)
```

No Python packages required — uses only ffmpeg and ffprobe via subprocess.
Pillow required only for safe zone overlay generation (already installed).

---

## Troubleshooting

### Videos not synced
All 3 cameras must be synced before running this script. If shot on DaVinci Resolve multicam, they're already synced. If not, sync in your NLE first or use matching timecodes.

### Person's head cut off
Adjust `--left-crop-y` or `--right-crop-y` to shift the crop window up (lower value) or down (higher value). Always verify with a preview frame before accepting.

### Face in TikTok danger zone
If a face sits behind the like/comment buttons or under the caption area, adjust crop offsets to move the face into the safe rectangle.

### File too large
ProRes is meant to be large — it's a production format. Use `--format h264` for smaller files when you don't need master quality.

### Hardware encoding fails
Use `--format h264-software` as fallback.


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
