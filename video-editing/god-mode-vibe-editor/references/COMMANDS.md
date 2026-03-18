# EXACT COMMANDS REFERENCE
## Copy-Paste Ready Commands from Transcripts

---

## INSTALLATION

### Create New Project
```bash
# NPM
npx create-video@latest

# Bun (faster)
bun create video
```

### Install Dependencies
```bash
npm install
# or
bun i
```

### Add Remotion Skill
```bash
npx skills add remotion-dev/skills
# or
bunx skills add remotion-dev/skills
```

### Start Dev Server
```bash
npm run dev
# Opens localhost:3000
```

### Start Claude Code
```bash
# Normal
claude

# Skip all permission prompts
claude --dangerously-skip-permissions

# Short form
claude -y
```

---

## RENDERING

### Render to MP4
```bash
npx remotion render src/index.ts MyVideo out/video.mp4
```

### Render with options
```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --codec=h264
```

---

## CLAUDE CODE COMMANDS

### Check Skills
```
/skills
```

### Use Remotion Skill
```
/remotion best practices
```

---

## TOOL INSTALLATION

### Whisper (Transcription)
```bash
pip install openai-whisper
```

### yt-dlp (Video Download)
```bash
pip install yt-dlp
```

### FFmpeg (Video Processing)
```bash
# Mac
brew install ffmpeg

# Windows
# Download from ffmpeg.org
```

### Node.js
```bash
# Required for Remotion
# Download from nodejs.org
```

---

## CLAUDE DESKTOP SETUP

1. Open Claude Desktop App
2. Click "Code" button
3. Select/create a folder
4. Start coding!

---

## VS CODE EXTENSION

1. Open VS Code
2. Extensions → Search "Claude"
3. Install Claude extension
4. Double-click in editor to open Claude
5. Or click Claude icon in sidebar

---

## MCP SERVER CONFIG

```bash
# View MCP config
claude config

# In VS Code Claude extension:
# Click Claude icon → MCP Servers → Manage MCP Servers → View Raw Config
```

---

## PERMISSION SETTINGS

### Trust Workspace
```bash
# When prompted, select "Trust this workspace"
```

### Auto-approve Edits
```bash
# In Claude Code, select "Edit automatically" instead of "Ask before edits"
```

### Global Auto-approve
```bash
claude config set --global autoApprove true
```

---

## FILE PATHS

### Skill Location
```
.claude/skills/remotion-best-practices/
```

### Project Structure
```
my-video/
├── src/
│   ├── index.ts
│   └── Composition.tsx
├── public/          # Put assets here
├── .claude/
│   └── skills/
└── package.json
```

---

## USEFUL ALIASES

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Quick Claude Code
alias cc='claude'
alias ccy='claude --dangerously-skip-permissions'

# Remotion shortcuts
alias rdev='npm run dev'
alias rrender='npx remotion render'
```
