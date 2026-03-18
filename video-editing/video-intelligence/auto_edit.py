#!/usr/bin/env python3
"""
Video Intelligence — Autonomous Video Editor
Combines Hume AI, Twelve Labs, PySceneDetect, MediaPipe for fully automated editing.

Usage:
    python3 auto_edit.py --input video.mp4 --output clips/ --target-duration 60

Environment:
    HUME_API_KEY - Hume AI API key
    TWELVE_LABS_API_KEY - Twelve Labs API key
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Check for required packages
def check_imports():
    missing = []
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    try:
        import mediapipe
    except ImportError:
        missing.append("mediapipe")
    try:
        from scenedetect import detect, ContentDetector
    except ImportError:
        missing.append("scenedetect")

    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print(f"Install with: pip3 install {' '.join(missing)}")
        sys.exit(1)

check_imports()

import cv2
import mediapipe as mp
from scenedetect import detect, ContentDetector

# ============================================
# SCENE DETECTION
# ============================================

def detect_scenes(video_path: str) -> list:
    """Detect scene boundaries using PySceneDetect."""
    print(f"[1/7] Detecting scenes in {video_path}...")
    scene_list = detect(video_path, ContentDetector())
    scenes = []
    for i, scene in enumerate(scene_list):
        scenes.append({
            "index": i,
            "start": scene[0].get_seconds(),
            "end": scene[1].get_seconds(),
            "duration": scene[1].get_seconds() - scene[0].get_seconds()
        })
    print(f"    Found {len(scenes)} scenes")
    return scenes

# ============================================
# TRANSCRIPTION (Whisper)
# ============================================

def transcribe_audio(video_path: str, output_dir: str) -> dict:
    """Extract audio and transcribe with Whisper."""
    print(f"[2/7] Transcribing audio...")

    audio_path = os.path.join(output_dir, "audio.wav")

    # Extract audio
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000",
        audio_path
    ], capture_output=True)

    # Try mlx_whisper first, fall back to whisper
    try:
        import mlx_whisper
        result = mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
            word_timestamps=True
        )
        print(f"    Transcribed {len(result.get('segments', []))} segments")
        return result
    except ImportError:
        print("    mlx_whisper not found, trying whisper...")
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, word_timestamps=True)
            return result
        except ImportError:
            print("    No whisper found. Skipping transcription.")
            return {"segments": []}

# ============================================
# EMOTION DETECTION (Hume AI)
# ============================================

def analyze_emotions(audio_path: str) -> list:
    """Analyze audio for emotion peaks using Hume AI."""
    print(f"[3/7] Analyzing emotions with Hume AI...")

    api_key = os.environ.get("HUME_API_KEY")
    if not api_key:
        print("    HUME_API_KEY not set. Skipping emotion analysis.")
        return []

    try:
        from hume import HumeClient
        from hume.models.config import ProsodyConfig

        client = HumeClient(api_key=api_key)

        job = client.expression_measurement.batch.start_inference_job(
            files=[audio_path],
            models=[ProsodyConfig()]
        )

        # Wait for job
        import time
        while True:
            status = client.expression_measurement.batch.get_job_status(job.job_id)
            if status.state == "COMPLETED":
                break
            time.sleep(2)

        results = client.expression_measurement.batch.get_job_predictions(job.job_id)

        # Extract emotion peaks
        peaks = []
        for prediction in results:
            for segment in prediction.prosody.predictions:
                emotions = {e.name: e.score for e in segment.emotions}
                peak_emotion = max(emotions, key=emotions.get)
                if emotions[peak_emotion] > 0.5:  # Threshold
                    peaks.append({
                        "time": segment.time,
                        "emotion": peak_emotion,
                        "score": emotions[peak_emotion]
                    })

        print(f"    Found {len(peaks)} emotion peaks")
        return peaks

    except Exception as e:
        print(f"    Hume error: {e}")
        return []

# ============================================
# VIDEO UNDERSTANDING (Twelve Labs)
# ============================================

def search_video_moments(video_path: str, queries: list) -> list:
    """Search video for specific moments using Twelve Labs."""
    print(f"[4/7] Indexing video with Twelve Labs...")

    api_key = os.environ.get("TWELVE_LABS_API_KEY")
    if not api_key:
        print("    TWELVE_LABS_API_KEY not set. Skipping video search.")
        return []

    try:
        from twelvelabs import TwelveLabsClient

        client = TwelveLabsClient(api_key=api_key)

        # Create temporary index
        index = client.index.create(
            name=f"temp-{os.path.basename(video_path)}",
            engines=["marengo2.6"]
        )

        # Upload video
        task = client.task.create(index_id=index.id, file=video_path)
        task.wait_for_done()

        # Search for moments
        all_results = []
        for query in queries:
            results = client.search.query(
                index_id=index.id,
                query=query,
                search_options=["visual", "audio"]
            )
            for clip in results.data:
                all_results.append({
                    "query": query,
                    "start": clip.start,
                    "end": clip.end,
                    "score": clip.score
                })

        # Cleanup
        client.index.delete(index.id)

        print(f"    Found {len(all_results)} matching moments")
        return all_results

    except Exception as e:
        print(f"    Twelve Labs error: {e}")
        return []

# ============================================
# FACE TRACKING (MediaPipe)
# ============================================

def get_face_positions(video_path: str, timestamps: list) -> dict:
    """Get face positions at specific timestamps for auto-reframe."""
    print(f"[5/7] Tracking faces for auto-reframe...")

    mp_face = mp.solutions.face_detection
    face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    positions = {}

    for ts in timestamps:
        frame_num = int(ts * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()

        if ret:
            results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                positions[ts] = {
                    "x": bbox.xmin + bbox.width / 2,
                    "y": bbox.ymin + bbox.height / 2
                }
            else:
                positions[ts] = {"x": 0.5, "y": 0.5}

    cap.release()
    print(f"    Tracked {len(positions)} face positions")
    return positions

# ============================================
# CLIP EXTRACTION
# ============================================

def extract_clips(video_path: str, moments: list, output_dir: str, vertical: bool = True) -> list:
    """Extract and optionally reframe clips."""
    print(f"[6/7] Extracting {len(moments)} clips...")

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    clips = []

    for i, moment in enumerate(moments):
        output_path = os.path.join(output_dir, f"clip_{i:03d}.mp4")

        # Build FFmpeg command
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(moment["start"]),
            "-i", video_path,
            "-t", str(moment["end"] - moment["start"]),
        ]

        if vertical:
            # Calculate 9:16 crop
            target_width = int(height * 9 / 16)
            x_offset = (width - target_width) // 2

            # Adjust for face position if available
            if "face_x" in moment:
                center_pixel = int(moment["face_x"] * width)
                x_offset = max(0, min(width - target_width, center_pixel - target_width // 2))

            cmd.extend([
                "-vf", f"crop={target_width}:{height}:{x_offset}:0",
            ])

        cmd.extend([
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            output_path
        ])

        subprocess.run(cmd, capture_output=True)
        clips.append(output_path)
        print(f"    Extracted clip {i+1}/{len(moments)}")

    return clips

# ============================================
# MOMENT SCORING (BEAR Formula)
# ============================================

def score_moments(scenes: list, emotions: list, search_results: list, transcript: dict) -> list:
    """Score moments using BEAR formula and combine all signals."""
    print(f"[7/7] Scoring moments with BEAR formula...")

    # Combine all signals into candidate moments
    candidates = []

    # Add scenes with minimum duration
    for scene in scenes:
        if scene["duration"] >= 5:  # At least 5 seconds
            candidates.append({
                "start": scene["start"],
                "end": scene["end"],
                "source": "scene",
                "score": 0.5
            })

    # Boost scenes with emotion peaks
    for peak in emotions:
        for c in candidates:
            if c["start"] <= peak["time"] <= c["end"]:
                c["score"] += 0.2  # Emotion boost
                c["emotion"] = peak["emotion"]

    # Boost scenes matching search queries
    for result in search_results:
        for c in candidates:
            if (c["start"] <= result["start"] <= c["end"] or
                c["start"] <= result["end"] <= c["end"]):
                c["score"] += result["score"] * 0.3  # Search relevance boost

    # Sort by score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    print(f"    Scored {len(candidates)} candidate moments")
    return candidates

# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Autonomous Video Editor")
    parser.add_argument("--input", "-i", required=True, help="Input video path")
    parser.add_argument("--output", "-o", default="./clips", help="Output directory")
    parser.add_argument("--target-duration", "-t", type=int, default=60, help="Target clip duration (seconds)")
    parser.add_argument("--max-clips", "-n", type=int, default=5, help="Maximum clips to extract")
    parser.add_argument("--vertical", action="store_true", help="Crop to 9:16 vertical")
    parser.add_argument("--queries", nargs="+", default=[
        "speaker gets excited",
        "emotional moment",
        "key insight or advice",
        "surprising revelation"
    ], help="Search queries for Twelve Labs")

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print(f"\n{'='*60}")
    print("VIDEO INTELLIGENCE — AUTONOMOUS EDITOR")
    print(f"{'='*60}\n")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Target duration: {args.target_duration}s")
    print(f"Vertical crop: {args.vertical}\n")

    # Run pipeline
    scenes = detect_scenes(args.input)
    transcript = transcribe_audio(args.input, args.output)

    audio_path = os.path.join(args.output, "audio.wav")
    emotions = analyze_emotions(audio_path) if os.path.exists(audio_path) else []

    search_results = search_video_moments(args.input, args.queries)

    # Score and select best moments
    scored = score_moments(scenes, emotions, search_results, transcript)

    # Select top moments within target duration
    selected = []
    total_duration = 0
    for moment in scored:
        if total_duration + moment["end"] - moment["start"] <= args.target_duration:
            selected.append(moment)
            total_duration += moment["end"] - moment["start"]
        if len(selected) >= args.max_clips:
            break

    if not selected:
        print("\nNo suitable moments found. Using top scenes by duration.")
        selected = scenes[:args.max_clips]

    # Get face positions for selected moments
    timestamps = [m["start"] for m in selected]
    face_positions = get_face_positions(args.input, timestamps)

    # Add face positions to moments
    for moment in selected:
        if moment["start"] in face_positions:
            moment["face_x"] = face_positions[moment["start"]]["x"]

    # Extract clips
    clips = extract_clips(args.input, selected, args.output, args.vertical)

    # Save metadata
    metadata = {
        "input": args.input,
        "scenes_detected": len(scenes),
        "emotion_peaks": len(emotions),
        "search_matches": len(search_results),
        "clips_extracted": len(clips),
        "clips": clips,
        "moments": selected
    }

    with open(os.path.join(args.output, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'='*60}")
    print("COMPLETE")
    print(f"{'='*60}")
    print(f"Extracted {len(clips)} clips to {args.output}/")
    print(f"Metadata saved to {args.output}/metadata.json")

if __name__ == "__main__":
    main()
