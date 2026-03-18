#!/usr/bin/env python3
"""
/transcribe-videos - Claude Code Slash Command
Viral Editz Edition with NRVES Framework Integration

Downloads YouTube videos, transcribes with Whisper, and extracts viral patterns
using the NRVES framework (Navigate, Restructure, Visualize, Enhance, Submit).

Installation:
  mkdir -p ~/.claude/commands
  cp transcribe_videos.py ~/.claude/commands/
  chmod +x ~/.claude/commands/transcribe_videos.py

Usage in Claude Code:
  /transcribe-videos https://youtube.com/watch?v=VIDEO_ID
  /transcribe-videos https://youtube.com/playlist?list=PLAYLIST_ID
  /transcribe-videos urls.txt
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_DIR = Path.home() / ".claude" / "video-transcripts"
SKILL_OUTPUT = Path.cwd() / ".claude" / "skills" / "extracted-knowledge"
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "medium")
MAX_VIDEOS = 50  # Safety limit

# ═══════════════════════════════════════════════════════════════════════════════
# NRVES FRAMEWORK (Viral Editz System)
# ═══════════════════════════════════════════════════════════════════════════════

NRVES_FRAMEWORK = """
## NRVES Framework (Viral Editz)

### N - NAVIGATE (Find the Value)
- What's the ONE transformation, insight, or emotional hook?
- If you can't state the value in one sentence, there's no video
- Kill threshold: If no clear value in first pass, skip the video

### R - RESTRUCTURE (Cut and Reorder)  
- Apply CUB Test to every segment:
  • C = Confusing → ADD context or CUT entirely
  • U = Unbelievable → ADD proof or CUT entirely  
  • B = Boring → CUT immediately, no exceptions
- Hook-first editing: Start with strongest moment, not chronologically
- Cut list format: [START_TIME - END_TIME] | KEEP/CUT | REASON

### V - VISUALIZE (Add What's Missing)
- For each CUB flag, prescribe the visual fix:
  • Confusing → Text overlay explaining context
  • Unbelievable → Screenshot/proof image
  • Boring → Pattern interrupt (zoom, B-roll, sound effect)
- Visual prescription format: [TIMESTAMP] | CUB_FLAG | VISUAL_FIX

### E - ENHANCE (Triple Hook Layer)
- Layer 1 (Visual): What appears on screen in first 0.5 seconds
- Layer 2 (Audio): What's heard in first 1 second  
- Layer 3 (Written): Caption/text hook in first 2 seconds
- All three layers must work independently AND together

### S - SUBMIT (Split Test)
- Create 2-3 hook variations for A/B testing
- Never release single version without split test data
"""

# Hook patterns to detect in transcripts
HOOK_PATTERNS = {
    "result_first": [
        r"(\d+[kKmM]?\+?)\s+(followers?|subscribers?|views?|dollars?|\$)",
        r"made\s+\$?\d+",
        r"grew\s+\w+\s+by\s+\d+",
        r"went\s+from\s+\d+\s+to\s+\d+",
    ],
    "contrarian": [
        r"everyone\s+(thinks?|says?|believes?)",
        r"most\s+people\s+(don'?t|never|won'?t)",
        r"stop\s+(doing|trying|using)",
        r"you'?re\s+doing\s+it\s+wrong",
        r"the\s+real\s+reason",
        r"what\s+they\s+don'?t\s+tell",
    ],
    "curiosity_gap": [
        r"here'?s?\s+(why|how|what)",
        r"the\s+(secret|trick|key)\s+(to|is)",
        r"nobody\s+(talks?|knows?)\s+about",
        r"you\s+won'?t\s+believe",
    ],
    "tension": [
        r"(but|however|except)\s+here'?s?\s+the\s+(thing|problem)",
        r"until\s+(I|you|they)",
        r"that'?s?\s+when\s+(everything|it\s+all)",
        r"plot\s+twist",
    ],
    "disbelief": [
        r"I\s+(couldn'?t|can'?t)\s+believe",
        r"this\s+(changed|blew|shocked)",
        r"in\s+just\s+\d+\s+(days?|hours?|minutes?|seconds?)",
        r"with\s+(no|zero|0)\s+",
    ],
}

# Words/phrases that indicate boring content (CUB - Boring)
BORING_INDICATORS = [
    "um", "uh", "like", "you know", "basically", "actually", "literally",
    "so yeah", "and stuff", "kind of", "sort of", "i mean", "i guess",
    "let me think", "hold on", "wait", "anyway", "moving on",
]

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def run_cmd(cmd: List[str], timeout: int = 3600) -> Tuple[bool, str]:
    """Execute shell command and return (success, output)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "⏱️ Command timed out"
    except Exception as e:
        return False, f"❌ Error: {e}"


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def check_dependencies() -> bool:
    """Verify required tools are installed."""
    deps = {
        'yt-dlp': 'pip install yt-dlp',
        'whisper': 'pip install openai-whisper',
    }
    missing = []
    for cmd, install in deps.items():
        success, _ = run_cmd(['which', cmd])
        if not success:
            missing.append(f"  {cmd}: {install}")
    
    if missing:
        print("❌ Missing dependencies:")
        print("\n".join(missing))
        return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# YOUTUBE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_video_info(url: str) -> Dict:
    """Fetch video metadata."""
    cmd = ['yt-dlp', '--dump-json', '--no-download', url]
    success, output = run_cmd(cmd, timeout=60)
    if success:
        try:
            return json.loads(output.strip().split('\n')[0])
        except:
            pass
    return {}


