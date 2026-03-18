#!/usr/bin/env python3
"""
Thread Carousel Renderer
========================
Renders Twitter/X-style thread carousels from config.json.
Produces 1080x1350 PNG slides with profile pics, verified badges,
word-wrapped text with emoji support, and embedded images.

Usage:
    python3 render_carousel.py <config.json>

Inspired by Tyler Germain's carousel generator architecture.
"""

import json
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

# =============================================================================
# CONSTANTS
# =============================================================================

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1350
MARGIN_X = 72
MARGIN_Y = 72
CONTENT_WIDTH = CANVAS_WIDTH - (MARGIN_X * 2)

AVATAR_SIZE = 56
BADGE_SIZE = 20
IMAGE_CORNER_RADIUS = 16
MAX_IMAGE_HEIGHT = 500

# Font sizes (tuned for 1080px canvas, readable on mobile)
NAME_FONT_SIZE = 21
HANDLE_FONT_SIZE = 17
TWEET_FONT_SIZE = 26
TWEET_LINE_HEIGHT = 1.35

# Spacing
PROFILE_ROW_BOTTOM_PAD = 14
TWEET_TEXT_TOP_PAD = 4
IMAGE_TOP_PAD = 16
IMAGE_BOTTOM_PAD = 8
TWEET_BOTTOM_PAD = 20
DIVIDER_VERTICAL_PAD = 16
SLIDE_NUMBER_SIZE = 14

# =============================================================================
# THEMES
# =============================================================================

THEMES = {
    "dark": {
        "bg": "#15202B",
        "text": "#E7E9EA",
        "secondary": "#71767B",
        "divider": "#2F3336",
        "badge": "#1D9BF0",
        "slide_num": "#3D4750",
    },
    "light": {
        "bg": "#FFFFFF",
        "text": "#0F1419",
        "secondary": "#536471",
        "divider": "#EFF3F4",
        "badge": "#1D9BF0",
        "slide_num": "#C4CDD5",
    },
    "black": {
        "bg": "#000000",
        "text": "#E7E9EA",
        "secondary": "#71767B",
        "divider": "#2F3336",
        "badge": "#1D9BF0",
        "slide_num": "#3D4750",
    },
}

# =============================================================================
# HELPERS
# =============================================================================


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def create_circular_mask(size):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def load_profile_pic(path, size):
    path = os.path.expanduser(path)
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((size, size), Image.LANCZOS)

    mask = create_circular_mask(size)
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output


def round_corners(img, radius):
    img = img.convert("RGBA")
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w, h)], radius, fill=255)
    img.putalpha(mask)
    return img


