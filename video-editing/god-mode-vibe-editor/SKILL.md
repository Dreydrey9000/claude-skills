# God-Mode Vibe Editing Skill (Viral Editz Edition)

The God-Mode Vibe Editor is the ultimate synthesis of the **NRVES™ Master System** and **Programmatic Video Automation** (Claude Code + Remotion + FFmpeg). It transforms raw footage into viral assets by treating every frame as code and every edit as a strategic "vibe" decision.

## THE NRVES™ MASTER SYSTEM (Core Methodology)

### 1. N - NARRATIVE (The Brain)
- **Hook-First Assembly**: Identify the "Payoff" (the most valuable/emotional moment) first. Move it to the first 3 seconds.
- **Triple Hook Layer**:
    - **Visual**: High-contrast text/graphic in first 0.5s.
    - **Audio**: Sound effect or punchy first word in first 1s.
    - **Written**: Compelling caption hook in first 2s.

### 2. R - RESTRUCTURE (The Scissors)
- **The CUB Test™**:
    - **Confusing**: Add context overlay or cut.
    - **Unbelievable**: Add proof card (screenshot/stat) or cut.
    - **Boring**: Cut immediately or add pattern interrupt.
- **Tight Pacing**: Apply 1.1x - 1.2x speed to talking head sections to remove "dead air" without sounding chipmunk-like.
- **2-Second Rule**: Something must change every 2 seconds (Visual, Info, or Energy).

### 3. V - VISUAL STORYTELLING (The Paint)
- **Programmatic Graphics**: Use Remotion components for:
    - **Proof Cards**: Slide-in screenshots for "Unbelievable" moments.
    - **Context Bars**: Top/bottom bars for "Confusing" terms.
    - **Zoom Pulses**: 1.15x scale pulses on key emphasis words.
- **Energy Matching**:
    - **High Energy (Hormozi)**: Fast cuts (1s), bold yellow/white text, heavy zoom pulses.
    - **Educational (Abdaal)**: Clean minimal text, subtle transitions, 2-3s cuts.

### 4. E - ENHANCE (The Polish)
- **Karaoke Subtitles**: Highlight current word in brand color (e.g., Viral Editz Yellow).
- **Progress Bars**: Add a subtle top progress bar to signal video length and increase retention.
- **Sound Design**: Auto-inject "Whoosh" on transitions and "Pop" on text appearances.

### 5. S - SUBMIT (The Split)
- **Split Test Generation**: Always generate 3 hook variations (Result First, Contrarian, Curiosity Gap).
- **Technical QC**: Verify 9:16 aspect ratio, safe zones for UI elements, and perfect audio leveling.

## ADVANCED WORKFLOWS (Programmatic IP)

### Website-to-Video Pipeline
1. **Extract**: Scrape brand guidelines (typography, colors, logo) from a URL.
2. **Visualize**: Create an HTML asset gallery of all images in `/public`.
3. **Compose**: Use the "Screenshot Technique" to feed Claude the visual reference.
4. **Render**: Generate the Remotion code and render the final MP4.

### The "Digital Twin" Editing
- **Prompt-Based Iteration**: Instead of manual timeline editing, use natural language: *"Make the text bigger," "Add a slot machine effect," "Sync the beat to the transitions."*
- **Context Management**: When context usage hits 50%, refresh the window to maintain performance.

## WORKFLOW COMMANDS

### /transcribe-videos
Downloads, transcribes, and runs NRVES analysis on any YouTube URL or playlist.
- **Usage**: `/transcribe-videos <url>`
- **Output**: `~/.claude/video-transcripts/`

### /vibe-edit
Processes a transcript or video file through the full NRVES pipeline.
- **Usage**: `/vibe-edit <file_path> --style [hormozi|minimal|clean]`

## THE THREE LAWS OF VIBE EDITING
1. **Hook or Die**: The first 3 seconds are 90% of the result.
2. **Change = Retention**: Stagnation is the enemy.
3. **Prove or Cut**: If they don't believe you, they won't follow you.