def get_playlist_urls(playlist_url: str) -> List[str]:
    """Extract video URLs from playlist."""
    cmd = ['yt-dlp', '--flat-playlist', '--get-id', playlist_url]
    success, output = run_cmd(cmd)
    if not success:
        return []
    
    urls = []
    for vid_id in output.strip().split('\n'):
        if vid_id and len(vid_id) == 11:
            urls.append(f"https://www.youtube.com/watch?v={vid_id}")
    return urls[:MAX_VIDEOS]


def download_audio(url: str, output_dir: Path) -> Optional[Path]:
    """Download audio from YouTube."""
    video_id = extract_video_id(url)
    if not video_id:
        return None
    
    output_path = output_dir / f"{video_id}.wav"
    if output_path.exists():
        return output_path
    
    cmd = [
        'yt-dlp', '-x',
        '--audio-format', 'wav',
        '--audio-quality', '0',
        '-o', str(output_dir / '%(id)s.%(ext)s'),
        '--no-playlist',
        url
    ]
    success, _ = run_cmd(cmd)
    
    # Find the file (might have different extension initially)
    if output_path.exists():
        return output_path
    
    for ext in ['wav', 'm4a', 'mp3', 'webm']:
        p = output_dir / f"{video_id}.{ext}"
        if p.exists():
            return p
    
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# TRANSCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════

def transcribe(audio_path: Path, output_dir: Path) -> Optional[Dict]:
    """Transcribe audio with Whisper."""
    cmd = [
        'whisper', str(audio_path),
        '--model', WHISPER_MODEL,
        '--output_dir', str(output_dir),
        '--output_format', 'all',
        '--language', 'en',
    ]
    success, _ = run_cmd(cmd)
    
    if success:
        json_path = output_dir / f"{audio_path.stem}.json"
        if json_path.exists():
            with open(json_path) as f:
                return json.load(f)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# NRVES PATTERN EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def detect_hooks(text: str, segments: List[Dict]) -> List[Dict]:
    """Find potential hook moments using NRVES patterns."""
    hooks = []
    
    for seg in segments:
        seg_text = seg.get('text', '').strip()
        seg_start = seg.get('start', 0)
        
        for hook_type, patterns in HOOK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, seg_text, re.IGNORECASE):
                    hooks.append({
                        'timestamp': format_time(seg_start),
                        'seconds': seg_start,
                        'type': hook_type,
                        'text': seg_text,
                        'pattern': pattern,
                    })
                    break
    
    # Sort by strength (result_first > contrarian > others)
    type_order = {'result_first': 0, 'contrarian': 1, 'disbelief': 2, 'curiosity_gap': 3, 'tension': 4}
    hooks.sort(key=lambda x: type_order.get(x['type'], 5))
    
    return hooks[:10]  # Top 10 hooks