def draw_verified_badge(img, x, y, size, color):
    """Draw a verified checkmark badge directly on the image."""
    draw = ImageDraw.Draw(img)
    # Blue circle
    draw.ellipse([x, y, x + size, y + size], fill=color)
    # White checkmark
    cx, cy = x + size / 2, y + size / 2
    s = size * 0.28
    # Checkmark path: short stroke down-right, then long stroke up-right
    check_points = [
        (cx - s * 0.7, cy - s * 0.05),
        (cx - s * 0.1, cy + s * 0.65),
        (cx + s * 0.9, cy - s * 0.55),
    ]
    draw.line(
        [check_points[0], check_points[1]],
        fill="white",
        width=max(2, int(size * 0.14)),
    )
    draw.line(
        [check_points[1], check_points[2]],
        fill="white",
        width=max(2, int(size * 0.14)),
    )


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels. Respects explicit newlines."""
    all_lines = []

    # Split on explicit newlines first
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            all_lines.append("")  # Blank line for spacing
            continue

        words = paragraph.split()
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    all_lines.append(current_line)
                current_line = word
        if current_line:
            all_lines.append(current_line)

    return all_lines


def load_fonts():
    """Load fonts — SF Pro Display preferred, Helvetica fallback."""
    home = os.path.expanduser("~")
    sf_bold = os.path.join(home, "Library/Fonts/SFPRODISPLAYBOLD.OTF")
    sf_regular = os.path.join(home, "Library/Fonts/SFPRODISPLAYREGULAR.OTF")

    bold_path = sf_bold if os.path.exists(sf_bold) else "/System/Library/Fonts/Helvetica.ttc"
    regular_path = sf_regular if os.path.exists(sf_regular) else "/System/Library/Fonts/Helvetica.ttc"

    return {
        "name_bold": ImageFont.truetype(bold_path, NAME_FONT_SIZE),
        "handle": ImageFont.truetype(regular_path, HANDLE_FONT_SIZE),
        "tweet": ImageFont.truetype(regular_path, TWEET_FONT_SIZE),
        "slide_num": ImageFont.truetype(regular_path, SLIDE_NUMBER_SIZE),
    }


# =============================================================================
# MEASUREMENT (for vertical centering)
# =============================================================================


def measure_tweet_block(tweet, fonts, text_width, draw, carousel_dir):
    """Calculate total pixel height of one tweet block."""
    h = 0

    # Profile row (avatar height + bottom padding)
    h += AVATAR_SIZE + PROFILE_ROW_BOTTOM_PAD

    # Tweet text
    lines = wrap_text(tweet["text"], fonts["tweet"], text_width, draw)
    line_h = int(TWEET_FONT_SIZE * TWEET_LINE_HEIGHT)
    h += len(lines) * line_h + TWEET_TEXT_TOP_PAD

    # Embedded image
    if tweet.get("image"):
        img_path = resolve_image_path(tweet["image"], carousel_dir)
        if img_path and os.path.exists(img_path):
            try:
                ref = Image.open(img_path)
                aspect = ref.width / ref.height
                img_w = text_width
                img_h = min(int(img_w / aspect), MAX_IMAGE_HEIGHT)
                h += IMAGE_TOP_PAD + img_h + IMAGE_BOTTOM_PAD
            except Exception:
                h += IMAGE_TOP_PAD + 300 + IMAGE_BOTTOM_PAD

    h += TWEET_BOTTOM_PAD
    return h


def resolve_image_path(image_ref, carousel_dir):
    """Resolve image path — absolute or relative to carousel references/."""
    if not image_ref:
        return None
    if os.path.isabs(image_ref):
        return image_ref
    # Try relative to carousel dir
    candidate = os.path.join(carousel_dir, image_ref)
    if os.path.exists(candidate):
        return candidate
    # Try inside references/
    candidate = os.path.join(carousel_dir, "references", image_ref)
    if os.path.exists(candidate):
        return candidate
    return image_ref


# =============================================================================
# RENDERING
# =============================================================================


def render_slide(config, slide_data, slide_num, total_slides, carousel_dir, output_dir, fonts, theme_name):
    """Render a single carousel slide as a 1080x1350 PNG."""
    colors = THEMES[theme_name]
    bg = hex_to_rgb(colors["bg"])
    text_color = hex_to_rgb(colors["text"])
    secondary = hex_to_rgb(colors["secondary"])
    divider_color = hex_to_rgb(colors["divider"])
    badge_color = colors["badge"]
    slide_num_color = hex_to_rgb(colors["slide_num"])

    profile = config["profile"]
    tweets = slide_data["tweets"]

    # Create canvas
    canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), bg)
    draw = ImageDraw.Draw(canvas)

    # Text area width (indented past avatar)
    text_indent = AVATAR_SIZE + 14
    text_width = CONTENT_WIDTH - text_indent

    # Load profile pic
    headshot_path = profile.get("headshot", "")
    if headshot_path and os.path.exists(os.path.expanduser(headshot_path)):
        pfp = load_profile_pic(headshot_path, AVATAR_SIZE)
    else:
        # Gray placeholder
        pfp = Image.new("RGBA", (AVATAR_SIZE, AVATAR_SIZE), (80, 80, 80, 255))
        mask = create_circular_mask(AVATAR_SIZE)
        tmp = Image.new("RGBA", (AVATAR_SIZE, AVATAR_SIZE), (0, 0, 0, 0))
        tmp.paste(pfp, (0, 0), mask)
        pfp = tmp

    # ---------- Measure total content height ----------
    total_content_h = 0
    for i, tweet in enumerate(tweets):
        total_content_h += measure_tweet_block(tweet, fonts, text_width, draw, carousel_dir)
        if i < len(tweets) - 1:
            total_content_h += DIVIDER_VERTICAL_PAD * 2 + 1  # divider

    # Vertical centering
    y = max(MARGIN_Y, (CANVAS_HEIGHT - total_content_h) // 2)

    # ---------- Render each tweet ----------
    for t_idx, tweet in enumerate(tweets):
        x = MARGIN_X

        # --- Profile pic ---
        canvas.paste(pfp, (x, y), pfp)

        # --- Name + badge + handle ---
        name_x = x + text_indent
        name_y = y + 4

        draw.text((name_x, name_y), profile["display_name"], fill=text_color, font=fonts["name_bold"])
        name_bbox = draw.textbbox((name_x, name_y), profile["display_name"], font=fonts["name_bold"])

        # Verified badge
        if profile.get("verified", False):
            bx = name_bbox[2] + 6
            by = name_y + (NAME_FONT_SIZE - BADGE_SIZE) // 2 + 1
            draw_verified_badge(canvas, bx, by, BADGE_SIZE, badge_color)

        # Handle
        handle_y = name_y + NAME_FONT_SIZE + 3
        draw.text((name_x, handle_y), profile["handle"], fill=secondary, font=fonts["handle"])

        # --- Tweet text (with emoji support) ---
        text_x = x + text_indent
        text_y = y + AVATAR_SIZE + PROFILE_ROW_BOTTOM_PAD + TWEET_TEXT_TOP_PAD

        lines = wrap_text(tweet["text"], fonts["tweet"], text_width, draw)
        line_h = int(TWEET_FONT_SIZE * TWEET_LINE_HEIGHT)

        with Pilmoji(canvas) as pilmoji:
            for line in lines:
                pilmoji.text((text_x, text_y), line, fill=text_color, font=fonts["tweet"])
                text_y += line_h

        text_y += 8

        # --- Embedded image ---
        if tweet.get("image"):
            img_path = resolve_image_path(tweet["image"], carousel_dir)
            if img_path and os.path.exists(img_path):
                try:
                    ref_img = Image.open(img_path).convert("RGB")
                    aspect = ref_img.width / ref_img.height
                    img_w = int(text_width)
                    img_h = min(int(img_w / aspect), MAX_IMAGE_HEIGHT)
                    ref_img = ref_img.resize((img_w, img_h), Image.LANCZOS)
                    ref_img = round_corners(ref_img, IMAGE_CORNER_RADIUS)

                    text_y += IMAGE_TOP_PAD
                    canvas.paste(ref_img, (int(text_x), int(text_y)), ref_img)
                    text_y += img_h + IMAGE_BOTTOM_PAD
                except Exception as e:
                    print(f"    Warning: Could not load image {img_path}: {e}")

        y = int(text_y) + TWEET_BOTTOM_PAD

        # --- Divider between combined tweets ---
        if t_idx < len(tweets) - 1:
            div_y = y + DIVIDER_VERTICAL_PAD
            draw.line(
                [(MARGIN_X + text_indent, div_y), (CANVAS_WIDTH - MARGIN_X, div_y)],
                fill=divider_color,
                width=1,
            )
            y = div_y + DIVIDER_VERTICAL_PAD

    # ---------- Slide number (bottom right) ----------
    slide_label = f"{slide_num}/{total_slides}"
    draw.text(
        (CANVAS_WIDTH - MARGIN_X, CANVAS_HEIGHT - 40),
        slide_label,
        fill=slide_num_color,
        font=fonts["slide_num"],
        anchor="ra",
    )

    # ---------- Save ----------
    output_path = os.path.join(output_dir, f"slide_{slide_num}.png")
    canvas.save(output_path, "PNG", quality=95)
    return output_path


# =============================================================================
# MAIN
# =============================================================================


def main():
    if len(sys.argv) < 2:
        print("Usage: render_carousel.py <config.json>")
        print("\nRenders Twitter/X-style thread carousel slides from a config file.")
        sys.exit(1)

    config_path = os.path.abspath(sys.argv[1])
    carousel_dir = os.path.dirname(config_path)

    with open(config_path) as f:
        config = json.load(f)

    theme = config.get("theme", "dark")
    title = config.get("title", "Untitled")
    slides = config.get("slides", [])

    if not slides:
        print("Error: No slides found in config.json")
        sys.exit(1)

    # Output directory = same as config.json location
    output_dir = carousel_dir
    os.makedirs(output_dir, exist_ok=True)

    fonts = load_fonts()
    total = len(slides)

    print(f"\n{'='*50}")
    print(f"  Thread Carousel Renderer")
    print(f"{'='*50}")
    print(f"  Title:  {title}")
    print(f"  Theme:  {theme}")
    print(f"  Slides: {total}")
    print(f"  Output: {output_dir}")
    print(f"{'='*50}\n")

    generated = []
    for i, slide in enumerate(slides, 1):
        path = render_slide(config, slide, i, total, carousel_dir, output_dir, fonts, theme)
        generated.append(path)
        print(f"  [{i}/{total}] Generated: {os.path.basename(path)}")

    print(f"\n  All {len(generated)} slides rendered successfully.")
    print(f"  Output: {output_dir}/\n")

    return generated


if __name__ == "__main__":
    main()
