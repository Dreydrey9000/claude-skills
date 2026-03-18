#!/opt/homebrew/bin/python3.13
"""Render strict Instagram carousel slides from transcript or slide list.

Rule enforced: convert number words to digits before rendering.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

UNITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
TEENS = {
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
SCALES = {
    "hundred": 100,
    "thousand": 1_000,
    "million": 1_000_000,
    "billion": 1_000_000_000,
}
NUMBER_WORDS = set(UNITS) | set(TEENS) | set(TENS) | set(SCALES) | {"and", "point"}
NUMBER_PHRASE_RE = re.compile(
    r"\b(?:" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")(?:[\s-]+(?:"
    + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
    + r"))*\b",
    re.IGNORECASE,
)
HYPHEN_PREFIX_RE = re.compile(
    r"\b(" + "|".join(sorted(set(UNITS) | set(TEENS) | set(TENS), key=len, reverse=True)) + r")-([A-Za-z]+)\b",
    re.IGNORECASE,
)


def parse_number_words(words: list[str]) -> str | None:
    total = 0
    current = 0
    seen = False
    base_seen = False
    i = 0

    while i < len(words):
        w = words[i]
        if w == "and":
            i += 1
            continue
        if w == "point":
            if not seen:
                return None
            i += 1
            decimals: list[str] = []
            while i < len(words):
                d = words[i]
                if d == "and":
                    i += 1
                    continue
                if d in UNITS:
                    decimals.append(str(UNITS[d]))
                elif d in TEENS:
                    decimals.extend(list(str(TEENS[d])))
                elif d in TENS:
                    decimals.extend(list(str(TENS[d])))
                else:
                    return None
                i += 1
            if not decimals:
                return None
            return f"{total + current}.{''.join(decimals)}"

        if w in UNITS:
            current += UNITS[w]
            seen = True
            base_seen = True
        elif w in TEENS:
            current += TEENS[w]
            seen = True
            base_seen = True
        elif w in TENS:
            current += TENS[w]
            seen = True
            base_seen = True
        elif w == "hundred":
            current = max(current, 1) * 100
            seen = True
            base_seen = True
        elif w in ("thousand", "million", "billion"):
            # Do not convert standalone scale words like "million" when preceded by numeric text.
            if current == 0 and not base_seen:
                return None
            scale = SCALES[w]
            current = max(current, 1)
            total += current * scale
            current = 0
            seen = True
        else:
            return None
        i += 1

    if not seen:
        return None
    return str(total + current)


def convert_number_words(text: str) -> str:
    def hyphen_replace(match: re.Match[str]) -> str:
        left = match.group(1).lower()
        right = match.group(2)
        if left in UNITS:
            value = UNITS[left]
        elif left in TEENS:
            value = TEENS[left]
        else:
            value = TENS.get(left)
        if value is None:
            return match.group(0)
        return f"{value}-{right}"

    text = HYPHEN_PREFIX_RE.sub(hyphen_replace, text)

    def phrase_replace(match: re.Match[str]) -> str:
        phrase = match.group(0)
        words = [w.lower() for w in re.split(r"[\s-]+", phrase) if w]
        parsed = parse_number_words(words)
        return parsed if parsed is not None else phrase

    text = NUMBER_PHRASE_RE.sub(phrase_replace, text)

    # Convert explicit numeric scales: "4.5 million" -> "4500000"
    def scale_replace(match: re.Match[str]) -> str:
        raw_value = match.group(1)
        scale_word = match.group(2).lower()
        scale = SCALES[scale_word]
        value = int(float(raw_value) * scale)
        return f"{value:,}"

    return re.sub(r"\b(\d+(?:\.\d+)?)\s+(thousand|million|billion)\b", scale_replace, text, flags=re.IGNORECASE)


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+", text.strip())
    return [c.strip() for c in chunks if c.strip()]


def pack_into_slides(sentences: list[str], slide_count: int) -> list[str]:
    if not sentences:
        return []
    if len(sentences) <= slide_count:
        return sentences

    slides: list[str] = []
    bucket_size = len(sentences) / slide_count
    start = 0.0
    for _ in range(slide_count):
        end = start + bucket_size
        s = int(round(start))
        e = int(round(end))
        if e <= s:
            e = s + 1
        slides.append(" ".join(sentences[s:e]).strip())
        start = end

    # Collapse accidental empties.
    slides = [s for s in slides if s]
    if len(slides) > slide_count:
        slides = slides[:slide_count]
    return slides


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        l, t, r, b = draw.textbbox((0, 0), trial, font=font)
        if (r - l) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def render_slide(text: str, slide_idx: int, slide_total: int, out_path: Path, width: int, height: int) -> None:
    img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    body_font = load_font(64)
    footer_font = load_font(34)

    lines = wrap_lines(draw, text, body_font, int(width * 0.82))
    line_heights = [draw.textbbox((0, 0), ln, font=body_font)[3] - draw.textbbox((0, 0), ln, font=body_font)[1] for ln in lines]
    spacing = 18
    total_h = sum(line_heights) + spacing * (len(lines) - 1)
    y = (height - total_h) // 2

    for ln, h in zip(lines, line_heights):
        l, t, r, b = draw.textbbox((0, 0), ln, font=body_font)
        x = (width - (r - l)) // 2
        draw.text((x, y), ln, font=body_font, fill=(255, 255, 255))
        y += h + spacing

    footer = f"{slide_idx}/{slide_total}"
    l, t, r, b = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text((width - (r - l) - 44, height - (b - t) - 34), footer, font=footer_font, fill=(41, 151, 255))

    img.save(out_path, format="PNG", optimize=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_slides(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def render_all(slides: Iterable[str], output_dir: Path, width: int, height: int) -> list[str]:
    slide_list = list(slides)
    output_dir.mkdir(parents=True, exist_ok=True)

    final_lines: list[str] = []
    for i, slide in enumerate(slide_list, start=1):
        normalized = re.sub(r"\s+", " ", slide).strip()
        normalized = convert_number_words(normalized)
        final_lines.append(normalized)
        render_slide(normalized, i, len(slide_list), output_dir / f"{i:02d}.png", width, height)

    (output_dir / "slides.final.txt").write_text("\n".join(final_lines) + "\n", encoding="utf-8")
    return final_lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render strict carousel slides with digit conversion.")
    parser.add_argument("--slides-file", type=Path, help="One slide per line.")
    parser.add_argument("--transcript-file", type=Path, help="Transcript text file.")
    parser.add_argument("--text", type=str, help="Inline transcript text.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--slide-count", type=int, default=10)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1350)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sources = [bool(args.slides_file), bool(args.transcript_file), bool(args.text)]
    if sum(sources) != 1:
        raise SystemExit("Provide exactly one input: --slides-file OR --transcript-file OR --text")

    if args.slides_file:
        slides = read_slides(args.slides_file)
    else:
        source_text = args.text if args.text else read_text(args.transcript_file)
        sentences = split_sentences(source_text)
        slides = pack_into_slides(sentences, args.slide_count)

    if not slides:
        raise SystemExit("No slides were generated from the input.")

    final_lines = render_all(slides, args.output_dir, args.width, args.height)

    print(f"Created {len(final_lines)} slides in {args.output_dir}")
    print(f"Final copy saved at {args.output_dir / 'slides.final.txt'}")


if __name__ == "__main__":
    main()
