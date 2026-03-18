# REMOTION + CLAUDE CODE: Complete Knowledge Extraction
## From 20 YouTube Transcripts - The Ultimate Reference

---

## WHAT IS REMOTION?

Remotion is a framework that creates videos using code. Every frame of a video is a React component. Claude Code writes the React components → Remotion renders them → You get an MP4.

**Why This Matters:**
- Videos become programmable
- AI can edit videos by editing code
- No manual timeline editing needed
- Version control for videos (git-trackable)
- Infinite variations from templates

**The Core Concept:**
> "What they've effectively done is every frame of a video asset is code. And when every frame is code, we can use programming to create functions, loops, conditionals to automate and scale video production."

---

## INSTALLATION (The Exact Commands)

### Step 1: Create Remotion Project
```bash
# Using npm
npx create-video@latest

# Using bun (faster)
bun create video
```

**During Setup:**
- Select: `blank` template
- Tailwind CSS: `Yes`
- Add agent skills: `Yes` (or add manually)

### Step 2: Install Dependencies
```bash
cd my-video
npm install
# or
bun i
```

### Step 3: Add Claude Code Skill
```bash
npx skills add remotion-dev/skills
# or
bunx skills add remotion-dev/skills
```

**During Skill Setup:**
- Select agent: `Claude Code` (can select multiple)
- Scope: `Global` (recommended - works across projects)
- Link type: `Symlink` (recommended - one source of truth)

### Step 4: Start Development
```bash
npm run dev
# Opens localhost:3000 with Remotion Studio
```

### Step 5: Open Claude Code
```bash
claude
# Or with auto-approve:
claude --dangerously-skip-permissions
```

---

## THE REMOTION STUDIO

When you run `npm run dev`, you get a local video editor at localhost:3000:

**Features:**
- Preview video in real-time
- See all scenes/compositions
- Timeline with frames
- Assets panel on left
- Hot reload (changes update instantly)

**Key Insight:**
> "You won't really be using much of the UI here to be honest. You're just going to prompt for any changes."

---

## SKILLS SYSTEM EXPLAINED

Think of skills like Pokemon TMs or GTA cheat codes:

> "In the same way you can teach Claude other skills like 'Hey, here's your video editing skill, and you're going to be using Remotion to do that.' We teach them the skill and then after Claude learns the skill, it can start doing these things."