def detect_cub_flags(segments: List[Dict]) -> List[Dict]:
    """Apply CUB test to identify problems."""
    flags = []
    
    for seg in segments:
        seg_text = seg.get('text', '').lower().strip()
        seg_start = seg.get('start', 0)
        
        # BORING: Filler words, hedging
        boring_count = sum(1 for b in BORING_INDICATORS if b in seg_text)
        if boring_count >= 2:
            flags.append({
                'timestamp': format_time(seg_start),
                'seconds': seg_start,
                'type': 'BORING',
                'reason': f"Filler detected ({boring_count} instances)",
                'action': 'CUT',
                'text': seg.get('text', ''),
            })
        
        # CONFUSING: Questions without answers, jargon
        if '?' in seg_text and len(seg_text.split()) < 8:
            flags.append({
                'timestamp': format_time(seg_start),
                'seconds': seg_start,
                'type': 'CONFUSING',
                'reason': 'Unclear question/reference',
                'action': 'ADD context overlay',
                'text': seg.get('text', ''),
            })
        
        # UNBELIEVABLE: Claims without proof
        claim_patterns = [
            r'\d+[xX%]', r'guarantee', r'always', r'never fails',
            r'everyone', r'nobody', r'best\s+\w+\s+ever'
        ]
        for pattern in claim_patterns:
            if re.search(pattern, seg_text):
                flags.append({
                    'timestamp': format_time(seg_start),
                    'seconds': seg_start,
                    'type': 'UNBELIEVABLE',
                    'reason': 'Claim needs proof',
                    'action': 'ADD proof screenshot',
                    'text': seg.get('text', ''),
                })
                break
    
    return flags


def extract_techniques(text: str) -> List[Dict]:
    """Extract specific techniques, commands, workflows mentioned."""
    techniques = []
    
    # Commands (shell, npm, pip, etc.)
    cmd_patterns = [
        (r'(?:run|execute|type)\s+[`"\']?([a-zA-Z][a-zA-Z0-9_\-\s\.]+)[`"\']?', 'command'),
        (r'(npm\s+(?:run|install|init)\s+\S+)', 'npm'),
        (r'(npx\s+\S+)', 'npx'),
        (r'(pip\s+install\s+\S+)', 'pip'),
        (r'(ffmpeg\s+[^\.]+)', 'ffmpeg'),
        (r'(claude\s+\S+)', 'claude'),
    ]
    
    for pattern, cmd_type in cmd_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            techniques.append({
                'type': 'command',
                'subtype': cmd_type,
                'value': match.group(1).strip(),
            })
    
    # Framework references
    framework_indicators = [
        'framework', 'system', 'method', 'process', 'workflow',
        'step one', 'step two', 'step 1', 'step 2',
        'first step', 'the key is', 'the secret is',
    ]
    
    sentences = re.split(r'[.!?]', text)
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for indicator in framework_indicators:
            if indicator in sentence_lower and len(sentence.split()) > 5:
                techniques.append({
                    'type': 'framework',
                    'value': sentence.strip(),
                })
                break
    
    return techniques


def extract_quotes(segments: List[Dict]) -> List[Dict]:
    """Find quotable moments (short, punchy statements)."""
    quotes = []
    
    strong_starters = [
        r'^the (key|secret|trick|answer|truth)',
        r'^(never|always|stop|start|quit)',
        r'^(most people|everyone|nobody)',
        r'^this (is|was|will|changes)',
        r'^(here\'?s|that\'?s) (the thing|why|how)',
        r'^(you|they|we) (don\'?t|won\'?t|can\'?t)',
    ]
    
    for seg in segments:
        seg_text = seg.get('text', '').strip()
        word_count = len(seg_text.split())
        
        # Ideal quote length: 5-25 words
        if not (5 <= word_count <= 25):
            continue
        
        for pattern in strong_starters:
            if re.search(pattern, seg_text.lower()):
                quotes.append({
                    'timestamp': format_time(seg.get('start', 0)),
                    'text': seg_text,
                    'words': word_count,
                })
                break
    
    return quotes[:20]  # Top 20


