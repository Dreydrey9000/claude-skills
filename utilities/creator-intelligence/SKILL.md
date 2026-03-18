---
name: creator-intelligence
description: >
  Scrape, deconstruct, and database any Instagram creator or Viral Editz client's entire content
  strategy. Input = Instagram handle or client name. Output = full Notion database with deconstructed
  videos, hooks, scripts, frameworks, editing styles, performance data, Content Market Fit profile,
  and queryable intelligence. This is the BUSINESS tool for Viral Editz clients and creators — NOT
  for personal/dating intel (use ig-profile-scraper for that). Triggers: "deconstruct this creator",
  "add to creator database", "competitor analysis", "creator intelligence", "client database",
  "viral database", new client onboarding, "compare to", "find similar creators", "what's working for",
  "content strategy for @handle", "analyze their content", "creator breakdown",
  "scrape their IG", "scrape @handle", any Instagram handle or URL.
  DEFAULT RULE: This is the DEFAULT skill for ALL Instagram scraping. If Drey drops an IG handle
  or URL, this fires FIRST. Only route to ig-profile-scraper if Drey explicitly asks for
  personal/dating intel ("who is this girl", "tell me about her", "stalker mode").
  If ambiguous, ASK: "Personal intel or creator analysis?"
  LINKED TO: ig-profile-scraper (personal/dating sub-tool — uses Playwright for lightweight scrapes)
---

# Creator Intelligence Engine

## What This Is

A full extraction pipeline that takes any Instagram handle (or client) and builds a complete
intelligence database: every video deconstructed, every hook cataloged, every framework extracted,
every editing style documented, performance tracked over time. Queryable on demand.

## Pipeline Overview

```
@handle
  │
  ▼
Phase 1: SCRAPE (Apify)
  │  All posts, engagement, metadata
  ▼
Phase 2: DOWNLOAD (yt-dlp)
  │  Top 20-30 videos by performance
  ▼
Phase 3: DECONSTRUCT (AI Cookbook + Hume + Twelve Labs)
  │  Frames, transcription, emotion, scene analysis
  ▼
Phase 4: EXTRACT (Content Market Fit + framework extraction)
  │  Hooks, topics, scripts, frameworks, editing DNA
  ▼
Phase 5: DATABASE (Notion)
  │  Creator profile + per-video entries + aggregated stats
  ▼
Phase 6: QUERY
     "What's working for @X right now?"
```

---

## Phase 1: Scrape (Apify)

### Output
- CSV/JSON of all posts with metadata
- Sorted by performance (views descending)
- Tagged by content type

---

## Phase 2: Download Top Videos

```bash
# Download S-Tier and A-Tier reels (top 20-30)
# For each video:
yt-dlp --write-info-json -o "creator_handle/%(id)s.%(ext)s" [VIDEO_URL]
```

## Phase 3: Deconstruct Each Video

For each downloaded video, run the full analysis stack:

### 3a. Frame Extraction
```bash
# Standard: 1 frame every 3 seconds
ffmpeg -i video.mp4 -vf "fps=1/3" -q:v 2 frames/frame_%03d.jpg

# Detailed (for editing style analysis): 1 frame every 0.5 seconds
ffmpeg -i video.mp4 -vf "fps=2" -q:v 2 frames/frame_%03d.jpg
```

### 3b. Audio + Transcription
```bash
ffmpeg -y -i video.mp4 -vn -acodec pcm_s16le -ar 16000 audio.wav
# Transcribe with word timestamps
mlx_whisper.transcribe('audio.wav', path_or_hf_repo='mlx-community/whisper-large-v3-turbo', word_timestamps=True)
```

### 3d. Emotion Detection (Hume AI)
- Run on audio: detect emotion peaks
- Map emotion arc across the video duration
- Identify: hook emotion, peak emotion, closing emotion

### 3e. Video Understanding (Twelve Labs)
- Scene segmentation
- Action recognition
- Object detection
- Overall video classification

---

## Phase 4: Extract Intelligence (Per Video)

