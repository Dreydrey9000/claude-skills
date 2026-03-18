# NRVES Pipeline - Viral Editz Automated Video Assembly Line

Automated end-to-end video editing pipeline for the Viral Editz agency. Processes raw client footage into publish-ready vertical (Instagram Reels) or horizontal (YouTube) content using the NRVES methodology.

Use this skill when the user says: "edit video", "process video", "edit with Claude", "run NRVES", "video editing", "edit this clip", "process this footage", "run the pipeline", "edit for [client name]", "creative mode", or drops a video file into a client watch folder.

## What It Does

Chains existing tools into a single automated workflow:

1. **N - Narrative**: Transcribe (faster-whisper) + identify hook (Claude API)
2. **R - Retention**: Remove silences (Silero VAD neural detection)
3. **V - Visual**: Crop to 9:16 with face tracking (OpenCV, eye-line at 1/3)
4. **E - Enhance**: Reorder around hook OR creative editorial cuts to target duration
5. **S - Submit**: Burn subtitles (libass) + export final MP4

## Execution Scripts

- **Pipeline**: `~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py`
- **Watch Folder**: `~/.claude/skills/_youtube-execution/nrves_pipeline/watch_folder.py`
- **Client Configs**: `~/.claude/skills/_youtube-execution/nrves_pipeline/client_configs/`

## Quick Start

```bash
# Process a single video with client config
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  input.mp4 --client thecreditbrothers

# Creative mode: AI analyzes transcript, creates editorial plan, cuts to target duration
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  input.mp4 --client thecreditbrothers --creative

# Creative mode with custom target (60 seconds)
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  input.mp4 --creative --target-duration 60

# Process all videos in a client folder
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  ~/Desktop/nrves/raw/thecreditbrothers/ --client thecreditbrothers

# Quick mode: just silence removal + subtitles
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  input.mp4 --client luiscarrillo --quick

# Skip specific steps
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/nrves_pipeline.py \
  input.mp4 --skip-crop --skip-subtitles
```

## Two Modes

### Trust Mode (default)
Auto-processes everything without stopping. Best for simple clips that just need silence removal, crop, and subtitles.

```bash
python3 nrves_pipeline.py input.mp4 --client epicdental
```

### Creative Mode (`--creative`)
AI analyzes the transcript first, creates an editorial plan showing which segments to keep, identifies the hook, and cuts to the target duration. Best for longer recordings where editorial decisions matter.

```bash
python3 nrves_pipeline.py input.mp4 --client thecreditbrothers --creative
```

The editorial plan is saved as `{filename}_editorial_plan.json` in the output directory for review.

## Watch Folder System

Drop videos into client folders and they auto-process:

```bash
# Start the watcher (runs in background)
python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/watch_folder.py

# Or run in background
nohup python3 ~/.claude/skills/_youtube-execution/nrves_pipeline/watch_folder.py &
```

### Folder Structure

```
~/Desktop/nrves/
├── raw/                          # Drop videos here
│   ├── luiscarrillo/
│   ├── ryanmagin/
│   ├── ryanmagin_youtube/
│   ├── thecreditbrothers/
│   ├── epicdental/
│   └── thebaileys/
├── processed/                    # Output appears here
│   └── {client_name}/
│       ├── {filename}_NRVES.mp4  # Final video
│       ├── {filename}_NRVES.srt  # Subtitle file
│       └── {filename}_editorial_plan.json  # (Creative mode only)
└── logs/                         # Processing logs
```

## Client Configs

Each client has a JSON config in `client_configs/`. Configs control every parameter:

| Client | Mode | Special |
|--------|------|---------|
| `luiscarrillo` | vertical | Standard |
| `ryanmagin` | vertical | Tight cuts (0.3s silence, 60ms padding) |
| `ryanmagin_youtube` | horizontal | No crop, no subtitles |
| `thecreditbrothers` | vertical | Left channel audio fix, 90s target |
| `epicdental` | vertical | Standard |
| `thebaileys` | vertical | Standard |
| `hormozi` | vertical | Aggressive cuts (0.4s silence, 80ms padding) |

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `input` | required | Input video file or folder |
| `--client`, `-c` | `default` | Client config name |
| `--output-dir`, `-o` | same as input | Output directory |
| `--skip-crop` | false | Skip 9:16 crop |
| `--skip-subtitles` | false | Skip subtitle burn |
| `--skip-hook` | false | Skip hook detection |
| `--quick`, `-q` | false | Quick: silence removal + subtitles only |
| `--creative` | false | Creative mode: editorial analysis + cuts |
| `--target-duration`, `-t` | from config | Target output duration in seconds |

## Face Tracking

The crop step uses OpenCV Haar cascade face detection:

- Samples 15 frames across the first 30 seconds
- Averages face position across all detections
- Centers face horizontally in the 9:16 crop
- Positions eye line at 1/3 from top (standard talking-head framing)
- If face is already above 1/3, uses full source height
- If face is below 1/3, zooms in (max 30% zoom) to reframe

## Audio Channel Fix

For recordings where only one mic channel has audio:

```json
"audio": {
  "fix_channels": "left"
}
```

Options: `"left"` (duplicate left to both), `"right"` (duplicate right), `"auto"` (detect and fix).

## Creative Mode - Editorial Analysis

When `--creative` is used, the pipeline sends the full transcript to Claude Sonnet to:

1. Identify the strongest hook
2. Map all story beats with timestamps
3. Select segments that create a complete narrative arc within target duration
4. Detect if multiple video opportunities exist in the footage
5. Return a structured cut plan

The plan is printed to console and saved as JSON. Segments are extracted and concatenated in the planned order (hook first), then the cut video is re-transcribed for accurate subtitles.

**Requires**: `ANTHROPIC_API_KEY` environment variable (~$0.01-0.02 per video).

## Dependencies

```bash
# Already installed on this machine
pip3 install torch torchaudio faster-whisper anthropic watchdog opencv-python
brew install homebrew-ffmpeg/ffmpeg/ffmpeg  # FFmpeg with libass for subtitles
```

## Related Skills

- **clipper-skill**: Generates editing directions from transcripts (conceptual). NRVES pipeline executes them.
- **god-mode-vibe-editor**: NRVES methodology reference. This pipeline implements it.
- **smart-video-edit**: Simpler FFmpeg workflow + Auphonic upload. Use for YouTube uploads.
- **jump-cut-vad**: Standalone silence removal component. Used internally by this pipeline.


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
