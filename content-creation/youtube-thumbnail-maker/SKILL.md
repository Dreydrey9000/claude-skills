# YouTube Thumbnail Maker

Generate YouTube thumbnails from scratch using Gemini (BananaBananaPro). Supports reference photos for face consistency, style cloning from competitor thumbnails, and iterative editing.

## When to Use
- User says "make a thumbnail", "generate thumbnail", "thumbnail for this video"
- User shares a video concept and needs a thumbnail
- User wants to clone a competitor's thumbnail style with their own face/branding

## Quick Start

```bash
# Generate from a text description
python3 ~/.claude/skills/youtube-thumbnail-maker/generate_thumbnail.py \
  --prompt "Person looking at phone timer showing 17:43, videos uploading in background" \
  --title "How I Post Every Day in Under 20 Minutes" \
  --style "clean, high-contrast, bold text overlay"

# Generate with a reference photo of the creator
python3 ~/.claude/skills/youtube-thumbnail-maker/generate_thumbnail.py \
  --prompt "Person looking shocked at their phone" \
  --title "This Changed Everything" \
  --reference path/to/creator_photo.jpg

# Clone style from a competitor thumbnail
python3 ~/.claude/skills/youtube-thumbnail-maker/generate_thumbnail.py \
  --clone path/to/competitor_thumbnail.jpg \
  --prompt "Recreate this style but with different person and text" \
  --title "My Version of This Topic" \
  --reference path/to/my_photo.jpg

# Edit an existing thumbnail
python3 ~/.claude/skills/youtube-thumbnail-maker/generate_thumbnail.py \
  --edit path/to/generated_thumb.jpg \
  --prompt "Make the text bigger, change background to dark blue"

# Generate from YouTube URL (downloads their thumbnail, clones the style)
python3 ~/.claude/skills/youtube-thumbnail-maker/generate_thumbnail.py \
  --youtube "https://youtube.com/watch?v=VIDEO_ID" \
  --prompt "Same style but about posting daily" \
  --title "How I Post Every Day"
```

## Parameters

| Flag | Description |
|------|-------------|
| `--prompt`, `-p` | Description of what the thumbnail should show |
| `--title`, `-t` | Text overlay for the thumbnail (the YouTube title shown ON the image) |
| `--subtitle` | Secondary text (smaller, below title) |
| `--reference`, `-r` | Reference photo(s) of the creator for face consistency |
| `--clone`, `-c` | Competitor thumbnail to clone the style of |
| `--youtube`, `-y` | YouTube URL to download thumbnail from and clone style |
| `--edit`, `-e` | Existing thumbnail to edit/refine |
| `--style`, `-s` | Style keywords (e.g. "clean, bold, dark background, neon accents") |
| `--variations`, `-n` | Number of variations to generate (default: 3) |
| `--resolution` | Output resolution: 1K, 2K, 4K (default: 2K) |
| `--output`, `-o` | Custom output path |

## Output

Thumbnails saved to `.tmp/thumbnails/YYYYMMDD/` organized by date.
- `HHMMSS_v1.jpg`, `HHMMSS_v2.jpg`, `HHMMSS_v3.jpg` for variations
- `HHMMSS_edited.jpg` for edit passes

## Thumbnail Best Practices (Built Into Prompts)

1. **16:9 aspect ratio** (1280x720 native YouTube)
2. **High contrast** - must read at small sizes (mobile)
3. **Max 3-5 words** of text on thumbnail
4. **Face = clicks** - close-up emotional faces outperform
5. **Complementary to title** - thumbnail shows, title tells
6. **Bold colors** - yellow, red, white on dark backgrounds
7. **Rule of thirds** - subject on left or right third, text on opposite

## API

- **Model:** `gemini-3-pro-image-preview`
- **API Key:** `GEMINI_API_KEY` env var (from `~/.claude/.env`)
- **Cost:** ~$0.14-0.24 per generation
- **Format:** 16:9, 2K default resolution
