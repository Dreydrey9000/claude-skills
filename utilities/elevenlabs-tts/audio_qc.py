#!/usr/bin/env python3
"""
Audio QC Protocol v2 — Viral Editz

Generates ElevenLabs TTS, transcribes back via STT, diffs against original,
and loops until clean. Chunks long scripts to avoid degradation, crossfade
stitches for seamless joins, and trims trailing artifacts.

Learned from Ryan Magin voice clone sessions:
- Model: eleven_multilingual_v2 (only model that preserves cloned voice)
- Style MUST be 0 (causes stutters, extra sounds, speed issues on clones)
- Similarity sweet spot is 0.75 (higher = distortion on clones)
- Chunk scripts under 800 chars to prevent late-script degradation
- Crossfade stitch (not silence gaps) for seamless chunk joins
- Write out numbers as words (multilingual model misreads digits)
- Expand contractions for cleaner pronunciation
- Trim trailing audio artifacts (TTS adds noise at end of generations)

Usage:
    python3 audio_qc.py --script script.txt
    python3 audio_qc.py --script script.txt --heygen
    python3 audio_qc.py --script script.txt --voice-id YOUR_VOICE_ID

Env vars (or pass via CLI):
    ELEVENLABS_API_KEY
    HEYGEN_API_KEY
"""

import argparse, json, os, shutil, subprocess, sys, time, difflib, re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_VOICE_ID = "FaqEcpH1etobBPMBMfJg"  # Ryan Magin TRT Voice
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_STT_MODEL = "scribe_v1"
MAX_RETRIES = 3
SIMILARITY_THRESHOLD = 0.92
CHUNK_CHAR_LIMIT = 700  # Stay under 800 with margin
CROSSFADE_DURATION = 0.15  # Seconds of crossfade between chunks
TAIL_TRIM_SECS = 0.4  # Trim from end of last chunk to kill artifacts

# Voice settings — tuned through multiple sessions with Ryan's clone
# KEY LEARNINGS:
#   style=0.0  → MANDATORY for cloned voices (causes artifacts otherwise)
#   similarity=0.75 → sweet spot (higher = distortion)
#   stability=0.55 → balanced expression without randomness
VOICE_SETTINGS = {
    "stability": 0.55,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}


# ── Text Preprocessing ───────────────────────────────────────────────────────

def preprocess_script(text: str) -> str:
    """Clean script for optimal TTS delivery on multilingual_v2."""
    # Remove em-dashes (cause weird pauses)
    text = text.replace("—", ",").replace("–", ",")
    # Remove ALL CAPS (causes unnatural emphasis artifacts)
    # Preserve meaning by keeping first letter cap
    words = text.split()
    cleaned = []
    for w in words:
        if w.isupper() and len(w) > 1 and w.isalpha():
            cleaned.append(w.capitalize())
        else:
            cleaned.append(w)
    text = " ".join(cleaned)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk_script(text: str, limit: int = CHUNK_CHAR_LIMIT) -> list[str]:
    """
    Split script into chunks under the character limit.
    Splits on sentence boundaries to preserve natural flow.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 > limit and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()

    if current:
        chunks.append(current.strip())

    return chunks


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace for comparison."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similarity(a: str, b: str) -> float:
    """SequenceMatcher ratio between two normalized strings."""
    return difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def word_diff(original: str, transcribed: str) -> list[dict]:
    """Return list of diffs: added, removed, changed words."""
    orig_words = normalize(original).split()
    trans_words = normalize(transcribed).split()
    sm = difflib.SequenceMatcher(None, orig_words, trans_words)
    issues = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        issues.append({
            "type": tag,
            "original": " ".join(orig_words[i1:i2]),
            "transcribed": " ".join(trans_words[j1:j2]),
            "position": f"words {i1}-{i2}",
        })
    return issues


def check_ffmpeg():
    """Verify ffmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


# ── ElevenLabs TTS ────────────────────────────────────────────────────────────

