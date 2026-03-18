---
name: audio-transcriber
description: "Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration"
category: content
risk: safe
source: community
tags: "[audio, transcription, whisper, meeting-minutes, speech-to-text]"
date_added: "2026-02-27"
---

## Purpose

This skill automates audio-to-text transcription with professional Markdown output, extracting rich technical metadata (speakers, timestamps, language, file size, duration) and generating structured meeting minutes and executive summaries. It uses Faster-Whisper or Whisper with zero configuration, working universally across projects without hardcoded paths or API keys.

Inspired by tools like Plaud, this skill transforms raw audio recordings into actionable documentation, making it ideal for meetings, interviews, lectures, and content analysis.

## When to Use

Invoke this skill when:

- User needs to transcribe audio/video files to text
- User wants meeting minutes automatically generated from recordings
- User requires speaker identification (diarization) in conversations
- User needs subtitles/captions (SRT, VTT formats)
- User wants executive summaries of long audio content
- User asks variations of "transcribe this audio", "convert audio to text", "generate meeting notes from recording"
- User has audio files in common formats (MP3, WAV, M4A, OGG, FLAC, WEBM)

## Workflow

### Step 3: Generate Markdown Output

**Objective:** Create structured Markdown with metadata, transcription, meeting minutes, and summary.

**Output Template:**

```markdown
# Audio Transcription Report

## 📊 Metadata

| Field | Value |
|-------|-------|
| **File Name** | {filename} |
| **File Size** | {file_size} |
| **Duration** | {duration_hms} |
| **Language** | {language} ({language_code}) |
| **Processed Date** | {process_date} |
| **Speakers Identified** | {num_speakers} |
| **Transcription Engine** | {engine} (model: {model}) |


## 📋 Meeting Minutes

### Participants
- {speaker_1}
- {speaker_2}
- ...

### Topics Discussed
1. **{topic_1}** ({timestamp})
   - {key_point_1}
   - {key_point_2}

2. **{topic_2}** ({timestamp})
   - {key_point_1}

### Decisions Made
- ✅ {decision_1}
- ✅ {decision_2}

### Step 5: Display Results Summary

**Objective:** Show completion status and next steps.

**Output:**

```bash
echo ""
echo "✅ Transcription Complete!"
echo ""
echo "📊 Results:"
echo "  File: $OUTPUT_FILE"
echo "  Language: $LANGUAGE"
echo "  Duration: $DURATION_HMS"
echo "  Speakers: $NUM_SPEAKERS"
echo "  Words: $WORD_COUNT"
echo "  Processing time: ${ELAPSED_TIME}s"
echo ""
echo "📝 Generated:"
echo "  - $OUTPUT_FILE (Markdown report)"
[if alternative formats:]
echo "  - ${OUTPUT_FILE%.*}.srt (Subtitles)"
echo "  - ${OUTPUT_FILE%.*}.json (Structured data)"
echo ""
echo "🎯 Next steps:"
echo "  1. Review meeting minutes and action items"
echo "  2. Share report with participants"
echo "  3. Track action items to completion"
```


## Example Usage

### **Example 3: Batch Processing**

**User Input:**
```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**Skill Output:**

```bash
📦 Batch mode: 5 files found
  1. team-standup.mp3
  2. client-call.mp3
  3. brainstorm-session.mp3
  4. product-demo.mp3
  5. retrospective.mp3

🎙️  Processing batch...

[1/5] team-standup.mp3 ✅ (2m 34s)
[2/5] client-call.mp3 ✅ (15m 12s)
[3/5] brainstorm-session.mp3 ✅ (8m 47s)
[4/5] product-demo.mp3 ✅ (22m 03s)
[5/5] retrospective.mp3 ✅ (11m 28s)

✅ Batch Complete!
📝 Generated 5 Markdown reports
⏱️  Total processing time: 6m 15s
```


### **Example 5: Large File Warning**

**User Input:**
```bash
copilot> transcribe audio to markdown: conference-keynote.mp3
```

**Skill Output:**

```bash
✅ Faster-Whisper detected (optimized)

📂 File: conference-keynote.mp3
📊 Size: 87.2 MB
⏱️  Duration: 02:15:47
⚠️  Large file (87.2 MB) - processing may take several minutes

Continue? [Y/n]:
```

**User:** `Y`

```bash
🎙️  Processing... (this may take 10-15 minutes)
[████░░░░░░░░░░░░░░░░] 20% - Estimated time remaining: 12m
```


This skill is **platform-agnostic** and works in any terminal context where GitHub Copilot CLI is available. It does not depend on specific project configurations or external APIs, following the zero-configuration philosophy.


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
