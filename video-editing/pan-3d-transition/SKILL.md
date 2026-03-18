# 3D Pan Transition Effect

Create fast-forward "preview" style transitions with subtle 3D rotation, similar to Premiere Pro's Basic 3D effect. Used for intros, scene transitions, or "coming up" previews.

## What It Does

1. **Extracts frames** from source video at native FPS
2. **Applies 3D CSS transforms** (rotateY, rotateX, scale) via Remotion
3. **Fast-forwards playback** (default 7x speed)
4. **Renders final video** at source resolution/FPS

The effect creates a subtle "floating card" look where the video appears to rotate in 3D space while playing at high speed.

---

## Tuned Default Values

These defaults were calibrated for subtle, professional-looking transitions:

```python
SWIVEL: 3.5° → -3.5°    # Gentle left-to-right rotation
TILT: 1.7° (constant)    # Slight upward tilt, no animation
ZOOM: 1.5% out           # Hardcoded in render (scale 0.985)
SPEED: 7x                # Fast but readable
EASING: linear           # Smooth, predictable motion
```

### Parameter Tuning Guide

| Effect | Parameter | Range | Notes |
|--------|-----------|-------|-------|
| More dramatic rotation | `--swivel-start/end` | ±5-15° | Keep symmetric (e.g., 10 → -10) |
| Subtle rotation | `--swivel-start/end` | ±2-4° | Current default is 3.5° |
| Constant tilt | `--tilt-start` = `--tilt-end` | 1-3° | No tilt animation |
| Tilt animation | Different start/end | 0-5° | Tilts during playback |
| Faster preview | `--speed` | 10-15 | For longer source content |
| Slower, readable | `--speed` | 3-5 | For shorter clips |
| Bouncy feel | `--easing spring` | - | Overshoots then settles |
| Smooth deceleration | `--easing easeOut` | - | Fast start, slow end |

---

## Background Options

### Solid Color (default)
```bash
python3 ~/.claude/skills/_youtube-execution/pan_3d_transition.py input.mp4 output.mp4 --bg-color "#1a1a2e"
```

### Background Image
```bash
python3 ~/.claude/skills/_youtube-execution/pan_3d_transition.py input.mp4 output.mp4 --bg-image .tmp/bg.png
```

The background is visible at the edges when the video rotates in 3D space. Use an image that complements your content (nature scenes, abstract textures, etc.).

---

## Performance

| Resolution | Output Duration | Render Time |
|------------|-----------------|-------------|
| 4K 60fps | 1 second | ~15-20s |
| 4K 60fps | 5 seconds | ~80s |
| 1080p 30fps | 1 second | ~5-8s |
| 1080p 30fps | 5 seconds | ~25-30s |

**Bottlenecks:**
1. FFmpeg frame extraction (disk I/O + decoding)
2. Remotion rendering (3D transforms on each frame)

---

### How It Works

1. **FFmpeg** extracts JPEG frames from source video segment
2. Frames are copied to Remotion's `public/frames/` directory
3. **Remotion** (React-based video renderer) generates a dynamic composition:
   - CSS `perspective` for 3D depth
   - CSS `transform: rotateY() rotateX() scale()` for 3D effect
   - Frame interpolation based on playback rate
4. Remotion renders final MP4 at source resolution/FPS
5. Temp frames are cleaned up

### CSS Transform Order

```css
transform: translateY(0%) rotateY(Xdeg) rotateX(Ydeg) scale(0.985)
```

- `translateY`: Vertical offset (currently 0)
- `rotateY`: Swivel (left/right rotation)
- `rotateX`: Tilt (up/down rotation)
- `scale`: Zoom (0.985 = 1.5% zoom out)

### Easing Functions

| Type | Behavior |
|------|----------|
| `linear` | Constant speed throughout |
| `easeOut` | Fast start, gradual slowdown |
| `easeInOut` | Slow start, fast middle, slow end |
| `spring` | Overshoots target, bounces back |

---

## Dependencies

### System Requirements
```bash
brew install ffmpeg node  # macOS
```

### Remotion Setup (one-time)
```bash
cd ~/.claude/skills/_youtube-execution/video_effects
npm install
```

The script uses `npx remotion render` which handles Remotion execution.

---

## Example Workflow

### Creating a "Coming Up" Preview

```bash
# Start 2 minutes into the video, create 5-second preview
python3 ~/.claude/skills/_youtube-execution/pan_3d_transition.py \
    .tmp/full_video.mp4 \
    .tmp/coming_up.mp4 \
    --start 120 \
    --output-duration 5 \
    --speed 10
```

---

## Troubleshooting

### Remotion render fails
```
Render error: Cannot find module 'remotion'
```
**Fix:** Run `npm install` in `~/.claude/skills/_youtube-execution/video_effects/`

### Video looks too zoomed out
The zoom is hardcoded at 1.5% (scale 0.985). To change, edit `pan_3d_transition.py` line ~196:
```python
const scaleVal = 0.985; // Change this value
```

### Background image not showing
- Ensure image path is correct and file exists
- Supported formats: PNG, JPG, JPEG
- Image is copied to Remotion's public folder during render

### Render is slow
- Lower resolution source = faster render
- Shorter output duration = fewer frames
- The 4K 60fps source extracts 2100 frames for a 5s transition at 7x speed

---

## Output

- **Deliverable:** Video file at specified output path
- **Format:** MP4 (H.264)
- **Resolution:** Matches source video
- **FPS:** Matches source video

---


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
