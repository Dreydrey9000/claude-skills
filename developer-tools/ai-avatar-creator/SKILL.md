---
name: ai-avatar-creator
description: Build photorealistic AI avatars for content creation using a proven 6-step workflow. Use this skill when users want to create consistent AI characters/avatars for social media content, UGC videos, digital spokespersons, or talking head videos. Triggers include requests to create AI avatars, build consistent AI characters, generate talking AI videos, make virtual influencers, or produce AI-generated spokesperson content. Covers the complete pipeline from base image generation through lip-synced video output.
---

# AI Avatar Creator

Build photorealistic, consistent AI avatars that can speak in videos. This skill guides users through a 6-step workflow using specific tools for each phase.

## Tool Stack

| Step | Tool Options | Purpose |
|------|------|---------|
| 1 | **Higgsfield** (recommended), Enhancor KORA, or any image generator | Base image creation |
| 2 | Enhancor NANO-BANANA or Higgsfield | Character variations |
| 3 | Higgsfield Soul ID | Character training |
| 4 | Higgsfield (Kling 2.1 Master) | Video generation |
| 5 | ElevenLabs | Voice synthesis |
| 6 | DreamFace | Lip sync |

## Starting Point: Gather Requirements

Before building, ask these 5 questions:

1. **Role**: What does this avatar do? (coach, spokesperson, influencer)
2. **Demographics**: Age, gender, ethnicity, aesthetic style?
3. **Personality**: How should they speak/behave? (casual, professional, energetic)
4. **Content formats**: Reels, podcasts, GRWM, talking head?
5. **Reference**: Any visual inspiration or reference images?

If user provides a **reference image**, analyze it to extract: age estimate, gender, ethnicity markers, hair style/color, skin tone, distinguishing features, and aesthetic style. Use these as the foundation.

---

## Workflow Summary

```
Step 1 → Create ONE perfect base image (KORA/Higgsfield)
Step 2 → Generate 20+ variations (NANO-BANANA)
Step 3 → Train character model (Soul ID)
Step 4 → Animate image to video (Kling 2.1)
Step 5 → Generate voice audio (ElevenLabs)
Step 6 → Lip sync video + audio (DreamFace)
```

**Total Time**: ~2 hours for first avatar

---

## Quality Checkpoints

Use these before proceeding to next step:

### After Step 1 (Base Image)
- [ ] Frontal view, direct eye contact
- [ ] Natural imperfections visible
- [ ] Even, natural lighting
- [ ] Simple background
- [ ] High resolution

### After Step 2 (Variations)
- [ ] 20+ usable images
- [ ] All match original character
- [ ] Mix of expressions, angles, settings
- [ ] No character drift

### After Step 3 (Training)
- [ ] Test generation produces consistent character
- [ ] Features match across different prompts
- [ ] Quality comparable to training images

### After Step 4 (Video)
- [ ] Smooth, natural movement
- [ ] No distortion or artifacts
- [ ] Character looks correct throughout
- [ ] Mouth movement visible and natural

### After Step 5 (Voice)
- [ ] Natural pacing and rhythm
- [ ] Matches avatar personality
- [ ] Clear pronunciation
- [ ] No robotic artifacts

### After Step 6 (Lip Sync)
- [ ] Lips match audio throughout
- [ ] No sync drift
- [ ] Professional quality output

---

## Troubleshooting Guide

### Step 5: Voice Creation Issues

**Voice sounds robotic or monotone**
→ Lower stability setting to 40-50%. Add proper punctuation for natural pauses. Choose different base voice.

**Inconsistent pronunciation of words**
→ Use phonetic spelling for difficult words. Add commas for natural speech rhythm. Test with shorter sentences.

**Voice doesn't match avatar age/style**
→ Test multiple voice options with same script. Consider target audience demographics. Match energy level to avatar.

**Wrong emotional tone in delivery**
→ Adjust script punctuation. Try different stability/clarity settings. Choose voice with appropriate baseline emotion.

**Voice sounds too fast or too slow**
→ Adjust speed slider (0.01 increments). Add periods and commas to control pacing. Use shorter sentences for faster delivery.

---

### General Workflow Issues

**Workflow taking too long**
→ Batch similar operations. Generate multiple variations in one session. Keep quality high in early steps to reduce re-work.

**Running out of credits**
→ Prioritize quality over quantity. Reject bad outputs early. Use undistorted portions of videos when possible.

**Character looks different across steps**
→ This is cumulative drift. Go back to earliest problematic step and redo. Maintain strict quality standards at each checkpoint.

**Final video doesn't look professional**
→ Check each step's quality markers. Usually the issue traces back to base image quality or training data consistency.

---

### Good Base Image
✅ Frontal view, direct eye contact
✅ Visible imperfections (pores, freckles, asymmetry)
✅ Natural daylight, even lighting
✅ Simple background
✅ High resolution

### Bad Base Image
❌ Extreme angles
❌ Sunglasses or obscured face
❌ Harsh or uneven lighting
❌ Busy/distracting background
❌ Overly perfect "AI look"

### Good Variation
✅ Features match original exactly
✅ Consistent skin tone and hair
✅ Clear, visible face
✅ Professional/appropriate for use case

### Bad Variation
❌ Different hair color/style
❌ Inconsistent skin tone
❌ Different age appearance
❌ Face obscured or too far away

---

## HeyGen API — Talking Photo Pipeline (Proven 2026-02-03)

Shortcut pipeline when you already have a base image + audio and just need the talking head video. Skips Steps 2-5.

### API Endpoints

| Step | Endpoint | Method |
|------|----------|--------|
| Upload as Talking Photo | `https://upload.heygen.com/v1/talking_photo` | POST (raw binary, Content-Type: image/jpeg) |
| Upload Audio | `https://upload.heygen.com/v1/asset` | POST (raw binary, Content-Type: audio/mpeg) |
| Generate Video | `https://api.heygen.com/v2/video/generate` | POST (JSON) |
| Check Status | `https://api.heygen.com/v1/video_status.get?video_id=X` | GET |

### Key: Upload Image as TALKING PHOTO, Not Regular Asset

Regular asset upload (`/v1/asset`) returns an `id` that does NOT work as a `talking_photo_id`. You MUST use the `/v1/talking_photo` endpoint which returns a proper `talking_photo_id`.

### Watermark Removal

- **API Free tier:** Watermark on all videos. No parameter to remove it.
- **API Pro ($99/mo):** No watermark with `"test": false`
- **Web UI workaround:** If you have a paid platform plan (Creator+), upload image + audio manually in HeyGen web UI and toggle watermark off before generating.

### HeyGen API Key

`sk_V2_hgu_ktgAobLdFV4_R7sCHf1JE0DJYsG8UUp6YmPtHVs56nsC`

### Processing Time

~4 minutes for a 59-second talking photo video (polled every 10s, completed at ~240s).


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