For each video, produce a structured analysis:

### Video Deconstruction Card

```markdown
## Video: [Title/First Line]
**URL:** [Instagram URL]
**Posted:** [Date]
**Duration:** [Seconds]
**Performance:** [Views] views | [Likes] likes | [Comments] comments | [ER]% engagement
**Tier:** [S/A/B/C]

### Hook (First 3 Seconds)
- **Text:** "[Exact opening words]"
- **Hook Type:** [Question / Bold Claim / Pattern Interrupt / Story / Stat / Controversy]
- **Visual:** [What's on screen in first 3 seconds]
- **Emotion:** [From Hume - curiosity, surprise, authority, etc.]

### Topic
- **Category:** [AI Tools / Business / Lifestyle / Tutorial / etc.]
- **Subtopic:** [Specific angle]
- **Evergreen?** [E] Evergreen / [D] Dated / [T] Trending

### Script Structure
- **Framework:** [Hook → Problem → Solution → CTA / Hook → Story → Lesson / etc.]
- **Full Script:** [Complete transcription]
- **Word Count:** [X words in Y seconds = Z WPM]
- **Key Phrases:** [Memorable lines]

### CTA
- **Type:** [Comment keyword / Follow / Link in bio / Share / Save / None]
- **Exact CTA:** "[Their exact words]"
- **ManyChat trigger:** [If applicable]

### Emotion Arc (from Hume)
- **Opening:** [emotion]
- **Peak:** [emotion at timestamp]
- **Close:** [emotion]

### Content Market Fit Alignment
- **Which Corner:** [YOU / AUDIENCE / OFFER — which corner does this video serve?]
- **Worldview expressed:** [What belief/value does this video reveal?]

### Recreate Prompt
- **Script template:** [Generalized version anyone could use]
- **Interview questions to ask:** [3-5 questions to get a client to produce similar content]
- **Image generation prompt:** [Nano Banana Pro prompt for thumbnail/visual]
- **Video generation prompt:** [Higgsfield/Kling prompt for animation]
```

---

## Phase 5: Database (Notion)

## Phase 6: Query Interface

## Client Intelligence (Extension for Viral Editz Clients)

Same pipeline PLUS these additional fields:

## Dave Compliance Notes

### Database Purity
- **Creator Intelligence ≠ Council.** Council = their brain (frameworks, expertise, when to consult them). Creator Intelligence = their content machine (hooks, performance, editing style, format data). A creator like @ownease can exist in BOTH — Council for his course teachings, Creator Intelligence for his content patterns.
- **Client Intelligence ≠ Client Profiles.** Client Profiles = psychology, speech patterns, proven hooks (existing DB). Client Intelligence = performance tracking, video deconstruction, competitor matching, editing style analysis. They relate to each other (Client Intelligence entries link to Client Profiles).

### Layer Placement
- Creator Intelligence DB → **Machine Layer** (HOW to execute: content patterns are tools)
- Video Deconstruction DB → **Machine Layer** (HOW to execute: deconstructed videos are reference)
- Hook Swipe File → Deferred (embedded in Video Deconstruction for now)

### Safety
- All operations are ADDITIVE. No deletions. No restructuring.
- Re-scrapes ADD new data with dated Change Log entries, never overwrite.

### Dave Gate Status
- Creator Intelligence: **PASSED** — solves real bottleneck of manual video pattern analysis
- Video Deconstruction: **PASSED** — enables systematic recreation and comparison
- Hook Swipe File: **DEFERRED** — not yet a proven bottleneck, hooks live in Video Deconstruction

---


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-13]: Context Diet — split 430 lines into routing card (190 lines) + references/full-details.md (268 lines). Zero content deleted. By skill-diet.py.

- 2026-02-06: Created. Source: Luis Carrillo brain dump session. Designed as the master extraction pipeline for both creators Drey follows and Viral Editz clients. Integrates with Content Market Fit, AI Cookbook, Video Intelligence, and all content creation skills. Notion databases designed (Creator Intelligence, Video Deconstruction, Hook Swipe File).
