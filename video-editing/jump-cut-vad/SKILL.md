# Jump Cut Editor (VAD-based)

Automatically remove silences from talking-head videos using neural voice activity detection (Silero VAD). More accurate than FFmpeg silence detection, especially for videos with background noise, breathing sounds, or quiet speech.

## What It Does

1. **Extracts audio** from video as WAV
2. **Runs Silero VAD** (neural voice activity detection) to identify speech segments
3. **Optionally detects "cut cut"** restart phrases and removes mistake segments
4. **Concatenates speech segments** with padding
5. **Applies audio enhancement** (optional): EQ, compression, loudness normalization
6. **Applies color grading** (optional): LUT-based color correction

---

## Features

### 1. Silero VAD (Voice Activity Detection)

Uses a neural network trained specifically for voice detection. Much better than FFmpeg's volume-based silence detection:

| Silero VAD | FFmpeg silencedetect |
|------------|---------------------|
| Detects actual speech | Detects volume drops |
| Ignores breathing | Cuts on breathing pauses |
| Works with background noise | Fails with background noise |
| Handles quiet speech | Misses quiet speech |

### 2. "Cut Cut" Restart Detection

Say "cut cut" during recording to mark a mistake. The script will:
1. Detect the phrase using Whisper transcription
2. Remove the segment containing "cut cut"
3. Remove the **previous** segment (where the mistake is)

This lets you redo takes naturally without stopping the recording.

```bash
# Enable restart detection
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad.py input.mp4 output.mp4 --detect-restarts

# Custom restart phrase
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad.py input.mp4 output.mp4 \
    --detect-restarts --restart-phrase "start over"
```

### 3. Audio Enhancement

Applies a professional voice processing chain:

```
highpass=f=80            # Remove rumble below 80Hz
lowpass=f=12000          # Remove harsh highs above 12kHz
equalizer (200Hz, -1dB)  # Reduce muddiness
equalizer (3kHz, +2dB)   # Boost presence/clarity
acompressor              # Gentle compression (3:1 ratio)
loudnorm=I=-16           # YouTube loudness standard (-16 LUFS)
```

```bash
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad.py input.mp4 output.mp4 --enhance-audio
```

### 4. LUT Color Grading

Apply color grading using standard LUT files:

```bash
# Apply .cube LUT
python3 ~/.claude/skills/_youtube-execution/jump_cut_vad.py input.mp4 output.mp4 \
    --apply-lut .tmp/cinematic.cube
```

**Supported formats:** `.cube`, `.3dl`, `.dat`, `.m3d`, `.csp`

---

## Parameter Tuning

### Silence Detection

| Goal | Parameter | Value |
|------|-----------|-------|
| More aggressive cuts | `--min-silence` | 0.3-0.4 |
| Preserve natural pauses | `--min-silence` | 0.8-1.0 |
| Keep very short utterances | `--min-speech` | 0.1-0.2 |
| Ignore brief sounds | `--min-speech` | 0.4-0.5 |

### Padding

| Goal | `--padding` value |
|------|------------------|
| Tight cuts | 50-80 |
| Natural feel | 100-150 |
| Extra breathing room | 200-300 |

---

## Recording Workflow

### With Restart Detection

1. Start recording
2. Speak naturally
3. Make a mistake → Say "cut cut" → Pause briefly → Redo from checkpoint
4. Continue recording
5. Stop when done

**The script automatically removes:**
- The segment containing "cut cut"
- The previous segment (your mistake)

### Without Restart Detection

1. Start recording
2. Speak with natural pauses
3. Long pauses (>0.5s default) will be cut
4. Finish and run the script

---

## Dependencies

### System Requirements

```bash
brew install ffmpeg  # macOS
```

### Python Dependencies

```bash
pip install torch  # For Silero VAD
pip install whisper  # For restart detection (optional)
```

Silero VAD is downloaded automatically from torch.hub on first run.

---

## Troubleshooting

### "No speech detected"
- Check that audio track exists in the video
- Try lowering `--min-speech` to 0.1

### Cuts feel too aggressive
- Increase `--padding` (e.g., 150-200)
- Increase `--min-silence` (e.g., 0.8)

### Breathing sounds being cut
VAD should handle this automatically. If not:
- Increase `--merge-gap` to 0.5
- Increase `--padding` slightly

### Restart detection not finding "cut cut"
- Ensure you speak the phrase clearly
- Try `--whisper-model medium` for better accuracy
- Check that Whisper is installed: `pip install whisper`

### LUT not applying
- Check file path is correct
- Ensure format is supported (.cube, .3dl, .dat, .m3d, .csp)
- Check FFmpeg has lut3d filter: `ffmpeg -filters | grep lut3d`

---

## Performance

## Output

- **Deliverable:** Edited video at specified output path
- **Format:** MP4 (H.264)
- **Encoding:** Hardware (10 Mbps) or Software (CRF 18), auto-detected
- **Audio:** AAC 192kbps (enhanced if `--enhance-audio`)
- **Resolution/FPS:** Matches source


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
