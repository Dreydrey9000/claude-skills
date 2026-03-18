#!/usr/bin/env python3
"""
Vibe Editor Clip Processor
Processes raw footage into viral clips using FFmpeg based on NRVES cut list.

Usage:
    python clip_processor.py input.mp4 --cuts cuts.json --output output.mp4
    python clip_processor.py input.mp4 --start 00:00:05 --end 00:00:25 --output clip.mp4
"""

import subprocess
import json
import argparse
import os
from pathlib import Path


def time_to_seconds(time_str: str) -> float:
    """Convert MM:SS or HH:MM:SS to seconds."""
    parts = time_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return float(time_str)


def seconds_to_time(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def cut_clip(input_file: str, start: str, end: str, output_file: str, 
             reencode: bool = True) -> bool:
    """
    Cut a single clip from input video.
    
    Args:
        input_file: Path to source video
        start: Start timestamp (MM:SS or HH:MM:SS)
        end: End timestamp (MM:SS or HH:MM:SS)
        output_file: Path for output clip
        reencode: If True, re-encode for precise cuts (slower but accurate)
    """
    cmd = ['ffmpeg', '-y', '-i', input_file, '-ss', start, '-to', end]
    
    if reencode:
        # Re-encode for frame-accurate cuts
        cmd.extend([
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '18',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-avoid_negative_ts', 'make_zero'
        ])
    else:
        # Stream copy (fast but may have keyframe issues)
        cmd.extend(['-c', 'copy'])
    
    cmd.append(output_file)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def concat_clips(clip_files: list, output_file: str) -> bool:
    """
    Concatenate multiple clips into one video.
    
    Args:
        clip_files: List of clip file paths in order
        output_file: Path for concatenated output
    """
    # Create temporary file list
    list_file = '/tmp/concat_list.txt'
    with open(list_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{os.path.abspath(clip)}'\n")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(list_file)
    return result.returncode == 0


def speed_adjust(input_file: str, output_file: str, speed: float = 1.2) -> bool:
    """
    Adjust video speed (tighten pacing).
    
    Args:
        input_file: Path to source video
        output_file: Path for output
        speed: Speed multiplier (1.2 = 20% faster)
    """
    pts_factor = 1 / speed
    atempo = speed
    
    # Handle atempo limits (0.5 to 2.0)
    atempo_filters = []
    while atempo > 2.0:
        atempo_filters.append('atempo=2.0')
        atempo /= 2.0
    while atempo < 0.5:
        atempo_filters.append('atempo=0.5')
        atempo *= 2.0
    atempo_filters.append(f'atempo={atempo}')
    
    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-filter:v', f'setpts={pts_factor}*PTS',
        '-filter:a', ','.join(atempo_filters),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def extract_audio(input_file: str, output_file: str) -> bool:
    """
    Extract audio for transcription (Whisper-compatible format).
    
    Args:
        input_file: Path to source video
        output_file: Path for audio output (recommend .wav)
    """
    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # 16-bit PCM
        '-ar', '16000',  # 16kHz sample rate
        '-ac', '1',  # Mono
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def process_cut_list(input_file: str, cuts_file: str, output_dir: str) -> list:
    """
    Process a JSON cut list and generate all clips.
    
    Cut list format:
    {
        "clips": [
            {"name": "hook", "start": "0:00", "end": "0:05", "action": "keep"},
            {"name": "story", "start": "0:08", "end": "0:20", "action": "keep"},
            {"name": "filler", "start": "0:05", "end": "0:08", "action": "cut"}
        ],
        "restructure": ["story", "hook"],  # Optional: new order
        "speed_sections": [
            {"start": "0:12", "end": "0:15", "speed": 1.3}
        ]
    }
    """
    with open(cuts_file) as f:
        cut_data = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each clip marked as "keep"
    generated_clips = []
    for clip in cut_data.get('clips', []):
        if clip.get('action') == 'keep':
            output_path = os.path.join(output_dir, f"{clip['name']}.mp4")
            success = cut_clip(input_file, clip['start'], clip['end'], output_path)
            if success:
                generated_clips.append({
                    'name': clip['name'],
                    'path': output_path,
                    'start': clip['start'],
                    'end': clip['end']
                })
                print(f"✓ Cut: {clip['name']} ({clip['start']} - {clip['end']})")
            else:
                print(f"✗ Failed: {clip['name']}")
    
    # Apply speed adjustments if specified
    for speed_section in cut_data.get('speed_sections', []):
        for clip in generated_clips:
            # Check if this clip overlaps with speed section
            # (Simplified: apply to matching clips by name)
            if clip.get('speed'):
                temp_path = clip['path'] + '.speed.mp4'
                if speed_adjust(clip['path'], temp_path, clip['speed']):
                    os.replace(temp_path, clip['path'])
                    print(f"✓ Speed adjusted: {clip['name']} @ {clip['speed']}x")
    
    # Restructure if specified
    restructure_order = cut_data.get('restructure', [])
    if restructure_order:
        ordered_clips = []
        for name in restructure_order:
            for clip in generated_clips:
                if clip['name'] == name:
                    ordered_clips.append(clip['path'])
                    break
        
        if ordered_clips:
            final_output = os.path.join(output_dir, 'final_restructured.mp4')
            if concat_clips(ordered_clips, final_output):
                print(f"✓ Restructured: {' → '.join(restructure_order)}")
                return final_output
    
    return generated_clips


def main():
    parser = argparse.ArgumentParser(description='Vibe Editor Clip Processor')
    parser.add_argument('input', help='Input video file')
    parser.add_argument('--start', '-s', help='Start timestamp (MM:SS)')
    parser.add_argument('--end', '-e', help='End timestamp (MM:SS)')
    parser.add_argument('--cuts', '-c', help='JSON cut list file')
    parser.add_argument('--output', '-o', default='output.mp4', help='Output file/directory')
    parser.add_argument('--speed', type=float, help='Speed adjustment (e.g., 1.2)')
    parser.add_argument('--extract-audio', action='store_true', help='Extract audio only')
    parser.add_argument('--fast', action='store_true', help='Use stream copy (fast but less accurate)')
    
    args = parser.parse_args()
    
    if args.extract_audio:
        output = args.output if args.output.endswith('.wav') else args.output.replace('.mp4', '.wav')
        if extract_audio(args.input, output):
            print(f"✓ Audio extracted: {output}")
        else:
            print("✗ Audio extraction failed")
    
    elif args.cuts:
        results = process_cut_list(args.input, args.cuts, args.output)
        print(f"\n✓ Processed {len(results) if isinstance(results, list) else 1} clips")
    
    elif args.start and args.end:
        if cut_clip(args.input, args.start, args.end, args.output, reencode=not args.fast):
            print(f"✓ Clip created: {args.output}")
            if args.speed:
                temp = args.output + '.speed.mp4'
                if speed_adjust(args.output, temp, args.speed):
                    os.replace(temp, args.output)
                    print(f"✓ Speed adjusted: {args.speed}x")
        else:
            print("✗ Clip creation failed")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
