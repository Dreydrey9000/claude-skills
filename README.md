# Claude Skills Library

Portable, shareable Claude Code skills and tools. Each skill is self-contained and can be dropped into anyone's `~/.claude/skills/` directory.

## Skills

| Skill | Description |
|-------|-------------|
| [make-portable](./make-portable/) | Package any project, script, or tool into a clean, sendable bundle with setup instructions |

## How to Install a Skill

1. Clone this repo (or download the skill folder you want)
2. Copy the skill folder into `~/.claude/skills/`
3. Restart Claude Code
4. The skill is now available as a slash command

```bash
# Example: install make-portable
cp -r make-portable ~/.claude/skills/make-portable
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) installed and configured
