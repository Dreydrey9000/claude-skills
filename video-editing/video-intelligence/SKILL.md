---
name: video-intelligence
description: Autonomous video editing using AI-powered video intelligence. Combines Hume AI (emotion detection), Twelve Labs (video understanding), PySceneDetect (scene boundaries), and MediaPipe (face tracking auto-reframe) to automatically find viral moments, detect energy peaks, and edit videos without manual scrubbing. Use when Drey wants to automate video editing, find viral clips autonomously, or process videos end-to-end.
---

# Video Intelligence — Autonomous Video Editing

AI-powered pipeline that watches videos like a human, finds the best moments, and edits automatically.

## Tool Stack

| Tool | Purpose | Status |
|------|---------|--------|
| **PySceneDetect** | Detect scene/shot boundaries | Installed |
| **MediaPipe** | Face tracking for auto-reframe | Installed |
| **OpenCV** | Frame analysis, cropping | Installed |
| **Hume AI** | Emotion detection (voice + face) | API Key Needed |
| **Twelve Labs** | Video search/understanding | API Key Needed |
| **Whisper** | Transcription | Installed |
| **FFmpeg** | Video processing | Installed |

## Environment Variables Needed

```bash
export HUME_API_KEY="your-hume-api-key"
export TWELVE_LABS_API_KEY="your-twelve-labs-api-key"
```

## The Autonomous Pipeline

```
Input: Raw video file
         ↓
Step 1: PySceneDetect → Find all scene boundaries
         ↓
Step 2: Whisper → Transcribe audio with timestamps
         ↓
Step 3: Hume AI → Analyze emotion peaks (excitement, anger, surprise)
         ↓
Step 4: Twelve Labs → Index video, find key moments by description
         ↓
Step 5: Claude → Score moments, select best hooks (HSP + BEAR)
         ↓
Step 6: FFmpeg → Cut clips at selected timestamps
         ↓
Step 7: MediaPipe → Track faces, calculate crop coordinates
         ↓
Step 8: FFmpeg → Apply 9:16 crop with face tracking
         ↓
Step 9: Remotion → Add subtitles (emotion-styled)
         ↓
Output: Finished clips ready to post
```

## Quick Commands

### Detect Scenes
```bash
scenedetect -i video.mp4 detect-content list-scenes
```

### Find Emotion Peaks (Hume)
```python
from hume import HumeClient
from hume.models.config import ProsodyConfig

client = HumeClient(api_key=os.environ["HUME_API_KEY"])

# Analyze audio for emotion
job = client.expression_measurement.batch.start_inference_job(
    files=["audio.wav"],
    models=[ProsodyConfig()]
)

# Get results - find peaks of excitement, surprise, anger
results = client.expression_measurement.batch.get_job_predictions(job.job_id)
```

### Search Video Content (Twelve Labs)
```python
from twelvelabs import TwelveLabsClient

client = TwelveLabsClient(api_key=os.environ["TWELVE_LABS_API_KEY"])

# Create index and upload video
index = client.index.create(name="my-videos", engines=["marengo2.6"])
task = client.task.create(index_id=index.id, file="video.mp4")

# Search for moments
results = client.search.query(
    index_id=index.id,
    query="when the speaker gets excited and raises voice",
    search_options=["visual", "audio"]
)

# Returns timestamps of matching moments
for clip in results.data:
    print(f"{clip.start} - {clip.end}: {clip.score}")
```

### Auto-Reframe with Face Tracking
```python
import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)

def get_face_center(frame):
    """Get center coordinates of detected face."""
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.detections:
        bbox = results.detections[0].location_data.relative_bounding_box
        center_x = bbox.xmin + bbox.width / 2
        center_y = bbox.ymin + bbox.height / 2
        return center_x, center_y
    return 0.5, 0.5  # Default to center

def calculate_crop(frame_width, frame_height, face_center_x):
    """Calculate 9:16 crop coordinates centered on face."""
    target_ratio = 9 / 16
    crop_width = int(frame_height * target_ratio)

    # Center crop on face
    center_pixel = int(face_center_x * frame_width)
    x_start = max(0, center_pixel - crop_width // 2)
    x_end = min(frame_width, x_start + crop_width)

    # Adjust if we hit edges
    if x_end - x_start < crop_width:
        x_start = max(0, x_end - crop_width)

    return x_start, x_end
```

### Full Autonomous Edit Command
```bash
# Run complete pipeline
python3 ~/.claude/skills/video-intelligence/auto_edit.py \
    --input video.mp4 \
    --output clips/ \
    --target-duration 60 \
    --style vertical
```

## Integration with NRVES Pipeline

This skill enhances the existing NRVES pipeline:

| NRVES Step | Video Intelligence Enhancement |
|------------|-------------------------------|
| N (Narrative) | Twelve Labs finds story moments |
| R (Retention) | Hume finds emotion peaks |
| V (Visual) | MediaPipe tracks faces |
| E (Edit) | Auto-crop, auto-cut |
| S (Style) | Emotion-styled subtitles |

## What Gets Automated

| Before | After |
|--------|-------|
| Watch full video manually | AI indexes and searches |
| Scrub for good moments | Emotion peaks auto-detected |
| Guess viral potential | BEAR score calculated |
| Manual vertical crops | Face tracking auto-reframe |
| Time-based subtitle colors | Emotion-based styling |

## API Costs (Estimates)

| Tool | Free Tier | After Free |
|------|-----------|------------|
| Hume AI | Limited | ~$0.01/min |
| Twelve Labs | 10 hrs/mo | ~$0.05/min |
| PySceneDetect | Free forever | Free |
| MediaPipe | Free forever | Free |

## Setup Checklist

- [x] PySceneDetect installed
- [x] OpenCV installed
- [x] MediaPipe installed
- [ ] Hume AI API key set
- [ ] Twelve Labs API key set
- [ ] Test on sample video

---

*Created: 2026-02-06*
*Layer: Machine*
*Status: Ready (pending API keys)*
