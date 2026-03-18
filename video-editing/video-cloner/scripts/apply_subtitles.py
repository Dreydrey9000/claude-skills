#!/usr/bin/env python3
"""
Universal Subtitle Renderer for Video Cloner

Applies word-by-word highlight subtitles to any video using a style profile.
Uses Pillow frame-by-frame compositing (no ffmpeg subtitle filters needed).

Supports:
    - Single or dual alternating highlight colors (yellow/green, etc.)
    - Stroke outlines and/or drop shadows
    - Background pills or stroke-only text
    - Any font, position, size — scales automatically with resolution

Usage:
    # With style profile JSON (supports nested subtitle_style key)
    python3 apply_subtitles.py --video input.mp4 --words words.json --style style.json --output output.mp4

    # With inline style params
    python3 apply_subtitles.py --video input.mp4 --words words.json \
        --font "Poppins-ExtraBold" --highlight-color "#FFE600" --output output.mp4

    # Quick defaults (white text, yellow highlight, Poppins ExtraBold)
    python3 apply_subtitles.py --video input.mp4 --words words.json --output output.mp4
"""

import argparse
import json
import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ─── Default Style ────────────────────────────────────────────────────────────

DEFAULT_STYLE = {
    "font_name": "Poppins-ExtraBold",
    "font_size_1080": 55,
    "highlight_color": [255, 230, 0],
    "highlight_colors": None,
    "normal_color": [255, 255, 255],
    "stroke_enabled": False,
    "stroke_color": [0, 0, 0],
    "stroke_width_1080": 4,
    "shadow_enabled": True,
    "shadow_color": [0, 0, 0, 160],
    "shadow_blur": 5,
    "shadow_offset": [3, 3],
    "bg_enabled": True,
    "bg_color": [0, 0, 0, 180],
    "bg_padding": [20, 12, 20, 12],
    "bg_radius": 15,
    "position_y_pct": 0.72,
    "max_words_per_line": 5,
    "no_punctuation": True,
}

# ─── Font Discovery ──────────────────────────────────────────────────────────

FONT_SEARCH_PATHS = [
    os.path.expanduser("~/Library/Fonts"),
    "/Library/Fonts",
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
]


def find_font(font_name):
    """Find a font file by name across system font directories."""
    # Direct path
    if os.path.exists(font_name):
        return font_name

    # Search by name
    for search_dir in FONT_SEARCH_PATHS:
        if not os.path.exists(search_dir):
            continue
        for f in os.listdir(search_dir):
            if font_name.lower().replace("-", "").replace(" ", "") in f.lower().replace("-", "").replace(" ", ""):
                if f.endswith((".ttf", ".otf")):
                    return os.path.join(search_dir, f)

    # Fallback
    fallbacks = ["Poppins-ExtraBold.ttf", "Poppins-Bold.ttf", "Arial Bold.ttf", "Helvetica Bold.ttf"]
    for fb in fallbacks:
        for search_dir in FONT_SEARCH_PATHS:
            path = os.path.join(search_dir, fb)
            if os.path.exists(path):
                print(f"Warning: Font '{font_name}' not found, using fallback: {fb}")
                return path

    print(f"Error: No suitable font found for '{font_name}'")
    sys.exit(1)


# ─── Video Info ───────────────────────────────────────────────────────────────

