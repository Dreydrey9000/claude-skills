---
name: make-portable
description: "Make any project, skill, script, or tool portable and sendable to friends. Strips personal configs, bundles dependencies, generates setup instructions, and creates a ready-to-share zip. Triggers: 'make this portable', 'send this to', 'package this for', 'share this with', 'portable', 'send to my friend', 'make sendable', 'bundle this', 'package for someone else'."
---

# Make Portable

Turn anything into a clean, self-contained package that someone else can download and run — no guesswork, no missing pieces, no "works on my machine."

## What "Portable" Means

Portable = your friend receives a zip, reads one file, follows the steps, and it works. Specifically:

1. **Zero personal config** — No hardcoded paths (`/Users/andrethomas/...`), no embedded API keys, no machine-specific references
2. **All dependencies declared** — Every library, package, CLI tool listed with exact install commands
3. **One setup file** — A single `SETUP.md` (or `SETUP.txt`) that walks them through everything step by step
4. **Tested instructions** — The setup steps are verified to actually work, not just guessed

## Process

### Step 1: Ask What We're Packaging

Ask the user:
- **"What are we making portable?"** — Get the path to the project, skill, script, or folder
- **"Who's receiving this?"** — Determines the tech level of the instructions:
  - "A friend who codes" → concise setup, assume they know terminal basics
  - "A friend who doesn't code" → ELI5 instructions, explain every step including opening terminal
  - "Someone with Claude Code" → Include SKILL.md or agent file, they can drop it right in

### Step 2: Scan & Audit

Automatically scan the target for:

**Personal Config Detection** (things that MUST be stripped/replaced):
- Hardcoded absolute paths (e.g., `/Users/andrethomas/`, `~/Library/...`)
- API keys, tokens, secrets (in `.env`, config files, or inline in code)
- Machine-specific references (local database URLs, localhost with custom ports)
- Personal usernames, emails, or account IDs embedded in code
- Browser profile paths, cookie paths, session files
- MCP server configs that reference local installs

**Dependency Detection** (things that MUST be documented):
- `package.json` → Node.js dependencies
- `requirements.txt` / `pyproject.toml` / `Pipfile` → Python dependencies
- `Gemfile` → Ruby dependencies
- `Cargo.toml` → Rust dependencies
- Import statements in code that reference external packages
- CLI tools used in scripts (`ffmpeg`, `yt-dlp`, `playwright`, `brew install X`)
- System-level requirements (Python version, Node version, OS)
- MCP servers or external services the tool talks to

**File Audit** (what to include/exclude):
- INCLUDE: Source code, config templates, README, assets
- EXCLUDE: `node_modules/`, `__pycache__/`, `.env` (real one), `.git/`, build artifacts, cache files, personal data files
- CREATE: `.env.example` from any `.env` file (keys blanked out with placeholder names)

### Step 3: Generate the Package

Create a folder at `/tmp/portable-{project-name}/` containing:

#### 1. `SETUP.md` — The One File They Need

Structure (adapt detail level based on recipient):

```markdown
# {Project Name} — Setup Guide

## What This Is
{One sentence: what it does and why it's cool}

## Prerequisites
{What they need BEFORE starting — OS, runtime versions, etc.}

- [ ] macOS / Linux / Windows (specify which)
- [ ] Node.js v{X}+ (`node --version` to check)
- [ ] Python {X}+ (`python3 --version` to check)
- [ ] {Any other system tools}

## Quick Start (< 5 minutes)

### 1. Install Dependencies
{Exact terminal commands — copy-paste ready}

### 2. Configure
{How to set up .env, API keys, etc. — what to get and where to get it}

### 3. Run
{The one command to make it go}

## Troubleshooting
{Top 3 things that might go wrong and how to fix them}
```

**Rules for SETUP.md:**
- Every command is copy-paste ready (no `<placeholder>` without explanation of what to replace)
- Version numbers are specific, not "latest"
- If an API key is needed, link to the exact page where they sign up
- Include `brew install` OR `apt-get install` OR both (based on recipient's OS if known)
- The "Run" section is ONE command. Not three. One.

#### 2. `.env.example` — Config Template

If the project uses environment variables:
```
# Get your API key at https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-key-here

# Get your key at https://supabase.com/dashboard → Settings → API
SUPABASE_URL=your-supabase-url-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here
```

Every variable gets a comment explaining WHERE to get it.

#### 3. `install.sh` — One-Click Setup Script (optional, for code-savvy recipients)

```bash
#!/bin/bash
# Auto-setup script — run: chmod +x install.sh && ./install.sh

echo "Setting up {Project Name}..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "Node.js required. Install: https://nodejs.org"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required. Install: https://python.org"; exit 1; }

# Install dependencies
{npm install / pip install -r requirements.txt / etc.}

# Create .env from template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env — fill in your API keys before running!"
fi

echo "Setup complete! Edit .env, then run: {start command}"
```

#### 4. The actual project files (cleaned)

All source code with:
- Personal paths replaced with relative paths or `$HOME`-based paths
- API keys stripped (referenced via `.env` instead)
- Comments noting anything the recipient might need to customize

### Step 4: Package It

Create a zip:
```
/tmp/portable-{project-name}.zip
```

Report to user:
- What's in the package
- What was stripped/changed for portability
- Anything the recipient will need to set up themselves (API keys, accounts, etc.)
- The exact path to the zip file

### Step 5: Verify (The Louise Check)

Before declaring it done, mentally walk through: "If Louise handed this to someone who's never seen it, could they get it running?"

Verify:
- [ ] No absolute paths to Drey's machine
- [ ] No embedded secrets
- [ ] SETUP.md has every step
- [ ] All dependencies are listed with install commands
- [ ] The "Run" command actually works
- [ ] .env.example has every needed variable with instructions
- [ ] Nothing references Claude Code internals that the recipient won't have

## Special Cases

### Packaging a Claude Code Skill
If the target is a skill from `~/.claude/skills/`:
- Include the SKILL.md file
- Include any files in the `references/` folder
- In SETUP.md, explain: "Copy this folder to `~/.claude/skills/` — you need Claude Code installed"
- List any MCP servers the skill depends on with install commands
- List any CLI tools the skill uses

### Packaging a Python Script
- Always include a `requirements.txt` (generate one if missing via `pip freeze` filtered to used packages)
- Specify Python version
- Recommend `python3 -m venv venv && source venv/bin/activate` in setup

### Packaging a Node.js Project
- Include `package.json` and `package-lock.json` (if exists)
- Specify Node version in `engines` field
- `.nvmrc` file if specific version matters

### Packaging a Full Web App
- Include database schema/migration files
- Include seed data if needed
- Document every external service (auth provider, database, storage, etc.)
- Include a `docker-compose.yml` if the setup is complex

## Output Location

All portable packages go to: `/tmp/portable-{name}.zip`

Tell the user: "Your portable package is at `/tmp/portable-{name}.zip` — send that to your friend along with this message: 'Unzip it, open SETUP.md, follow the steps.'"
