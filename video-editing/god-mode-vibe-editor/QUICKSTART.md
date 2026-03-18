# Quick Start Guide

## 1. Install Prerequisites
```bash
# Node.js (required)
# Download from nodejs.org

# FFmpeg (for video processing)
brew install ffmpeg  # Mac
# or download from ffmpeg.org

# Whisper (for transcription)
pip install openai-whisper
```

## 2. Create Remotion Project
```bash
npx create-video@latest
# Select: blank, yes TailwindCSS, yes Skills
cd my-video
npm install
```

## 3. Add Remotion Skill
```bash
npx skills add remotion-dev/skills
```

## 4. Start Working
```bash
# Terminal 1: Start Remotion Studio
npm run dev

# Terminal 2: Start Claude Code
claude --dangerously-skip-permissions
```

## 5. Install /transcribe-videos Command
```bash
mkdir -p ~/.claude/commands
cp scripts/transcribe_videos.py ~/.claude/commands/
chmod +x ~/.claude/commands/transcribe_videos.py
```

## First Prompt to Try
```
Use /remotion best practices. 
Go to [your-website-url], extract brand colors and logo.
Create a 15-second promo video with a "Result First" hook.
```

That's it. You're vibe editing.