# ═══════════════════════════════════════════════════════════════════════════════
# NRVES ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def run_nrves_analysis(transcript: Dict, video_info: Dict) -> Dict:
    """Full NRVES analysis on a transcript."""
    text = transcript.get('text', '')
    segments = transcript.get('segments', [])
    
    analysis = {
        'meta': {
            'title': video_info.get('title', 'Unknown'),
            'channel': video_info.get('channel', 'Unknown'),
            'url': video_info.get('webpage_url', ''),
            'duration': video_info.get('duration', 0),
            'duration_formatted': format_time(video_info.get('duration', 0)),
        },
        'N_navigate': {
            'description': 'Find the ONE value/transformation',
            'hooks': detect_hooks(text, segments),
            'best_hook': None,
        },
        'R_restructure': {
            'description': 'CUB test and cut list',
            'cub_flags': detect_cub_flags(segments),
            'suggested_cuts': [],
        },
        'V_visualize': {
            'description': 'Visual fixes for CUB flags',
            'visual_prescriptions': [],
        },
        'E_enhance': {
            'description': 'Triple hook layer suggestions',
            'hook_layers': [],
        },
        'S_submit': {
            'description': 'Split test variations',
            'variations': [],
        },
        'extracted': {
            'techniques': extract_techniques(text),
            'quotes': extract_quotes(segments),
            'full_text': text,
        },
    }
    
    # Set best hook
    if analysis['N_navigate']['hooks']:
        analysis['N_navigate']['best_hook'] = analysis['N_navigate']['hooks'][0]
    
    # Generate cut list from CUB flags
    for flag in analysis['R_restructure']['cub_flags']:
        if flag['type'] == 'BORING':
            analysis['R_restructure']['suggested_cuts'].append({
                'timestamp': flag['timestamp'],
                'action': 'CUT',
                'reason': flag['reason'],
            })
    
    # Visual prescriptions from CUB
    for flag in analysis['R_restructure']['cub_flags']:
        if flag['type'] == 'CONFUSING':
            analysis['V_visualize']['visual_prescriptions'].append({
                'timestamp': flag['timestamp'],
                'type': 'text_overlay',
                'content': f"Add context for: {flag['text'][:50]}...",
            })
        elif flag['type'] == 'UNBELIEVABLE':
            analysis['V_visualize']['visual_prescriptions'].append({
                'timestamp': flag['timestamp'],
                'type': 'proof_screenshot',
                'content': f"Add proof for claim: {flag['text'][:50]}...",
            })
    
    # Hook layer suggestions
    if analysis['N_navigate']['best_hook']:
        hook = analysis['N_navigate']['best_hook']
        analysis['E_enhance']['hook_layers'] = [
            {'layer': 'visual', 'suggestion': f"Show result/transformation at {hook['timestamp']}"},
            {'layer': 'audio', 'suggestion': f"Lead with: \"{hook['text'][:60]}...\""},
            {'layer': 'text', 'suggestion': f"Caption: {hook['text'][:40]}..."},
        ]
    
    # Split test variations
    hooks = analysis['N_navigate']['hooks'][:3]
    for i, hook in enumerate(hooks, 1):
        analysis['S_submit']['variations'].append({
            'version': f"V{i}",
            'hook_type': hook['type'],
            'opening': hook['text'][:80],
            'timestamp': hook['timestamp'],
        })
    
    return analysis


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_skill_file(analyses: List[Dict], output_dir: Path) -> Path:
    """Generate skill reference markdown from all analyses."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = output_dir / f"video_knowledge_{timestamp}.md"
    
    with open(output_path, 'w') as f:
        # Header
        f.write("# 🎬 Extracted Video Knowledge\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Videos Processed:** {len(analyses)}\n")
        f.write(f"**Framework:** NRVES (Viral Editz)\n\n")
        f.write("---\n\n")
        
        # NRVES Framework Reference
        f.write(NRVES_FRAMEWORK)
        f.write("\n---\n\n")
        
        # Aggregated Best Hooks
        f.write("## 🎯 Top Hooks Found (All Videos)\n\n")
        all_hooks = []
        for a in analyses:
            for hook in a['N_navigate']['hooks'][:3]:
                all_hooks.append({
                    'source': a['meta']['title'][:40],
                    **hook
                })
        
        for hook in all_hooks[:15]:
            f.write(f"**[{hook['type'].upper()}]** @ {hook['timestamp']}\n")
            f.write(f"> \"{hook['text']}\"\n")
            f.write(f"*Source: {hook['source']}*\n\n")
        
        f.write("---\n\n")
        
        # Aggregated Quotes
        f.write("## 💬 Quotable Moments\n\n")
        all_quotes = []
        for a in analyses:
            for q in a['extracted']['quotes'][:5]:
                all_quotes.append({
                    'source': a['meta']['title'][:40],
                    **q
                })
        
        for q in all_quotes[:20]:
            f.write(f"> \"{q['text']}\"\n")
            f.write(f"*@ {q['timestamp']} — {q['source']}*\n\n")
        
        f.write("---\n\n")
        
        # Aggregated Commands
        f.write("## 🔧 Commands & Code Found\n\n```bash\n")
        all_cmds = set()
        for a in analyses:
            for t in a['extracted']['techniques']:
                if t['type'] == 'command':
                    all_cmds.add(t['value'])
        
        for cmd in sorted(all_cmds):
            f.write(f"{cmd}\n")
        f.write("```\n\n---\n\n")
        
        # Individual Video Analyses
        f.write("## 📹 Individual Video Analyses\n\n")
        
        for a in analyses:
            meta = a['meta']
            f.write(f"### {meta['title']}\n\n")
            f.write(f"- **Channel:** {meta['channel']}\n")
            f.write(f"- **Duration:** {meta['duration_formatted']}\n")
            f.write(f"- **URL:** {meta['url']}\n\n")
            
            # Best hook
            if a['N_navigate']['best_hook']:
                hook = a['N_navigate']['best_hook']
                f.write(f"**🎯 Best Hook ({hook['type']})** @ {hook['timestamp']}\n")
                f.write(f"> {hook['text']}\n\n")
            
            # CUB Flags
            if a['R_restructure']['cub_flags']:
                f.write("**⚠️ CUB Flags:**\n")
                for flag in a['R_restructure']['cub_flags'][:5]:
                    f.write(f"- [{flag['type']}] @ {flag['timestamp']}: {flag['action']}\n")
                f.write("\n")
            
            # Visual Prescriptions
            if a['V_visualize']['visual_prescriptions']:
                f.write("**🎨 Visual Fixes:**\n")
                for vp in a['V_visualize']['visual_prescriptions'][:3]:
                    f.write(f"- @ {vp['timestamp']}: {vp['type']} - {vp['content'][:50]}\n")
                f.write("\n")
            
            # Transcript (collapsed)
            f.write("<details>\n<summary>📝 Full Transcript</summary>\n\n")
            f.write("```\n")
            text = a['extracted']['full_text'][:8000]
            f.write(text)
            if len(a['extracted']['full_text']) > 8000:
                f.write("\n... [truncated]")
            f.write("\n```\n</details>\n\n")
            
            f.write("---\n\n")
        
        # Claude Deep Analysis Prompt
        f.write("## 🤖 Claude: Deep Knowledge Extraction\n\n")
        f.write("```\n")
        f.write("Analyze all content above using the NRVES framework.\n\n")
        f.write("Extract and organize into separate files:\n\n")
        f.write("1. HOOKS.md - All hook patterns with timestamps and types\n")
        f.write("2. TECHNIQUES.md - Every specific technique or method\n")
        f.write("3. COMMANDS.md - All commands, code, configurations\n")
        f.write("4. WORKFLOWS.md - Step-by-step processes described\n")
        f.write("5. QUOTES.md - Best quotable moments for content\n")
        f.write("6. CUB_PATTERNS.md - Common Confusing/Unbelievable/Boring patterns\n\n")
        f.write("Save to: .claude/skills/vibe-editor/references/\n")
        f.write("```\n")
    
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def process_video(url: str, cache_dir: Path) -> Optional[Dict]:
    """Process single video through full pipeline."""
    video_id = extract_video_id(url)
    if not video_id:
        print(f"  ⚠️ Invalid URL: {url}")
        return None
    
    # Check cache
    cache_file = cache_dir / f"{video_id}_nrves.json"
    if cache_file.exists():
        print(f"  ✓ Using cached analysis")
        with open(cache_file) as f:
            return json.load(f)
    
    # Get video info
    print(f"  → Fetching video info...")
    info = get_video_info(url)
    if not info:
        print(f"  ⚠️ Could not fetch video info")
        return None
    
    title = info.get('title', 'Unknown')[:50]
    print(f"  → Title: {title}...")
    
    # Download audio
    print(f"  → Downloading audio...")
    audio_path = download_audio(url, cache_dir)
    if not audio_path:
        print(f"  ⚠️ Download failed")
        return None
    
    # Transcribe
    print(f"  → Transcribing ({WHISPER_MODEL})...")
    transcript = transcribe(audio_path, cache_dir)
    if not transcript:
        print(f"  ⚠️ Transcription failed")
        return None
    
    # NRVES Analysis
    print(f"  → Running NRVES analysis...")
    analysis = run_nrves_analysis(transcript, info)
    
    # Cache result
    with open(cache_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    # Cleanup audio
    if audio_path.exists():
        audio_path.unlink()
    
    hooks = len(analysis['N_navigate']['hooks'])
    flags = len(analysis['R_restructure']['cub_flags'])
    print(f"  ✓ Complete! Found {hooks} hooks, {flags} CUB flags")
    
    return analysis


def main():
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║        /transcribe-videos - NRVES Video Analyzer             ║
║            Viral Editz Edition                               ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  /transcribe-videos <url>              Single video
  /transcribe-videos <playlist_url>     YouTube playlist  
  /transcribe-videos <file.txt>         File with URLs (one per line)

Examples:
  /transcribe-videos "https://youtube.com/watch?v=VIDEO_ID"
  /transcribe-videos "https://youtube.com/playlist?list=PLxxxx"
  /transcribe-videos my_videos.txt

Environment Variables:
  WHISPER_MODEL=medium  (tiny|base|small|medium|large)
        """)
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Parse input
    input_arg = sys.argv[1]
    urls = []
    
    if os.path.isfile(input_arg):
        with open(input_arg) as f:
            urls = [l.strip() for l in f if l.strip() and l.startswith('http')]
        print(f"📄 Loaded {len(urls)} URLs from {input_arg}")
    
    elif 'playlist' in input_arg or 'list=' in input_arg:
        print(f"📋 Fetching playlist...")
        urls = get_playlist_urls(input_arg)
        print(f"   Found {len(urls)} videos")
    
    else:
        urls = [input_arg]
    
    if not urls:
        print("❌ No valid URLs found")
        sys.exit(1)
    
    # Setup
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🎬 Processing {len(urls)} video(s) with NRVES framework")
    print(f"📂 Cache: {OUTPUT_DIR}")
    print(f"🎤 Whisper: {WHISPER_MODEL}\n")
    
    # Process each video
    analyses = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url[:60]}...")
        result = process_video(url, OUTPUT_DIR)
        if result:
            analyses.append(result)
    
    if not analyses:
        print("\n❌ No videos processed successfully")
        sys.exit(1)
    
    # Generate output
    print(f"\n→ Generating skill reference file...")
    output_path = generate_skill_file(analyses, SKILL_OUTPUT)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    ✅ COMPLETE                                ║
╚══════════════════════════════════════════════════════════════╝

📊 Processed: {len(analyses)}/{len(urls)} videos
📄 Output: {output_path}

Next Steps:
1. Review the extracted hooks and patterns
2. Ask Claude to do deep analysis:
   
   "Read {output_path.name} and extract all techniques 
    into my vibe-editor skill references"

3. Or inject directly into your skill:
   
   "Add the best patterns from this file to 
    .claude/skills/vibe-editor/references/"
    """)


if __name__ == '__main__':
    main()