def get_video_info(video_path):
    """Get resolution and FPS via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    info = {"duration": float(data.get("format", {}).get("duration", 0))}
    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            info["width"] = s["width"]
            info["height"] = s["height"]
            fps_str = s.get("r_frame_rate", "30/1")
            if "/" in fps_str:
                num, den = fps_str.split("/")
                info["fps"] = round(int(num) / int(den), 2)
            else:
                info["fps"] = float(fps_str)
    return info


# ─── Text Rendering ──────────────────────────────────────────────────────────

def clean_word(word, no_punctuation=True):
    """Clean word text — remove punctuation if style says so."""
    if no_punctuation:
        return word.strip().strip(".,!?;:\"'()-—…").upper()
    return word.strip().upper()


def get_highlight_color(style, window_index=0):
    """Get the highlight color for a given word window.

    If highlight_colors (list of colors) is set, alternates between them
    per window. Otherwise falls back to single highlight_color.
    """
    colors = style.get("highlight_colors")
    if colors and len(colors) > 0:
        color = colors[window_index % len(colors)]
        return tuple(color)
    return tuple(style.get("highlight_color", [255, 230, 0]))


def render_subtitle_frame(words_in_window, active_idx, style, width, height, font,
                          window_index=0, stroke_width=0):
    """Render a single subtitle overlay frame as RGBA image."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if not words_in_window:
        return img

    # Clean words
    cleaned = [clean_word(w["text"], style.get("no_punctuation", True)) for w in words_in_window]
    cleaned = [w for w in cleaned if w]  # Remove empty after cleaning

    if not cleaned:
        return img

    # Split into lines
    max_per_line = style.get("max_words_per_line", 5)
    lines = []
    for i in range(0, len(cleaned), max_per_line):
        lines.append(cleaned[i:i + max_per_line])

    # Calculate text dimensions
    highlight_color = get_highlight_color(style, window_index)
    normal_color = tuple(style["normal_color"])

    line_texts = [" ".join(line) for line in lines]
    line_bboxes = [font.getbbox(text) for text in line_texts]
    line_heights = [bbox[3] - bbox[1] for bbox in line_bboxes]
    line_widths = [bbox[2] - bbox[0] for bbox in line_bboxes]
    line_spacing = int(max(line_heights) * 0.3) if line_heights else 10

    total_height = sum(line_heights) + line_spacing * (len(lines) - 1)
    max_width = max(line_widths) if line_widths else 0

    # Position
    y_pos = int(height * style.get("position_y_pct", 0.72))
    x_center = width // 2

    # Background pill
    if style.get("bg_enabled", True):
        bg_color = tuple(style["bg_color"])
        pad = style.get("bg_padding", [20, 12, 20, 12])
        radius = style.get("bg_radius", 15)

        # Scale padding and radius for resolution
        scale = width / 1080.0
        pad = [int(p * scale) for p in pad]
        radius = int(radius * scale)

        bg_left = x_center - max_width // 2 - pad[0]
        bg_top = y_pos - pad[1]
        bg_right = x_center + max_width // 2 + pad[2]
        bg_bottom = y_pos + total_height + pad[3]

        # Draw rounded rectangle background
        bg_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg_img)
        bg_draw.rounded_rectangle(
            [bg_left, bg_top, bg_right, bg_bottom],
            radius=radius,
            fill=bg_color
        )
        img = Image.alpha_composite(img, bg_img)
        draw = ImageDraw.Draw(img)

    # Shadow layer (only when shadow_enabled is true or unset with shadow_color present)
    if style.get("shadow_enabled", True) and style.get("shadow_color"):
        shadow_color = tuple(style["shadow_color"])
        shadow_offset = style.get("shadow_offset", [3, 3])
        shadow_blur = style.get("shadow_blur", 5)

        scale = width / 1080.0
        shadow_offset = [int(o * scale) for o in shadow_offset]
        shadow_blur = int(shadow_blur * scale)

        shadow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)

        cy = y_pos
        word_global_idx = 0
        for line_idx, line in enumerate(lines):
            line_text = " ".join(line)
            line_bbox = font.getbbox(line_text)
            lw = line_bbox[2] - line_bbox[0]
            lx = x_center - lw // 2 + shadow_offset[0]
            ly = cy + shadow_offset[1]
            shadow_draw.text((lx, ly), line_text, font=font, fill=shadow_color)
            cy += line_heights[line_idx] + line_spacing
            word_global_idx += len(line)

        if shadow_blur > 0:
            shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=shadow_blur))

        img = Image.alpha_composite(img, shadow_img)
        draw = ImageDraw.Draw(img)

    # Stroke parameters
    stroke_enabled = style.get("stroke_enabled", False)
    stroke_color = tuple(style.get("stroke_color", [0, 0, 0])) if stroke_enabled else None
    sw = stroke_width if stroke_enabled else 0

    # Draw text with highlight (stroke + fill)
    cy = y_pos
    word_global_idx = 0
    for line_idx, line in enumerate(lines):
        # Calculate line start X
        line_text = " ".join(line)
        line_bbox = font.getbbox(line_text)
        lw = line_bbox[2] - line_bbox[0]
        cx = x_center - lw // 2

        for word in line:
            color = highlight_color if word_global_idx == active_idx else normal_color
            draw.text((cx, cy), word, font=font, fill=color,
                       stroke_width=sw, stroke_fill=stroke_color)
            word_bbox = font.getbbox(word + " ")
            cx += word_bbox[2] - word_bbox[0]
            word_global_idx += 1

        cy += line_heights[line_idx] + line_spacing

    return img


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def process_video(video_path, words_path, style, output_path, format_type="h264"):
    """Process video frame-by-frame, overlaying subtitles."""
    # Load word timestamps
    with open(words_path) as f:
        words = json.load(f)

    # Get video info
    info = get_video_info(video_path)
    width, height = info["width"], info["height"]
    fps = info["fps"]
    duration = info["duration"]

    print(f"Video: {width}x{height} @ {fps}fps, {duration:.1f}s")

    # Scale font size for resolution
    scale = width / 1080.0
    font_size = int(style.get("font_size_1080", 55) * scale)
    font_path = find_font(style.get("font_name", "Poppins-ExtraBold"))
    font = ImageFont.truetype(font_path, font_size)
    print(f"Font: {font_path} @ {font_size}pt (scale: {scale:.1f}x)")

    # Scale stroke width for resolution
    stroke_width = int(style.get("stroke_width_1080", 4) * scale) if style.get("stroke_enabled", False) else 0

    # Clean words
    cleaned_words = []
    for w in words:
        cleaned = clean_word(w["text"], style.get("no_punctuation", True))
        if cleaned:
            cleaned_words.append({**w, "cleaned": cleaned})

    total_frames = int(duration * fps)
    print(f"Processing {total_frames} frames...")

    # FFmpeg decode pipe
    decode_cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-v", "quiet", "-"
    ]

    # FFmpeg encode pipe
    if format_type == "prores":
        ext = ".mov"
        encode_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{width}x{height}", "-r", str(fps),
            "-i", "-",
            "-i", video_path, "-map", "0:v", "-map", "1:a",
            "-c:v", "prores_ks", "-profile:v", "3",
            "-c:a", "pcm_s24le",
            "-shortest", output_path
        ]
    else:
        ext = ".mp4"
        encode_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{width}x{height}", "-r", str(fps),
            "-i", "-",
            "-i", video_path, "-map", "0:v", "-map", "1:a",
            "-c:v", "h264_videotoolbox", "-b:v", "25M",
            "-c:a", "aac", "-b:a", "320k",
            "-shortest", output_path
        ]

    decoder = subprocess.Popen(decode_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    encoder = subprocess.Popen(encode_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    frame_size = width * height * 3
    frame_count = 0
    window_size = style.get("max_words_per_line", 5) * 2  # Show 2 lines max

    try:
        while True:
            raw_frame = decoder.stdout.read(frame_size)
            if len(raw_frame) < frame_size:
                break

            timestamp = frame_count / fps

            # Find active word and window
            active_idx = None
            window_start = 0
            for i, w in enumerate(cleaned_words):
                if w["start"] <= timestamp <= w["end"]:
                    active_idx = i
                    break
                elif w["start"] > timestamp:
                    # Between words — highlight the previous one still
                    if i > 0 and timestamp - cleaned_words[i - 1]["end"] < 0.3:
                        active_idx = i - 1
                    break

            # Determine word window
            if active_idx is not None:
                window_start = max(0, (active_idx // window_size) * window_size)
                window_end = min(len(cleaned_words), window_start + window_size)
                window_words = cleaned_words[window_start:window_end]
                local_active = active_idx - window_start
                window_index = active_idx // window_size
            else:
                window_words = []
                local_active = None
                window_index = 0

            # Render subtitle overlay
            if window_words:
                frame_img = Image.frombytes("RGB", (width, height), raw_frame)
                overlay = render_subtitle_frame(window_words, local_active, style, width, height, font,
                                                window_index=window_index, stroke_width=stroke_width)
                frame_img = frame_img.convert("RGBA")
                frame_img = Image.alpha_composite(frame_img, overlay)
                frame_img = frame_img.convert("RGB")
                encoder.stdin.write(frame_img.tobytes())
            else:
                encoder.stdin.write(raw_frame)

            frame_count += 1
            if frame_count % (int(fps) * 5) == 0:
                print(f"  Frame {frame_count}/{total_frames} ({timestamp:.1f}s)")

    except BrokenPipeError:
        pass
    finally:
        decoder.stdout.close()
        if encoder.stdin:
            encoder.stdin.close()
        decoder.wait()
        encoder.wait()

    output_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nDone! {frame_count} frames processed")
    print(f"Output: {output_path} ({output_size:.0f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Universal Subtitle Renderer")
    parser.add_argument("--video", "-v", required=True, help="Input video file")
    parser.add_argument("--words", "-w", required=True, help="Word timestamps JSON file")
    parser.add_argument("--style", "-s", help="Style profile JSON file")
    parser.add_argument("--output", "-o", required=True, help="Output video file")
    parser.add_argument("--format", default="h264", choices=["h264", "prores", "h264-software"],
                        help="Output format (default: h264)")

    # Inline style overrides
    parser.add_argument("--font", help="Font name (e.g. Poppins-ExtraBold)")
    parser.add_argument("--font-size", type=int, help="Font size at 1080p (scales automatically)")
    parser.add_argument("--highlight-color", help="Highlight color hex (e.g. #FFE600)")
    parser.add_argument("--normal-color", help="Normal text color hex (e.g. #FFFFFF)")
    parser.add_argument("--no-bg", action="store_true", help="Disable background pill")
    parser.add_argument("--position-y", type=float, help="Vertical position (0.0-1.0, default 0.72)")

    args = parser.parse_args()

    # Load style
    if args.style and os.path.exists(args.style):
        with open(args.style) as f:
            raw_style = json.load(f)
        # Flatten nested subtitle_style key (e.g. @ryanmagin_style.json)
        if "subtitle_style" in raw_style:
            style = {**DEFAULT_STYLE, **raw_style["subtitle_style"]}
        else:
            style = {**DEFAULT_STYLE, **raw_style}
    else:
        style = DEFAULT_STYLE.copy()

    # Apply inline overrides
    if args.font:
        style["font_name"] = args.font
    if args.font_size:
        style["font_size_1080"] = args.font_size
    if args.highlight_color:
        h = args.highlight_color.lstrip("#")
        style["highlight_color"] = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    if args.normal_color:
        h = args.normal_color.lstrip("#")
        style["normal_color"] = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    if args.no_bg:
        style["bg_enabled"] = False
    if args.position_y:
        style["position_y_pct"] = args.position_y

    process_video(args.video, args.words, style, args.output, args.format)


if __name__ == "__main__":
    main()
