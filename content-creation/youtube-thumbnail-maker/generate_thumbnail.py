#!/usr/bin/env python3
"""
YouTube Thumbnail Generator using Gemini (BananaBananaPro).

Generates thumbnails from text descriptions, reference photos, competitor style cloning,
and supports iterative editing.

Usage:
    # From text description
    python generate_thumbnail.py --prompt "Person looking at timer on phone" --title "20 Minutes"

    # With reference photo
    python generate_thumbnail.py --prompt "Person shocked" --title "This Changed Everything" -r photo.jpg

    # Clone competitor style
    python generate_thumbnail.py --clone competitor_thumb.jpg --prompt "Same style, my topic" --title "My Title"

    # Edit existing
    python generate_thumbnail.py --edit thumb.jpg --prompt "Make text bigger"

    # From YouTube URL
    python generate_thumbnail.py --youtube "https://youtube.com/watch?v=ID" --title "My Version"
"""

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types

# Load env
for env_path in ['.env', os.path.expanduser('~/.env'), os.path.expanduser('~/.claude/.env')]:
    if os.path.exists(env_path):
        load_dotenv(env_path)

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("NANO_BANANA_API_KEY")
MODEL = "gemini-3-pro-image-preview"
OUTPUT_BASE = Path(".tmp/thumbnails")

# YouTube thumbnail best practices baked into every prompt
THUMBNAIL_SYSTEM = """You are generating a YouTube thumbnail image. Follow these rules:
- 16:9 aspect ratio (landscape, wide format)
- HIGH CONTRAST - must be readable at small sizes on mobile
- Maximum 3-5 words of bold text overlay if text is included
- Close-up emotional faces outperform everything else for clicks
- Bold colors: yellows, reds, whites on dark backgrounds pop
- Rule of thirds: subject on one side, text on the other
- Clean, uncluttered composition - one focal point
- Professional quality, photorealistic style unless told otherwise
- The thumbnail should make someone STOP scrolling"""


def get_client():
    if not API_KEY:
        print("Error: Set GEMINI_API_KEY or NANO_BANANA_API_KEY in your environment or ~/.claude/.env")
        sys.exit(1)
    return genai.Client(api_key=API_KEY)


def get_output_dir():
    today = datetime.now().strftime("%Y%m%d")
    output_dir = OUTPUT_BASE / today
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_image(response, output_dir, suffix="v1"):
    timestamp = datetime.now().strftime("%H%M%S")
    saved = []
    img_count = 0
    for part in response.parts:
        if hasattr(part, 'text') and part.text:
            print(f"  Gemini says: {part.text[:200]}")
        elif hasattr(part, 'inline_data') and part.inline_data:
            img_count += 1
            filename = f"{timestamp}_{suffix}.jpg" if img_count == 1 else f"{timestamp}_{suffix}_{img_count}.jpg"
            filepath = output_dir / filename
            # Gemini returns JPEG by default - save with .jpg
            img = part.as_image()
            img.save(str(filepath))
            saved.append(str(filepath))
            print(f"  Saved: {filepath}")
    return saved


def download_youtube_thumbnail(url):
    """Download thumbnail from a YouTube URL using yt-dlp."""
    output_dir = get_output_dir()
    thumb_path = output_dir / "source_yt_thumb.jpg"
    try:
        cmd = ["yt-dlp", "--write-thumbnail", "--skip-download", "--convert-thumbnails", "jpg",
               "-o", str(output_dir / "source_yt"), url]
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        # Find the downloaded thumbnail
        for f in output_dir.glob("source_yt*.jpg"):
            return str(f)
    except Exception as e:
        print(f"Warning: Could not download thumbnail: {e}")
    return None


