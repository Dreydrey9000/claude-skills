# Video Cloner — Clone Any Video Style & Auto-Edit

Download any video (Instagram, TikTok, YouTube), analyze it frame-by-frame at 0.5s intervals, extract the exact visual style (fonts, colors, layouts, transitions, overlays, animations), and apply that style to your own footage. Produces both auto-edited video files AND detailed edit instruction docs.

### Extract Frames at 0.5s Intervals

```bash
# Extract every 0.5 seconds — this is the core analysis input
ffmpeg -i ref_video.mp4 -vf "fps=2" -q:v 2 ~/.tmp/ref_frames/frame_%04d.jpg

# Also extract audio for transcription
ffmpeg -i ref_video.mp4 -vn -acodec pcm_s16le ~/.tmp/ref_audio.wav
```

## Phase 2: Frame-by-Frame Style Analysis

For EVERY extracted frame, catalog the following:

## Phase 3: Style Profile Generation

After analyzing all frames, generate a **reusable style profile** saved to `~/.claude/skills/video-cloner/styles/`:

### Style Profile Document

```markdown
# Style Profile: @creator_handle

## Source
- Reference: [URL]
- Creator: @handle
- Platform: Instagram Reels
- Duration: 45s
- Views: 2.1M
- Date analyzed: [today]

## Text Overlays
- **Hook text:** Montserrat Bold, #FFFFFF, black stroke 3px
- **Position:** Top center, 15% from top
- **Animation:** Pop-in with slight scale (1.0 → 1.05 → 1.0)
- **Duration:** Stays for first 3 seconds

## Transitions & Pacing
- **Primary:** Hard cuts
- **Average cut interval:** 2.1 seconds
- **Zoom pattern:** Punch-in to 1.2x every 4-6 seconds
- **Speaker switches:** Cross-dissolve 0.2s (only for multi-person)

## Overlays & Images
- **Article screenshots:** Full-width, centered, 3-second hold
- **Product images:** Right-aligned, 40% frame width, drop shadow
- **Sourcing:** Official brand websites, current as of today

## Color & Grade
- **Temperature:** Warm (+10)
- **Contrast:** High
- **Saturation:** Slightly boosted
- **Vignette:** None

## Layout
- **Primary:** Single talking head, centered
- **Secondary:** Article screenshot full-frame with voiceover
- **Tertiary:** Product image overlay right-side during mention
```

---

## Phase 4: Image & Article Sourcing

When the reference video (or your own footage) mentions brands, products, articles, or statistics — source accurate visuals.

## Phase 5: Auto-Edit Pipeline

### What Needs Manual/CapCut Finishing

| Element | Why It Can't Be Auto-Edited | Instruction Format |
|---------|---------------------------|-------------------|
| **Animated text (slide-in, pop)** | FFmpeg can't do smooth text animations | Exact text, font, color, timing, animation type in edit doc |
| **Music/SFX sync** | Requires creative judgment on track selection | BPM suggestion, mood, where to place drops |
| **Complex transitions (3D, morph)** | Beyond ffmpeg filter capabilities | Exact timestamp, transition type, duration in edit doc |
| **Green screen compositing** | Requires chroma key + background selection | Background source + key color in edit doc |
| **Motion tracking text** | Text that follows a person/object | Position keyframes in edit doc |

## Phase 6: Edit Instructions Document

For everything that can't be auto-edited, produce a detailed instruction doc:

### Edit Instructions Format

```markdown
# EDIT INSTRUCTIONS — Style Clone of @reference_handle
## Applied to: [Your Video Title]
## Date: [today]

---

## What Was Auto-Edited (Already Applied)
- [x] Word-highlight subtitles (Poppins ExtraBold, yellow highlight, dark pill bg)
- [x] Hook text overlay ("STOP DOING THIS" — Montserrat Bold, white, top-center)
- [x] Article screenshot at 8.0s-10.5s (Chase Sapphire Preferred — verified current)
- [x] Zoom punch-in at 3.0s, 7.5s, 15.0s (1.2x)
- [x] Hard cuts matching 2.1s average pacing

## What Needs Manual Finishing (CapCut/Premiere)

### 1. Animated Text at 0:00-0:03
- **Text:** "STOP DOING THIS WITH YOUR MONEY"
- **Font:** Montserrat Bold, 48pt
- **Color:** #FFFFFF with #000000 stroke (3px)
- **Animation:** Pop-in with slight bounce (scale 0 → 1.05 → 1.0, 0.3s duration)
- **Position:** Top center, 15% from top edge
- **Reference frame:** See frame_004.jpg

### 2. Product Image Slide-In at 0:08
- **Image:** Chase Sapphire Preferred card (sourced: prepared_overlay_chase.png)
- **Animation:** Slide in from right, 0.3s ease-out
- **Position:** Right-center, 40% frame width
- **Hold:** 3 seconds
- **Exit:** Fade out 0.2s
- **Reference frame:** See frame_017.jpg

### 3. Background Music
- **Mood:** Upbeat, confident, corporate-casual
- **BPM:** ~120 (matches reference pacing)
- **Volume:** -18dB under voice
- **Drop at:** 0:03 (after hook text)

---

## Frame Comparison
| Timestamp | Reference Frame | Our Recreation |
|-----------|----------------|---------------|
| 0:00 | ref_frame_001.jpg | our_frame_001.jpg |
| 0:03 | ref_frame_007.jpg | our_frame_007.jpg |
| 0:08 | ref_frame_017.jpg | our_frame_017.jpg |
```

---

## Phase 7: Quality Verification

Before delivering:

## Supported Content Types

## Tools Required

### Core (Must Have)

| Tool | Purpose | Install |
|------|---------|---------|
| **yt-dlp** | Download videos from Instagram/TikTok/YouTube | `brew install yt-dlp` or `pip3 install yt-dlp` |
| **ffmpeg** | Frame extraction, video encoding, overlays, cuts | `brew install ffmpeg` |
| **ffprobe** | Video metadata — resolution, duration, FPS | Included with ffmpeg |
| **faster-whisper** | Word-level transcription for subtitle timing | `pip3 install faster-whisper` |
| **Pillow (PIL)** | Frame-by-frame subtitle rendering, image preparation | `pip3 install Pillow` |
| **Python 3** | Scripting for all pipelines | Pre-installed on macOS |

### Image & Article Sourcing

| Tool | Purpose |
|------|---------|
| **Perplexity** | Research articles, verify claims, find current brand info |
| **WebFetch** | Fetch article pages for screenshot content |
| **WebSearch** | Search for current product images, brand assets |
| **Google Drive MCP** | Store sourced images for reuse |

## Examples

### Example 1: Clone Coretta Brothers Credit Card Video

**Input:** "Clone this: [Instagram Reel URL] — apply to my Baileys video"

**What happens:**
1. Downloads Coretta Brothers reel
2. Extracts 60 frames (30s at 0.5s intervals)
3. Detects: Montserrat Bold hook text, word-highlight subs (yellow on white, Poppins), article screenshots of credit card pages, product card images, punch-in zooms every 3s
4. Sources: Current Chase Sapphire Preferred card image from chase.com, AmEx Platinum from americanexpress.com — verifies current designs
5. Applies detected subtitle style to Baileys footage
6. Inserts sourced product images at appropriate timestamps
7. Generates edit instructions for animated text and transitions
8. Delivers: auto-edited video + instructions doc + style profile saved as `@corettabrothers_style.md`


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
