# ElevenLabs TTS — Voice Clone Audio Generation

Generate production-quality AI voiceovers using ElevenLabs cloned voices with automatic QC, chunking, and crossfade stitching.

## When to Use

Use this skill when the user wants to:
- Generate AI voiceover audio from a script
- Create TTS audio using a cloned voice (Ryan Magin, Luis, or any clone)
- Run audio QC on generated speech
- Convert a YAP script or any text into spoken audio
- Produce audio for HeyGen avatar videos

Triggers: "generate audio", "elevenlabs", "TTS", "text to speech", "voiceover", "voice clone audio", "read this in Ryan's voice", "make audio from this script"

## API Key

ElevenLabs API key: `aba208275bd6b2a39fc033067eda714bb9a40f6be0a9d518eb3c08cac674cc53`

## Critical Voice Settings (Learned from Production)

These settings were dialed in through multiple production sessions with Ryan Magin's cloned voice. DO NOT deviate unless testing.

```python
VOICE_SETTINGS = {
    "stability": 0.55,        # Balanced — not monotone, not random
    "similarity_boost": 0.75,  # Sweet spot for clones (higher = distortion)
    "style": 0.0,             # MUST BE ZERO for cloned voices
    "use_speaker_boost": True,
}
```

### Why These Settings

| Setting | Value | Reason |
|---------|-------|--------|
| **style** | **0.0** | ElevenLabs docs confirm: style > 0 on cloned voices causes "inconsistent speed, mispronunciation, and extra sounds." We tested 0.25, 0.40, 0.65 — all produced artifacts. Zero is mandatory. |
| **similarity_boost** | **0.75** | Docs say this is the sweet spot. We tested 0.85 and 0.90 — both caused voice distortion on clones. |
| **stability** | **0.55** | Lower = more expressive but can hallucinate. Higher = monotone. 0.55 is the balance point. On retries, bump by +0.05 per attempt (max 0.75). |

## Model Selection

**ALWAYS use `eleven_multilingual_v2`** for cloned voices.

| Model | Use Case | Clone Compatible? |
|-------|----------|-------------------|
| `eleven_multilingual_v2` | Cloned voices | YES — only model that preserves clone |
| `eleven_turbo_v2_5` | Fast English (premade voices) | NO — changes clone voice |
| `eleven_flash_v2_5` | Low latency (premade voices) | NO — changes clone voice |
| `eleven_v3` | Newest (premade voices) | NO — 400 error on clones |

## Script Preprocessing Rules

Before sending ANY script to the API, apply these transformations:

1. **Remove em-dashes** (`—` and `–`) → replace with commas
2. **Remove ALL CAPS** → convert to Title Case (caps cause unnatural emphasis artifacts)
3. **Write out all numbers** → "twelve" not "12", "five figure" not "5-figure"
4. **Expand contractions** → "do not" instead of "don't", "can not" instead of "can't" (multilingual model misreads contractions as other languages)
5. **No special punctuation** → no ellipsis (...), no semicolons, no colons mid-sentence
6. **Keep sentences short** → one idea per sentence for natural pacing

### How It Works:

1. **Split on sentence boundaries** — never mid-sentence
2. **Each chunk under 700 characters**
3. **Context seeding** — chunks 2+ include the last sentence of the previous chunk as a lead-in so the model carries the same tone/energy forward
4. **STT timestamp trimming** — transcribe the context-seeded chunk, find where the new content starts using word-level timestamps, trim the lead-in
5. **Crossfade stitch** — 150ms triangular crossfade between chunks (NOT silence gaps — those create audible pauses)
6. **Tail trim** — cut last 0.4s from final chunk to remove end-of-generation artifacts

### Why Context Seeding

Without it, each chunk generates independently and can drift in tone/energy. By prepending the last sentence of the previous chunk, the model "warms up" on the established tone before hitting the new content.

## Complete Workflow

### Step 1: Preprocess the Script
```
Apply preprocessing rules above. Remove caps, em-dashes, expand contractions, write out numbers.
```

### Step 2: Generate Audio
```bash
# Short script (under 700 chars) — single pass
python3 ~/Desktop/Vision-Agents/audio_qc.py \
  --script script.txt \
  --elevenlabs-key "aba208275bd6b2a39fc033067eda714bb9a40f6be0a9d518eb3c08cac674cc53" \
  --voice-id "FaqEcpH1etobBPMBMfJg" \
  --output-dir ./output \
  --threshold 0.92

# Long script — auto-chunks, context-seeds, crossfade stitches
# (same command — chunking is automatic based on length)
```

### Step 3: QC Loop (Automatic)
The script automatically:
1. Generates TTS audio
2. Transcribes it back via ElevenLabs STT (scribe_v1)
3. Diffs transcript against original script
4. If similarity < 92%, bumps stability +0.05 and retries (max 3 attempts)
5. Reports all word-level issues found