**How Skills Work:**
1. Skills are markdown files in `.claude/skills/`
2. They contain best practices and context
3. Claude reads them dynamically when relevant
4. Keeps context clean (only loads what's needed)

**Checking Skills:**
```bash
# In Claude Code
/skills
# Shows: remotion-best-practices (if installed)
```

---

## PROMPTING TECHNIQUES (From The Transcripts)

### Basic Prompts That Work

**Product Demo:**
```
Use remotion to create a short promo video for this course: [URL]
```

**From Website:**
```
Head over to [website URL], extract the brand guidelines, colors, 
typography, grab the logo, and create an explainer video.
```

**Sports/Data:**
```
Create a 20 second video going over the biggest stories in the NBA 
this season.
```

**Landing Page:**
```
Go to this website and fetch the assets, use the same colors (white, 
black text, blue accents) and build a video for a product demo.
```

### Advanced Prompting Patterns

**The Screenshot Technique:**
> "Take a screenshot of your landing page and paste it into Claude Code so it has a reference of the visual aesthetic."

**The Asset Gallery Technique:**
> "If you have lots of images, ask Claude to visualize all assets in one screen on an HTML gallery with the path under each image. Then Claude knows: 'I want to use that asset, that asset' and puts them together."

**The 10 Image Limit Workaround:**
```
I want to visualize all my assets in one screen on an HTML gallery.
Make sure to include the path to each one under the image.
```

**Iterative Editing:**
```
Make the text significantly bigger for all scenes
Use this gradient throughout the video: [paste gradient]
Add an instructor image at the end
```

---

## WORKFLOW PATTERNS

### Pattern 1: Website → Video
1. Give Claude the URL
2. Claude fetches brand colors, images, copy
3. Claude creates Remotion composition
4. Preview in Studio
5. Iterate with prompts
6. Render final MP4

### Pattern 2: Assets → Video
1. Organize assets in `/public` folder
2. Create asset gallery (HTML preview)
3. Take screenshot of gallery
4. Prompt with screenshot + direction
5. Claude composes video from assets

### Pattern 3: Existing React App → Video
1. Open your app's directory
2. Claude can use existing React components
3. "Look at my components and create a promo video"
4. Components render in video (realistic app demos)

### Pattern 4: Multi-Tool Composition
```
Use /remotion best practices
Use the nano banana skill for image generation
Use /sfx for sound effects with 11Labs
Align the beat of the SFX to the video transitions
```

---

## TOOL INTEGRATIONS

### 11Labs (Voice/SFX)
```bash
# CLI tool for sound effects
# Generates audio from text prompts
# Can align SFX to video beats
```

### Nano Banana (Image Generation)
```bash
# Generate images from text
# Use as backgrounds/assets in videos
# Can generate styled images matching brand
```

### Whisper (Transcription)
```bash
# Transcribe video audio
# Word-level timestamps
# Use for auto-captions in Remotion
```

### Aureanic/Orphonic (Audio Enhancement)
```bash
# Improve audio quality
# Cleanup background noise
# Enhance voice clarity
```

### HeyGen (AI Avatars)
```bash
# Generate AI avatar videos
# Combine with Remotion overlays
# Create presenter-style content
```

---

## CAPTIONING WORKFLOW

### Automated Caption Pipeline:
1. **Analyze & Transcribe** - Whisper with word-level timestamps
2. **Parse Transcript** - Detect ums, mistakes, filler
3. **Trim Video** - Cut mistakes automatically
4. **Audio Process** - Aureanic enhancement
5. **Remotion Caption Engine** - Add styled captions

### Caption Best Practices:
> "The biggest mistake people make with this stuff - people don't pay enough attention to detail on the fonts and the size of the fonts, the visual hierarchy, the white space, how it flows."

**Typography that works:**
- Google Fonts (web-safe)
- Proper spacing
- Text shadow for readability
- Consistent styling logic

---

## RENDERING

### Preview vs Render:
```bash
# Preview (hot reload)
npm run dev

# Render to MP4
npx remotion render src/index.ts MyVideo out/video.mp4
```

### Render Settings:
- Default: 30 FPS
- Can configure resolution, codec
- Rendering is CPU/GPU intensive
- Consider VPS for render farms

---

## PRO TIPS FROM TRANSCRIPTS

### 1. Visual References Are Everything
> "AI and Claude Code has eyes. You guys really need to be taking advantage of the eyes it has because it's really strong."

### 2. Screenshot Your Landing Page
Feed Claude screenshots of your existing brand materials.

### 3. Asset Gallery for Large Projects
Don't make Claude scan 100 files. Create an HTML gallery preview.

### 4. Multiple Claude Instances
> "We can have multiple of these different instances running for us. One can edit automatically while another fetches information."

### 5. Iterative Refinement
Don't try to get it perfect in one prompt. Iterate:
```
- "I don't like this, use nano banana for the background"
- "Make it faster, more hype"
- "Add a slot machine effect instead of slideshow"
```

### 6. MCP Servers for Extended Capabilities
Access Gmail, Notion, Zapier from Claude Code via MCP.

### 7. Skip Permissions for Speed
```bash
claude --dangerously-skip-permissions
```

### 8. Use VS Code Extension
Install Claude extension in VS Code. Double-click to open Claude interface directly.

---

## COMMON MISTAKES TO AVOID

1. **Not providing visual references** - Claude can SEE. Show it what you want.

2. **One giant prompt** - Break it into scenes, iterate.

3. **Ignoring the skill** - Always invoke `/remotion` to load best practices.

4. **Too many assets** - Create gallery, use screenshot technique.

5. **Manual editing in Studio** - Just prompt for changes instead.

6. **Not using brand guidelines** - Extract from website first.

---

## VIDEO TYPES THAT WORK

From the transcripts, these work well:

- **Product demos** - Show SaaS features with animations
- **Explainer videos** - Website → video conversion
- **Social media ads** - Quick promotional content
- **Motion graphics** - Title cards, lower thirds, transitions
- **Data visualizations** - Dynamic dashboards, charts
- **Logo reveals** - Animated intros/outros
- **Promo videos** - Course/product marketing

---

## REMOTION CODE STRUCTURE

```
my-video/
├── src/
│   ├── index.ts          # Entry point
│   ├── Root.tsx          # Main composition
│   └── Composition.tsx   # Your video component
├── public/               # Assets (images, fonts)
├── .claude/
│   └── skills/
│       └── remotion-best-practices/
├── package.json
└── remotion.config.ts
```

### Basic Component Pattern:
```tsx
import { useCurrentFrame, interpolate } from 'remotion';

export const MyScene = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  
  return (
    <div style={{ opacity }}>
      Your content here
    </div>
  );
};
```

---

## FRAME MATH

- 30 FPS standard
- Frame 0 = 0:00
- Frame 30 = 0:01
- Frame 900 = 0:30

```tsx
// 5 second video at 30fps = 150 frames
<Composition
  durationInFrames={150}
  fps={30}
  width={1080}
  height={1920}
/>
```

---

## QUOTES FROM CREATORS

> "Claude literally made this in under five prompts."

> "This was not possible literally a week ago."

> "The barrier of entry for doing anything has drastically gotten lower and lower."

> "My computer is now Claude's computer."

> "People are generating entire videos with voiceovers, motion graphics and product demos all from a single text prompt."

---

## MOBILE ACCESS (VPS Setup)

From NetworkChuck's video:
1. Set up VPS (Hostinger recommended)
2. Install Claude Code on VPS
3. Use terminal app on phone to SSH
4. Claude Code from anywhere

```bash
# Forever terminal setup
# Access Claude Code from phone
```

---

## THE BUSINESS OPPORTUNITY

> "I found a lot of the examples, they just don't look good. If it's not something you'd actually use, I don't think there's any point talking about it."

**Focus on quality outputs:**
- Real brand guidelines
- Professional typography
- Proper visual hierarchy
- Actually usable content

**Market validation:**
- Submagic: $1M ARR in 3 months (video editing)
- AI video tools: $5-6M ARR
- Crayo: $6M ARR

---

## NEXT STEPS

1. Install Remotion + Claude Code skill
2. Start with simple prompt (promo for your website)
3. Take screenshots of your brand materials
4. Iterate with specific feedback
5. Add tools (11Labs, Nano Banana) as needed
6. Build reusable templates
7. Scale to batch generation

---

*Extracted from 20 YouTube transcripts covering Claude Code + Remotion workflows*
*Total lines processed: ~11,000*
