#!/usr/bin/env python3
"""
Frame Extractor for Video Cloner

Downloads a video (or uses local file) and extracts frames at 0.5s intervals.
Also extracts metadata and transcribes with word-level timestamps.

Usage:
    # From URL (Instagram/TikTok/YouTube)
    python3 extract_frames.py --url "https://instagram.com/reel/XXX" --output ~/.tmp/ref_analysis

    # From local file
    python3 extract_frames.py --file "/path/to/video.mp4" --output ~/.tmp/ref_analysis

    # Custom frame interval
    python3 extract_frames.py --url "URL" --output ~/.tmp/ref_analysis --interval 1.0
"""

import argparse
import subprocess
import json
import os
import sys
import glob


def download_video(url, output_dir):
    """Download video + metadata using yt-dlp."""
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "ref_video.%(ext)s")

    cmd = [
        "yt-dlp",
        "--write-info-json",
        "--write-thumbnail",
        "-o", output_template,
        url
    ]

    print(f"Downloading: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error downloading:\n{result.stderr[-500:]}")
        sys.exit(1)

    # Find the downloaded video file
    for ext in ["mp4", "webm", "mkv", "mov"]:
        path = os.path.join(output_dir, f"ref_video.{ext}")
        if os.path.exists(path):
            return path

    # Fallback: find any video file
    for f in os.listdir(output_dir):
        if f.startswith("ref_video") and not f.endswith((".json", ".jpg", ".webp", ".png")):
            return os.path.join(output_dir, f)

    print("Error: Could not find downloaded video file")
    sys.exit(1)


def get_video_info(video_path):
    """Get video metadata via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    info = {
        "duration": float(data.get("format", {}).get("duration", 0)),
        "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 1),
    }

    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            info["width"] = s.get("width", 0)
            info["height"] = s.get("height", 0)
            info["fps"] = s.get("r_frame_rate", "30/1")
            info["codec"] = s.get("codec_name", "unknown")
            info["orientation"] = "vertical" if s["height"] > s["width"] else "horizontal"

    return info


def extract_metadata(output_dir):
    """Extract metadata from yt-dlp info.json."""
    info_files = glob.glob(os.path.join(output_dir, "*.info.json"))
    if not info_files:
        return {}

    with open(info_files[0]) as f:
        d = json.load(f)

    return {
        "creator": d.get("uploader", "Unknown"),
        "handle": f"@{d.get('uploader_id', d.get('channel', 'unknown'))}",
        "title": d.get("title", ""),
        "description": d.get("description", "")[:500],
        "duration": d.get("duration", 0),
        "view_count": d.get("view_count", "N/A"),
        "like_count": d.get("like_count", "N/A"),
        "comment_count": d.get("comment_count", "N/A"),
        "upload_date": d.get("upload_date", "unknown"),
        "platform": d.get("extractor", "unknown"),
        "url": d.get("webpage_url", ""),
    }


def extract_frames(video_path, output_dir, interval=0.5):
    """Extract frames at specified interval using ffmpeg."""
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    fps = 1.0 / interval  # 0.5s interval = 2 fps

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-q:v", "2",
        os.path.join(frames_dir, "frame_%04d.jpg")
    ]

    print(f"Extracting frames every {interval}s...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error extracting frames:\n{result.stderr[-500:]}")
        sys.exit(1)

    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    print(f"Extracted {len(frame_files)} frames")
    return frame_files


def extract_audio(video_path, output_dir):
    """Extract audio as WAV for transcription."""
    audio_path = os.path.join(output_dir, "ref_audio.wav")

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        audio_path
    ]

    print("Extracting audio...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Warning: Could not extract audio:\n{result.stderr[-300:]}")
        return None

    return audio_path


def transcribe(audio_path, output_dir):
    """Transcribe audio with word-level timestamps using faster-whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Warning: faster-whisper not installed. Skipping transcription.")
        print("Install with: pip3 install faster-whisper")
        return None

    print("Transcribing with word-level timestamps...")
    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(audio_path, word_timestamps=True)

    words = []
    full_text = []

    for segment in segments:
        full_text.append(segment.text.strip())
        if segment.words:
            for word in segment.words:
                words.append({
                    "start": round(word.start, 2),
                    "end": round(word.end, 2),
                    "text": word.word.strip()
                })

    # Save word timestamps
    words_path = os.path.join(output_dir, "ref_words.json")
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    # Save clean transcript
    transcript_path = os.path.join(output_dir, "ref_transcript.txt")
    with open(transcript_path, "w") as f:
        f.write(" ".join(full_text))

    print(f"Transcribed {len(words)} words")
    return {"words_path": words_path, "transcript_path": transcript_path, "word_count": len(words)}


def main():
    parser = argparse.ArgumentParser(description="Video Cloner Frame Extractor")
    parser.add_argument("--url", "-u", help="Video URL (Instagram/TikTok/YouTube)")
    parser.add_argument("--file", "-f", help="Local video file path")
    parser.add_argument("--output", "-o", default=os.path.expanduser("~/.tmp/ref_analysis"),
                        help="Output directory (default: ~/.tmp/ref_analysis)")
    parser.add_argument("--interval", "-i", type=float, default=0.5,
                        help="Frame extraction interval in seconds (default: 0.5)")
    parser.add_argument("--skip-transcribe", action="store_true",
                        help="Skip transcription step")

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error("Either --url or --file is required")

    os.makedirs(args.output, exist_ok=True)

    # Step 1: Get video file
    if args.url:
        video_path = download_video(args.url, args.output)
        metadata = extract_metadata(args.output)
    else:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        video_path = args.file
        metadata = {}

    # Step 2: Get video info
    video_info = get_video_info(video_path)
    print(f"\nVideo: {video_info.get('width', '?')}x{video_info.get('height', '?')} "
          f"({video_info.get('orientation', '?')}) — {video_info['duration']:.1f}s "
          f"— {video_info['file_size_mb']}MB")

    expected_frames = int(video_info["duration"] / args.interval) + 1
    print(f"Expected frames: ~{expected_frames} (every {args.interval}s)")

    # Step 3: Extract frames
    frame_files = extract_frames(video_path, args.output, args.interval)

    # Step 4: Extract audio + transcribe
    transcript_info = None
    if not args.skip_transcribe:
        audio_path = extract_audio(video_path, args.output)
        if audio_path:
            transcript_info = transcribe(audio_path, args.output)

    # Step 5: Save analysis manifest
    manifest = {
        "video_path": video_path,
        "output_dir": args.output,
        "interval": args.interval,
        "total_frames": len(frame_files),
        "video_info": video_info,
        "metadata": metadata,
        "transcript": transcript_info,
        "frames_dir": os.path.join(args.output, "frames"),
    }

    manifest_path = os.path.join(args.output, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Report
    print(f"\n{'='*60}")
    print(f"  Frame Extraction Complete")
    print(f"{'='*60}")
    print(f"  Video:      {os.path.basename(video_path)}")
    print(f"  Resolution: {video_info.get('width', '?')}x{video_info.get('height', '?')}")
    print(f"  Duration:   {video_info['duration']:.1f}s")
    print(f"  Frames:     {len(frame_files)} (every {args.interval}s)")
    if metadata:
        print(f"  Creator:    {metadata.get('creator', 'N/A')} ({metadata.get('handle', '')})")
        print(f"  Views:      {metadata.get('view_count', 'N/A')}")
    if transcript_info:
        print(f"  Words:      {transcript_info['word_count']}")
    print(f"  Output:     {args.output}")
    print(f"  Manifest:   {manifest_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
