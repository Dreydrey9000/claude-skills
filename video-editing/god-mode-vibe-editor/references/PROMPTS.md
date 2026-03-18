# God-Mode Prompting Library

Copy-paste prompts that actually work with Claude Code + Remotion.

---

## SETUP PROMPTS

### Website-to-Video Pipeline
```
Head over to [URL], extract the brand guidelines (typography, colors, logo), 
and create a file called 'brand-identity'. Then, use the /remotion skill to 
build a 30-second promo video that matches this aesthetic exactly.
```

### Asset Gallery (For Large Projects)
```
Visualize all my assets in /public on an HTML gallery. 
Include the file path under each image.
```

### Install Skill
```
Install the remotion skill from this URL: [paste GitHub URL]
Then create a new remotion project and show me it's working.
```

---

## EDITING PROMPTS

### NRVES Analysis
```
Analyze this transcript using the NRVES framework:
- N: Find the ONE value/hook
- R: Apply CUB test (flag Confusing, Unbelievable, Boring)
- V: Prescribe visual fix for each flag
- E: Design triple hook (visual 0.5s, audio 1s, written 2s)
- S: Generate 3 hook variations
```

### Apply Hormozi Vibe
```
Apply the "Hormozi Vibe" to this video:
- Tighten pacing to 1.2x
- Bold yellow karaoke captions
- Zoom pulse (1.15x) on every number/result mentioned
- "Pop" sound on text appearances
```

### Apply Abdaal Vibe
```
Apply the "Abdaal Vibe" to this video:
- Clean minimal text, lots of white space
- Subtle transitions (no aggressive zooms)
- 2-3 second cuts
- Serif fonts, calm energy
```

### Make Text Bigger
```
Make the text significantly bigger for all scenes.
```

### Change Animation Style
```
Change the transition style to [slot machine / slide-in / fade / pop].
```

### Sync to Beat
```
Use /sfx to generate background music.
Align the beat of the music to the video transitions.
```

---

## CAPTION PROMPTS

### Auto-Caption
```
Transcribe this video with Whisper (word-level timestamps).
Add karaoke-style captions that highlight the current word.
Use [BRAND COLOR] as the highlight color.
Match the font to my brand guidelines.
```

### Fix Caption Timing
```
The captions are off by [X] seconds. Shift all caption timestamps 
by [X] seconds [earlier/later].
```

---

## SPLIT TEST PROMPTS

### Generate Hook Variations
```
Generate 3 different versions of the first 3 seconds:
- Version A: Result First ("I made $X doing Y")
- Version B: Contrarian ("Stop doing X. Here's why.")
- Version C: Curiosity Gap ("The secret to X that nobody talks about")
Each must have unique Visual, Audio, and Written hooks.
```

---

## ERROR RECOVERY

### Render Failed
```
The Remotion render failed with this error: [Paste Error]
Analyze the code, fix the frame math, and try again.
```

### Skill Not Loading
```
The remotion skill isn't being recognized. 
Check .claude/skills/ directory and verify the skill.md file exists.
Reinstall if needed.
```

### Video Won't Preview
```
The localhost preview is blank. Check if npm run dev is running.
If needed, kill the process and restart.
```

---

## BATCH PROMPTS

### Process Multiple Videos
```
For each video in /videos folder:
1. Transcribe with Whisper
2. Run NRVES analysis
3. Generate cut list
4. Create Remotion composition
Save all outputs to /output folder.
```

### Render All Compositions
```
Render all compositions in this project to MP4.
Output to /renders folder with naming: [composition-name]-[date].mp4
```

---

## PRO PATTERNS

### The Screenshot Technique
```
[Paste screenshot of your landing page]
Use this as the visual reference. Match colors, fonts, and style exactly.
```

### Context Management
```
We're at 50% context. Summarize what we've built so far, 
then I'll start a fresh window and paste the summary.
```

### Multi-Tool Composition
```
Use /remotion best practices
Use nano banana for background image generation
Use /sfx for sound effects with 11Labs
Create a 30-second video with music aligned to transitions.
```
