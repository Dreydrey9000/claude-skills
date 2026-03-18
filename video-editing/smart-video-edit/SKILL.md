# Video Editing Directive

Automatically edit talking-head videos: remove silences, enhance audio, add swivel teaser, and optionally upload to YouTube.

---

## Recommended Workflow (VAD + Swivel Teaser)

The best quality workflow uses neural voice activity detection for silence removal, then adds a swivel teaser preview.

### When User Says "Edit X Video"

1. Run Step 1 (VAD silence removal) on the input video
2. Run Step 2 (swivel teaser) on the edited output
3. Open the final video for user review

**Background image:** Use `.tmp/bg.png` if it exists, otherwise omit `--bg-image` (uses solid gray).

### Quick Start

**IMPORTANT: Always use the parallel version (`jump_cut_vad_parallel.py`) - it's 5-10x faster.**

```bash
# Step 1: Remove silences + enhance audio (PARALLEL version)
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 .tmp/edited.mp4 --enhance-audio

# Step 2: Add swivel teaser at 3 seconds (previews content from 1:00 onwards)
python3 ~/.claude/skills/_youtube-execution/insert_3d_transition.py .tmp/edited.mp4 output.mp4 \
    --bg-image .tmp/background.png
```

### One-liner

```bash
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 .tmp/edited.mp4 --enhance-audio && \
python3 ~/.claude/skills/_youtube-execution/insert_3d_transition.py .tmp/edited.mp4 output.mp4 --bg-image .tmp/bg.png
```

### What This Produces

| Step | Tool | Result |
|------|------|--------|
| 1 | `jump_cut_vad_parallel.py` | Silences removed via neural VAD, audio enhanced (EQ, compression, -16 LUFS) |
| 2 | `insert_3d_transition.py` | 5-second swivel teaser inserted at 3s, previewing content from 1:00 onwards |

**Timeline:**
```
[0-3s intro] [3-8s swivel teaser @ 60x] [8s onwards: edited content]
Audio: Original audio plays continuously throughout
```

### Full Options

```bash
# With "cut cut" restart detection (removes mistakes)
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 .tmp/edited.mp4 \
    --enhance-audio --detect-restarts

# With LUT color grading
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 .tmp/edited.mp4 \
    --enhance-audio --apply-lut .tmp/cinematic.cube

# Custom swivel teaser timing
python3 ~/.claude/skills/_youtube-execution/insert_3d_transition.py .tmp/edited.mp4 output.mp4 \
    --insert-at 5 --duration 3 --teaser-start 90 --bg-image .tmp/bg.png
```

See `directives/jump_cut_vad.md` and `directives/pan_3d_transition.md` for full documentation.

---

## Alternative: Simple FFmpeg Workflow

For simpler needs, use the FFmpeg-based workflow with Auphonic upload.

### Execution Script

`~/.claude/skills/_youtube-execution/simple_video_edit.py`

## What It Does (Pipeline)

1. **Silence Detection** - FFmpeg detects silences ≥3s at -35dB
2. **Silence Removal** - Cuts all detected silences (no AI decisions)
3. **Audio Normalization** - EBU R128 (-16 LUFS) + 80Hz highpass
4. **Transcription** - Whisper transcribes for metadata generation
5. **Metadata Generation** - Claude generates summary + chapters (saved to file)
6. **Auphonic Upload** - Uploads to Auphonic → YouTube as private draft

---

### Silence Detection
- FFmpeg `silencedetect` filter
- Default: -35dB threshold, 3s minimum duration (stricter to filter out breathing)
- All detected silences are cut (no AI filtering)

### Audio Normalization
```
highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11
```

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `highpass=f=80` | 80Hz | Remove low-frequency rumble |
| `I=-16` | -16 LUFS | YouTube loudness standard |
| `TP=-1.5` | -1.5 dBTP | True peak limit |
| `LRA=11` | 11 LU | Loudness range |

### Video Encoding
- macOS: Hardware encoding (h264_videotoolbox) at 8Mbps
- Fallback: libx264 CRF 18
- Audio: AAC 320kbps

---

## Recording Workflow

1. **Start recording** (1-3s silent intro is fine)
2. **Speak content** with natural pauses
3. **Long pause (3+ seconds)** = will be cut
4. **Stop recording**

If you make a mistake, just pause 3+ seconds and redo. The silence will be removed.

---

## Dependencies

```bash
pip install anthropic faster-whisper python-dotenv requests
brew install ffmpeg  # macOS
```

### Environment Variables (`.env`)

```
ANTHROPIC_API_KEY=sk-ant-...
AUPHONIC_API_KEY=...
```

### Hardcoded Values

```python
AUPHONIC_PRESET_UUID = "8YdWMdfF2QXpdZ2mDuUugj"
YOUTUBE_SERVICE_UUID = "bkVnnU8ziaaHjRckFz9XAT"  # Nick Saraev channel
```

---

## Troubleshooting

### Audio too quiet
Run without `--no-normalize` to apply EBU R128 normalization.

### Cuts feel abrupt
Increase `--silence-duration` to only cut longer pauses (e.g., `--silence-duration 5`).

### Too much content being cut
Raise threshold: `--silence-threshold -40` (more negative = quieter sounds needed to trigger).

### Breathing sounds kept as pauses
The default -35dB should handle most breathing. If not, try `--silence-threshold -30` (less negative = louder sounds still count as silence).

### Hardware encoding fails
Script automatically falls back to software encoding (libx264).

---

## Related Tools

### Jump Cut Editor (VAD-based) - `~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py`
More accurate silence removal using neural voice activity detection (Silero VAD). Better than FFmpeg for detecting actual speech vs. background noise. **Always use the parallel version for 5-10x faster processing.**

```bash
# Basic usage
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 output.mp4

# With audio enhancement and LUT color grading
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad_parallel.py input.mp4 output.mp4 \
    --enhance-audio --apply-lut .tmp/cinematic.cube
```

### 3D Pan Transition - `~/.claude/skills/_youtube-execution/pan_3d_transition.py`
Create fast-forward "preview" transitions with 3D rotation effects. See `directives/pan_3d_transition.md`.

```bash
# Create intro transition
python3 ~/.claude/skills/_youtube-execution/pan_3d_transition.py input.mp4 .tmp/intro.mp4 \
    --output-duration 3 --bg-image .tmp/background.png
```


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