def generate_audio(
    script: str,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    output_path: str = "output_audio.mp3",
) -> str:
    """Generate audio via ElevenLabs TTS. Returns path to mp3."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": script,
        "model_id": model,
        "voice_settings": VOICE_SETTINGS,
    }).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", "application/json")

    print(f"  [TTS] Generating audio → {output_path}")
    resp = urlopen(req, timeout=120)
    with open(output_path, "wb") as f:
        f.write(resp.read())
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  [TTS] Done — {size_kb:.0f} KB")
    return output_path


def generate_chunked_audio(
    script: str,
    api_key: str,
    voice_id: str,
    output_dir: str,
) -> str:
    """
    Generate audio in chunks with context seeding and crossfade stitching.

    For scripts over CHUNK_CHAR_LIMIT:
    1. Split into sentence-boundary chunks
    2. Generate each chunk (chunks 2+ include last sentence of prior chunk as context)
    3. Trim context lead-ins using STT word timestamps
    4. Crossfade stitch all chunks
    5. Trim trailing artifacts from final chunk
    """
    chunks = chunk_script(script)

    if len(chunks) == 1:
        # Short script — single pass, just trim the tail
        path = os.path.join(output_dir, "audio_final.mp3")
        generate_audio(script, api_key, voice_id, output_path=path)
        trim_tail(path, path)
        return path

    print(f"  [CHUNK] Script split into {len(chunks)} chunks")
    for i, c in enumerate(chunks, 1):
        print(f"    Chunk {i}: {len(c)} chars — \"{c[:50]}...\"")

    chunk_paths = []
    prev_last_sentence = None

    for i, chunk in enumerate(chunks):
        raw_path = os.path.join(output_dir, f"chunk_{i}_raw.mp3")

        if i == 0 or prev_last_sentence is None:
            # First chunk — generate directly
            generate_audio(chunk, api_key, voice_id, output_path=raw_path)
            chunk_paths.append(raw_path)
        else:
            # Subsequent chunks — prepend last sentence of previous chunk as context
            context_text = f"{prev_last_sentence} {chunk}"
            generate_audio(context_text, api_key, voice_id, output_path=raw_path)

            # Transcribe to find where the actual chunk starts
            trim_path = os.path.join(output_dir, f"chunk_{i}_trimmed.mp3")
            cut_time = find_context_cut_point(raw_path, prev_last_sentence, api_key)

            if cut_time > 0:
                subprocess.run(
                    ["ffmpeg", "-y", "-i", raw_path, "-ss", str(cut_time),
                     "-acodec", "copy", trim_path],
                    capture_output=True,
                )
                chunk_paths.append(trim_path)
                print(f"  [CHUNK] Chunk {i+1} trimmed at {cut_time:.2f}s")
            else:
                chunk_paths.append(raw_path)
                print(f"  [CHUNK] Chunk {i+1} — could not find cut point, using full audio")

        # Store last sentence for next chunk's context
        sentences = re.split(r'(?<=[.!?])\s+', chunk)
        prev_last_sentence = sentences[-1] if sentences else None

    # Trim tail of last chunk
    last = chunk_paths[-1]
    trimmed_last = os.path.join(output_dir, "last_chunk_trimmed.mp3")
    trim_tail(last, trimmed_last)
    chunk_paths[-1] = trimmed_last

    # Crossfade stitch
    final_path = os.path.join(output_dir, "audio_final.mp3")
    crossfade_stitch(chunk_paths, final_path)

    return final_path


def find_context_cut_point(audio_path: str, context_sentence: str, api_key: str) -> float:
    """Use STT word timestamps to find where the context sentence ends."""
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    boundary = "----AudioQCBoundary9876"

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="audio.mp3"\r\n'
        f"Content-Type: audio/mpeg\r\n\r\n"
    ).encode() + audio_data + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="model_id"\r\n\r\n'
        f"{DEFAULT_STT_MODEL}"
        f"\r\n--{boundary}--\r\n"
    ).encode()

    req = Request(url, data=body, method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    resp = urlopen(req, timeout=120)
    data = json.loads(resp.read())

    # Count words in context sentence, find timestamp after that many words
    context_word_count = len(normalize(context_sentence).split())
    words = [w for w in data.get("words", []) if w.get("type") == "word"]

    if len(words) > context_word_count:
        # Cut just before the word after the context ends (with 0.2s buffer)
        cut_word = words[context_word_count]
        return max(0, cut_word["start"] - 0.2)

    return 0


def trim_tail(input_path: str, output_path: str, trim_secs: float = TAIL_TRIM_SECS):
    """Trim trailing seconds from audio to remove end-of-generation artifacts."""
    # Get duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", input_path],
        capture_output=True, text=True,
    )
    duration = float(result.stdout.strip())
    target = duration - trim_secs

    if target < 1:
        # Too short to trim, just copy
        if input_path != output_path:
            shutil.copy2(input_path, output_path)
        return

    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-t", str(target),
         "-acodec", "copy", output_path],
        capture_output=True,
    )


def crossfade_stitch(chunk_paths: list[str], output_path: str, fade_dur: float = CROSSFADE_DURATION):
    """Crossfade stitch multiple audio files into one seamless file."""
    if len(chunk_paths) == 1:
        shutil.copy2(chunk_paths[0], output_path)
        return

    # Convert all to wav first for proper audio processing
    wav_paths = []
    for i, mp3 in enumerate(chunk_paths):
        wav = mp3.rsplit(".", 1)[0] + ".wav"
        subprocess.run(["ffmpeg", "-y", "-i", mp3, wav], capture_output=True)
        wav_paths.append(wav)

    # Sequential crossfade merge
    current = wav_paths[0]
    for i in range(1, len(wav_paths)):
        merged = current.rsplit(".", 1)[0] + f"_merged_{i}.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", current, "-i", wav_paths[i],
             "-filter_complex", f"acrossfade=d={fade_dur}:c1=tri:c2=tri",
             merged],
            capture_output=True,
        )
        current = merged

    # Encode final to mp3
    subprocess.run(
        ["ffmpeg", "-y", "-i", current, "-b:a", "192k", output_path],
        capture_output=True,
    )

    # Clean up wav files
    for wav in wav_paths:
        if os.path.exists(wav):
            os.remove(wav)
    # Clean up intermediate merges
    for f in Path(os.path.dirname(output_path)).glob("*_merged_*.wav"):
        f.unlink()

    print(f"  [STITCH] Crossfade stitched {len(chunk_paths)} chunks → {output_path}")


# ── ElevenLabs STT ────────────────────────────────────────────────────────────

def transcribe_audio(
    audio_path: str,
    api_key: str,
    model: str = DEFAULT_STT_MODEL,
) -> str:
    """Transcribe audio via ElevenLabs STT. Returns transcript text."""
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    boundary = "----AudioQCBoundary9876"

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="audio.mp3"\r\n'
        f"Content-Type: audio/mpeg\r\n\r\n"
    ).encode() + audio_data + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="model_id"\r\n\r\n'
        f"{model}"
        f"\r\n--{boundary}--\r\n"
    ).encode()

    req = Request(url, data=body, method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    print(f"  [STT] Transcribing {os.path.basename(audio_path)}...")
    resp = urlopen(req, timeout=120)
    data = json.loads(resp.read())
    transcript = data.get("text", "")
    print(f"  [STT] Got {len(transcript.split())} words")
    return transcript


# ── QC Loop ───────────────────────────────────────────────────────────────────

def run_qc(
    script: str,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID,
    output_dir: str = ".",
    max_retries: int = MAX_RETRIES,
    threshold: float = SIMILARITY_THRESHOLD,
) -> tuple[str, str, float]:
    """
    Generate → Transcribe → Compare loop.
    Returns (audio_path, transcript, similarity_score).
    """
    has_ffmpeg = check_ffmpeg()
    use_chunking = has_ffmpeg and len(script) > CHUNK_CHAR_LIMIT

    print("\n" + "=" * 60)
    print("  AUDIO QC PROTOCOL v2 — Viral Editz")
    print("=" * 60)
    print(f"  Script length: {len(script)} chars")
    print(f"  Chunking: {'yes' if use_chunking else 'no (single pass)'}")
    print(f"  Voice settings: stability={VOICE_SETTINGS['stability']}, "
          f"similarity={VOICE_SETTINGS['similarity_boost']}, "
          f"style={VOICE_SETTINGS['style']}")

    # Preprocess
    script_clean = preprocess_script(script)
    if script_clean != script:
        print("  [PRE] Script preprocessed (removed caps, em-dashes)")

    best_score = 0
    best_path = None
    best_transcript = None

    for attempt in range(1, max_retries + 1):
        print(f"\n── Attempt {attempt}/{max_retries} ──")

        attempt_dir = os.path.join(output_dir, f"attempt_{attempt}")
        os.makedirs(attempt_dir, exist_ok=True)

        if use_chunking:
            audio_path = generate_chunked_audio(script_clean, api_key, voice_id, attempt_dir)
        else:
            audio_path = os.path.join(attempt_dir, "audio.mp3")
            generate_audio(script_clean, api_key, voice_id, output_path=audio_path)
            trim_tail(audio_path, audio_path)

        transcript = transcribe_audio(audio_path, api_key)

        score = similarity(script_clean, transcript)
        issues = word_diff(script_clean, transcript)

        print(f"\n  [QC] Similarity: {score:.1%}")

        if issues:
            print(f"  [QC] Found {len(issues)} issue(s):")
            for i, issue in enumerate(issues[:10], 1):
                orig = issue["original"] or "(nothing)"
                trans = issue["transcribed"] or "(nothing)"
                print(f"        {i}. [{issue['type']}] \"{orig}\" → \"{trans}\"")
            if len(issues) > 10:
                print(f"        ... and {len(issues) - 10} more")
        else:
            print("  [QC] No issues detected!")

        if score > best_score:
            best_score = score
            best_path = audio_path
            best_transcript = transcript

        if score >= threshold:
            print(f"\n  PASSED — {score:.1%} similarity (threshold: {threshold:.0%})")
            final_path = os.path.join(output_dir, "audio_final.mp3")
            shutil.copy2(audio_path, final_path)
            return final_path, transcript, score

        print(f"\n  BELOW THRESHOLD — {score:.1%} < {threshold:.0%}")

        if attempt < max_retries:
            # Bump stability slightly each retry
            VOICE_SETTINGS["stability"] = min(0.75, VOICE_SETTINGS["stability"] + 0.05)
            print(f"  Bumping stability to {VOICE_SETTINGS['stability']:.2f} for next attempt...")

    print(f"\n  Max retries reached. Best score: {best_score:.1%}")
    final_path = os.path.join(output_dir, "audio_final.mp3")
    shutil.copy2(best_path, final_path)
    return final_path, best_transcript, best_score


# ── HeyGen Video ──────────────────────────────────────────────────────────────

def upload_audio_to_heygen(audio_path: str, api_key: str) -> str:
    """Upload audio to HeyGen, return asset URL."""
    url = "https://upload.heygen.com/v1/asset"
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    req = Request(url, data=audio_data, method="POST")
    req.add_header("X-API-KEY", api_key)
    req.add_header("Content-Type", "audio/mpeg")

    print("  [HeyGen] Uploading audio...")
    resp = urlopen(req, timeout=120)
    data = json.loads(resp.read())

    if data.get("code") != 100:
        raise RuntimeError(f"HeyGen upload failed: {data}")

    audio_url = data["data"]["url"]
    print(f"  [HeyGen] Uploaded → {data['data']['id']}")
    return audio_url


def generate_heygen_video(
    audio_url: str,
    api_key: str,
    avatar_id: str,
    width: int = 720,
    height: int = 1280,
) -> str:
    """Submit HeyGen video generation. Returns video_id."""
    url = "https://api.heygen.com/v2/video/generate"
    payload = json.dumps({
        "test": False,
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal",
            },
            "voice": {
                "type": "audio",
                "audio_url": audio_url,
            },
        }],
        "dimension": {"width": width, "height": height},
    }).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("X-Api-Key", api_key)
    req.add_header("Content-Type", "application/json")

    print("  [HeyGen] Submitting video generation...")
    resp = urlopen(req, timeout=60)
    data = json.loads(resp.read())

    if data.get("error"):
        raise RuntimeError(f"HeyGen error: {data['error']}")

    video_id = data["data"]["video_id"]
    print(f"  [HeyGen] Video ID: {video_id}")
    return video_id


def poll_heygen_video(video_id: str, api_key: str, timeout_secs: int = 600) -> str:
    """Poll HeyGen until video is ready. Returns video URL."""
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    start = time.time()

    print("  [HeyGen] Waiting for video to render", end="", flush=True)
    while time.time() - start < timeout_secs:
        req = Request(url)
        req.add_header("X-Api-Key", api_key)
        resp = urlopen(req, timeout=30)
        data = json.loads(resp.read())["data"]

        status = data["status"]
        if status == "completed":
            print(" done!")
            video_url = data["video_url"]
            print(f"  [HeyGen] Video URL: {video_url[:80]}...")
            return video_url
        elif status == "failed":
            error = data.get("error", {})
            raise RuntimeError(f"HeyGen render failed: {error}")

        print(".", end="", flush=True)
        time.sleep(15)

    raise TimeoutError(f"HeyGen render timed out after {timeout_secs}s")


def download_video(video_url: str, output_path: str) -> str:
    """Download the rendered video."""
    req = Request(video_url)
    print(f"  [HeyGen] Downloading → {output_path}")
    resp = urlopen(req, timeout=120)
    with open(output_path, "wb") as f:
        f.write(resp.read())
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  [HeyGen] Done — {size_mb:.1f} MB")
    return output_path


# ── Report ────────────────────────────────────────────────────────────────────

def print_report(
    script: str, transcript: str, score: float,
    issues: list, audio_path: str, video_path: str = None,
):
    """Print final QC report."""
    print("\n" + "=" * 60)
    print("  AUDIO QC REPORT")
    print("=" * 60)
    print(f"  Similarity Score:  {score:.1%}")
    print(f"  Audio File:        {audio_path}")
    if video_path:
        print(f"  Video File:        {video_path}")
    print(f"  Issues Found:      {len(issues)}")
    print(f"  Voice Settings:    stability={VOICE_SETTINGS['stability']}, "
          f"similarity={VOICE_SETTINGS['similarity_boost']}, "
          f"style={VOICE_SETTINGS['style']}")

    if issues:
        print("\n  Issues:")
        for i, issue in enumerate(issues[:15], 1):
            print(f"    {i}. [{issue['type']}] \"{issue['original']}\" → \"{issue['transcribed']}\"")

    print("=" * 60)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Audio QC Protocol v2 — Viral Editz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic QC (generate + verify audio)
  python3 audio_qc.py -s script.txt -o ./output

  # Full pipeline (audio QC + HeyGen video)
  python3 audio_qc.py -s script.txt -o ./output --heygen

  # Custom voice + settings
  python3 audio_qc.py -s script.txt --voice-id YOUR_ID --threshold 0.90
        """,
    )
    parser.add_argument("--script", "-s", help="Path to script text file")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help="ElevenLabs voice ID")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    parser.add_argument("--threshold", type=float, default=SIMILARITY_THRESHOLD)
    parser.add_argument("--max-retries", type=int, default=MAX_RETRIES)
    parser.add_argument("--elevenlabs-key", default=os.environ.get("ELEVENLABS_API_KEY"))
    parser.add_argument("--heygen", action="store_true", help="Also generate HeyGen video")
    parser.add_argument("--heygen-key", default=os.environ.get("HEYGEN_API_KEY"))
    parser.add_argument("--avatar-id", default="f1edc6880c3e49b0835f975b7f8d26f1")
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--height", type=int, default=1280)

    args = parser.parse_args()

    if args.script:
        script = Path(args.script).read_text().strip()
    else:
        print("Paste your script (Ctrl+D when done):")
        script = sys.stdin.read().strip()

    if not script:
        print("Error: No script provided")
        sys.exit(1)

    if not args.elevenlabs_key:
        print("Error: Set ELEVENLABS_API_KEY or pass --elevenlabs-key")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Run QC loop
    audio_path, transcript, score = run_qc(
        script=script,
        api_key=args.elevenlabs_key,
        voice_id=args.voice_id,
        output_dir=args.output_dir,
        max_retries=args.max_retries,
        threshold=args.threshold,
    )

    issues = word_diff(preprocess_script(script), transcript)
    video_path = None

    # HeyGen video generation
    if args.heygen:
        if not args.heygen_key:
            print("Error: Set HEYGEN_API_KEY or pass --heygen-key")
            sys.exit(1)

        audio_url = upload_audio_to_heygen(audio_path, args.heygen_key)
        video_id = generate_heygen_video(
            audio_url, args.heygen_key, args.avatar_id,
            width=args.width, height=args.height,
        )
        video_url = poll_heygen_video(video_id, args.heygen_key)
        video_path = os.path.join(args.output_dir, "heygen_video.mp4")
        download_video(video_url, video_path)

    print_report(script, transcript, score, issues, audio_path, video_path)


if __name__ == "__main__":
    main()