def generate_thumbnail(prompt, title=None, subtitle=None, style=None,
                       reference_paths=None, clone_path=None, variations=3,
                       resolution="2K"):
    """Generate thumbnail(s) from scratch."""
    client = get_client()
    output_dir = get_output_dir()

    # Build the prompt
    full_prompt = f"{THUMBNAIL_SYSTEM}\n\n"
    full_prompt += f"Generate a YouTube thumbnail with this description:\n{prompt}\n"

    if title:
        full_prompt += f"\nBold text overlay on the thumbnail: \"{title}\"\n"
        full_prompt += "Make this text large, bold, and highly readable. Use a contrasting color.\n"

    if subtitle:
        full_prompt += f"\nSmaller subtitle text: \"{subtitle}\"\n"

    if style:
        full_prompt += f"\nStyle: {style}\n"

    full_prompt += "\nIMPORTANT: Output must be 16:9 landscape format. Photorealistic quality."

    # Build content list
    contents = []

    if clone_path:
        clone_img = Image.open(clone_path)
        contents.append(f"IMAGE 1 (STYLE REFERENCE - clone this thumbnail's style, layout, and composition): ")
        contents.append(clone_img)
        contents.append("\n")

    if reference_paths:
        for i, ref_path in enumerate(reference_paths):
            ref_img = Image.open(ref_path)
            label = f"IMAGE {len(contents)//2 + 1} (REFERENCE PHOTO of the person to feature in the thumbnail):"
            contents.append(label)
            contents.append(ref_img)
            contents.append("\n")

    contents.append(full_prompt)

    all_saved = []
    for v in range(1, variations + 1):
        print(f"\nGenerating variation {v}/{variations}...")
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio="16:9",
                    ),
                ),
            )
            saved = save_image(response, output_dir, suffix=f"v{v}")
            all_saved.extend(saved)
        except Exception as e:
            print(f"  Error on variation {v}: {e}")

    return all_saved


def edit_thumbnail(edit_path, prompt, resolution="2K"):
    """Edit an existing thumbnail."""
    client = get_client()
    output_dir = get_output_dir()

    img = Image.open(edit_path)
    full_prompt = f"Edit this YouTube thumbnail: {prompt}\n"
    full_prompt += "Keep the 16:9 aspect ratio. Keep it professional and high-contrast."

    print(f"\nEditing: {edit_path}")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[full_prompt, img],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size=resolution
                ),
            ),
        )
        return save_image(response, output_dir, suffix="edited")
    except Exception as e:
        print(f"  Error: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="YouTube Thumbnail Generator (Gemini)")
    parser.add_argument("--prompt", "-p", help="Description of the thumbnail")
    parser.add_argument("--title", "-t", help="Bold text overlay on thumbnail")
    parser.add_argument("--subtitle", help="Secondary text")
    parser.add_argument("--reference", "-r", nargs="+", help="Reference photo(s) of creator")
    parser.add_argument("--clone", "-c", help="Competitor thumbnail to clone style from")
    parser.add_argument("--youtube", "-y", help="YouTube URL to clone thumbnail from")
    parser.add_argument("--edit", "-e", help="Existing thumbnail to edit")
    parser.add_argument("--style", "-s", help="Style keywords")
    parser.add_argument("--variations", "-n", type=int, default=3, help="Number of variations")
    parser.add_argument("--resolution", default="2K", choices=["1K", "2K", "4K"])
    parser.add_argument("--output", "-o", help="Custom output path")

    args = parser.parse_args()

    # Edit mode
    if args.edit:
        if not args.prompt:
            print("Error: --prompt is required for edit mode")
            sys.exit(1)
        results = edit_thumbnail(args.edit, args.prompt, args.resolution)
        if results:
            print(f"\nDone! {len(results)} edit(s) saved.")
        return

    # YouTube clone mode
    clone_path = args.clone
    if args.youtube:
        print(f"Downloading thumbnail from: {args.youtube}")
        clone_path = download_youtube_thumbnail(args.youtube)
        if clone_path:
            print(f"  Downloaded: {clone_path}")

    # Generate mode
    if not args.prompt:
        print("Error: --prompt is required")
        sys.exit(1)

    results = generate_thumbnail(
        prompt=args.prompt,
        title=args.title,
        subtitle=args.subtitle,
        style=args.style,
        reference_paths=args.reference,
        clone_path=clone_path,
        variations=args.variations,
        resolution=args.resolution,
    )

    if results:
        print(f"\nDone! {len(results)} thumbnail(s) generated:")
        for r in results:
            print(f"  {r}")
    else:
        print("\nNo thumbnails generated. Check errors above.")


if __name__ == "__main__":
    main()