### Step 4: Manual Listen Check
Even with 92%+ similarity, ALWAYS listen to the final audio. The QC catches word accuracy but NOT:
- Unnatural pacing
- Weird tonal shifts between chunks
- Robotic delivery
- Trailing artifacts

### Step 5 (Optional): HeyGen Video
```bash
python3 ~/Desktop/Vision-Agents/audio_qc.py \
  --script script.txt \
  --elevenlabs-key "API_KEY" \
  --heygen \
  --heygen-key "sk_V2_hgu_ktgAobLdFV4_R7sCHf1JE0DJYsG8UUp6YmPtHVs56nsC" \
  --avatar-id "f1edc6880c3e49b0835f975b7f8d26f1" \
  --output-dir ./output
```

**HeyGen Watermark Note:** Watermark removal via API requires Enterprise plan. For watermark-free videos on Creator plan, upload the audio manually through the HeyGen web UI and toggle watermark off there.

## Production Learnings (Clone Content)

### Stability Sweet Spot by Content Type

| Content Type | Stability | Why |
|-------------|-----------|-----|
| Clone response / commentary | **0.65** | Grounded energy, conviction, "soul" — not flat, not loose |
| Standard narration | 0.55 | Default balanced setting |
| Energetic / hype | 0.45-0.50 | More dynamic range, but can go too loose — test first |

**Key Learning (2026-02-03):** When generating Ryan Magin clone content (AI clone responding to comments/haters), stability 0.65 with similarity 0.75 produced the best "soul" — punchy, confident, grounded. Stability 0.45 went too loose and lost the conviction. The script matters as much as the settings — short punchy sentences ("You are telling on yourself right now." / "You are good. Go away.") give the model room to breathe and hit.

### Tail Trim Fix

Default pipeline trims 0.4s from the end of the final chunk to remove generation artifacts. This can cut off the last word. **Fix:** Restitch manually with only 0.1s trim:

```bash
# Get raw chunks from best attempt, trim context seed from chunk 2,
# only 0.1s off the very end, crossfade stitch at 150ms
ffmpeg -y -i chunk0.wav -i chunk1_trimmed.wav \
  -filter_complex "[0][1]acrossfade=d=0.15:c1=tri:c2=tri" \
  -b:a 192k output.mp3
```

### QC Score False Alarms

The QC similarity score will report low (10-55%) when the script uses written-out numbers ("twenty five") because STT transcribes them back as digits ("25"). Also "CRI" transcribes as "cry" and "can not" as "cannot." These are transcription interpretation differences, NOT mispronunciations. **Listen to the audio** — if the words sound right, the score is misleading.

## Files

- **QC Script:** `~/Desktop/Vision-Agents/audio_qc.py`
- **Viral Scripts DB:** `~/.claude/skills/yap-generator/references/viral-scripts-database.md`

## Asset Registry (Backups on Backups)

Every asset lives in ALL FOUR locations. When updating, update ALL of them.

| Location | Path / URL | What Lives There |
|----------|-----------|-----------------|
| **Claude Code Skill** | `~/.claude/skills/elevenlabs-tts/SKILL.md` | Source of truth — full workflow, settings, registry |
| **GitHub** | `https://github.com/itsluisc/claude-code-skills/tree/main/elevenlabs-tts` | SKILL.md + audio_qc.py |
| **Notion Knowledge Library** | `https://www.notion.so/ElevenLabs-TTS-Voice-Clone-Audio-Generation-2fb17674eab481cfb613cfa14cc11aca` | Done-For-You Course Standard (4 parts) |
| **Notion Master Frameworks** | `https://www.notion.so/Audio-QC-Protocol-ElevenLabs-TTS-Pipeline-2fb17674eab481e5a30ce77cd072ddf2` | Framework entry (Machinery layer) |
| **Google Drive** | `https://drive.google.com/drive/folders/1Fc7IPeaIRSq3oTq4rx2abyBIxmwl5Ngn` | SKILL.md + audio_qc reference (inside Notion/Knowledge Library/) |

### Notion API Token

`ntn_X62823410449D6uWLOLVFYAyo0pQPnxzGGFt59gWUPk8AI`

### Key IDs

| Resource | ID |
|----------|-----|
| Knowledge Library DB | `96d5b537-b85a-435a-ac99-7f2c811341b6` |
| Master Frameworks DB | `5553912e-1355-4033-a743-90ff7d133e72` |
| Knowledge Library Page | `2fb17674eab481cfb613cfa14cc11aca` |
| Master Frameworks Page | `2fb17674eab481e5a30ce77cd072ddf2` |
| Google Drive Folder | `1Fc7IPeaIRSq3oTq4rx2abyBIxmwl5Ngn` |
| Google Drive Parent (Notion/) | `1yRNhguvEWZ00gBJtWRHzsGB-J-igb5Dt` |
| Google Drive Parent (Knowledge Library/) | `1RRJeqTCMIBUIByxzSXLSDi9NzHHPWl0e` |
| GitHub Repo | `itsluisc/claude-code-skills` |


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
