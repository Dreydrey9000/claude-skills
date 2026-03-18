# Viral Patterns & Hidden IP Reference

This document contains the synthesized "Hidden IP" from 20+ hours of expert video editing training and the Viral Editz NRVES system.

## ADVANCED HOOK FORMULAS

| Formula Type | Logic | Example |
| :--- | :--- | :--- |
| **Result First** | Show the end state immediately to prove authority. | "I made $100M using this one spreadsheet." |
| **Contrarian** | Attack a common belief to create friction/curiosity. | "Stop posting reels. They are killing your brand." |
| **Curiosity Gap** | Mention a "secret" or "missing piece" without revealing it. | "There is a hidden button in your settings that..." |
| **Tension/Disaster** | Start at the peak of a problem or failure. | "I almost lost my entire business because of this..." |
| **The "Mechanism"** | Introduce a new, unique way of doing something. | "This AI 'Digital Twin' edits my videos while I sleep." |

## THE CUB FIX MATRIX

| Flag | Trigger | Visual Prescription |
| :--- | :--- | :--- |
| **Confusing** | Industry jargon, complex concepts, acronyms. | **Context Bar**: Semi-transparent overlay with definition. |
| **Unbelievable** | Revenue claims, big stats, transformations. | **Proof Card**: Slide-in screenshot or "Verified" badge. |
| **Boring** | Long explanations, filler words, static shots. | **Pattern Interrupt**: Zoom pulse (1.15x) or B-roll cut. |

## RETENTION "VIBE" RULES

### The 2-Second Rule
Every 2 seconds, the viewer's brain needs a "refresh." This is achieved through:
- **Visual Change**: A cut, a zoom, or a new text element.
- **Information Change**: A new fact, a pivot in the story, or a punchline.
- **Energy Change**: A shift in tone, a sound effect, or a music swell.

### Energy Matching Styles
- **The "Hormozi" Vibe**: High contrast, fast pacing (1.2x), bold yellow captions, frequent zoom pulses, and "Pop" sound effects.
- **The "Abdaal" Vibe**: Minimalist, clean white space, serif fonts, subtle transitions, and ambient background music.
- **The "Cardone" Vibe**: Aggressive, high-energy delivery, large red/white text, and "Urgency" graphics.

## PROGRAMMATIC ANIMATION PATTERNS (Remotion)

- **Zoom Pulse**: `interpolate(frame, [0, 5, 10], [1, 1.15, 1])` - Use for emphasis on key words.
- **Slide-In Proof**: `spring({ frame, fps, config: { damping: 12 } })` - Use for proof cards.
- **Karaoke Highlight**: Map transcript timestamps to text color changes to keep the viewer "reading" along.
