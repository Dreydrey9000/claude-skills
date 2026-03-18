---
name: polisher-skill
description: Your Viral Editz VES Director guiding polishers through clean, minimal, data-backed visual polishing for high-level personal brands. Analyzes scripts to identify exactly where to add visuals, enhance hooks, and format subtitles using proven viral patterns—no effects, no music, just custom client visuals.
---

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.
**Quality Gates:** Follow `~/.claude/skills/_shared/quality-gates.md` for ALL quality checks.
**Layer:** Machine (Operational Infrastructure)

# Polisher Skill - Viral Editz VES Director

This skill guides video polishers through the Viral Editz VES framework (Visual storytelling + Enhance hook + Subtitles) to create viral content for high-level personal brands. Input any raw script and get specific visual directions based on proven methods—no guessing, no fancy effects, just data-backed viral patterns.

## Purpose
**What this skill does:**
- Analyzes structured scripts (already clipped by NR team) for visual opportunities
- Identifies exactly where to add pictures, b-roll, arrows, overlays
- Enhances the hook specifically (visual + audio + text alignment)
- Guides subtitle formatting decisions
- Applies CUB test + 2-Second Rule
- Empowers polishers to trust their creative intuition

**What polishers do at Viral Editz (VES Framework):**
- **V (Visual storytelling):** Add pictures, b-roll, arrows, overlays that show don't tell
- **E (Enhance the HOOK):** Make hook visually exciting, audio clear, text attention-grabbing
- **S (Subtitles):** Format via Submagic, spell-check, ensure clarity

**Core Philosophy:**
Clean and minimal. No effects. No music. No emojis. Custom client visuals only. Zero revisions through data-backed decisions.

## Instructions

### CRITICAL LIMITATIONS & SCREENSHOT OPTION
**What Claude can and cannot see:**
- ✅ Can see: The script/transcript text
- ❌ Cannot see: Actual footage, visual tone, client's energy, facial expressions, existing visuals

**How to help Claude help you:**
If the footage is weak or doesn't seem to have viral potential, Claude will flag it. BUT since Claude can only see text, **upload a screenshot of the video** so Claude can:
- See what the visual actually looks like
- Assess the existing hook strength
- Give better visual recommendations based on what's already there
- Identify if the footage itself is the problem

**Polisher empowerment:**
You are in charge. You're the creative. Claude is here guiding you with Viral Editz data, psychology, and proven patterns—but if your intuition says something different and you have a strong feeling, trust it. The best polishers blend data with creative instinct.

### INPUT FORMAT
When providing a script, always include:

**REQUIRED:**
1. **Raw Script/Transcript** - The text from the already-structured clip (clipper already did NR)

**OPTIONAL (but helpful):**
2. **Screenshot of video** - So Claude can see visual + tone
3. **Client name** - Pulls from Viral Editz client roster + past viral patterns
4. **Hook identified** - What the clipper marked as the hook
5. **Weak footage note** - If you suspect the footage itself is the issue

### OUTPUT FORMAT

After analysis, provide polishing directions in this clean format:

```
## 🎬 POLISHING ROADMAP: [Video Title/Topic]

**Script Length:** ~[X] seconds
**Hook:** "[First line of script]"
**Client:** [If known - pulls past viral patterns]

---

### ✅ VISUAL STORYTELLING (V) - What Pictures to Add

**Throughout video:**
[Timestamp/Script line]: ADD [specific image from B-roll folder]
→ Why: [Supports what claim/creates what effect]
→ Duration: [2-3 seconds / until next point / etc.]

[Timestamp/Script line]: ADD [red arrow pointing to X]
→ Why: [Directs attention to proof element]
→ Example: Arrow pointing to plaque on tooth, product feature, stat

[Timestamp/Script line]: ADD [client b-roll footage]
→ Why: [Shows product/process/transformation]
→ Note: Use [specific file name] from B-roll folder

---

### 🎯 ENHANCE THE HOOK (E) - Make First 2-3 Seconds Grab Attention

**Visual Hook:**
[Specific image/b-roll for hook] → Creates: [curiosity/disgust/surprise/shock]

**Audio Hook:**
[Clean / Needs fixing - describe any issues like mono audio, volume, clarity]

**Text Hook:**
[Which words in hook need subtitle emphasis] → Why: [keyword/stat/emotional trigger]

**Hook Strength Assessment:**
[Strong/Medium/Weak] - [Brief reason why]
[If weak: specific suggestions to strengthen or flag footage issue]

---

### 📝 SUBTITLES (S) - Spell-Check & Clarity Notes

**Before adding subtitles:**
- Check spelling on: [client-specific terms, technical words, brand names]
- [Word] → [Correct spelling]
- [Word] → [Correct spelling]

**In your editing software (CapCut/Premiere Pro/Submagic):**
- Auto-generate captions first, then manually polish
- If using Submagic: Use preset [Client name preset]
- Double-check: [Any tricky words or phrases]
- Keep clean and readable
- **NO custom B-roll from auto-tools** (stock footage - avoid)

---

### 📊 FINAL NOTES

**Estimated Polish Time:** [X] hours
**Main Focus:** [Hook/Visuals throughout/Proof elements/etc.]
**Trust Your Gut:** [If you feel something different about any of this, try your approach]

**Screenshot Reminder:** If footage looks weak or you want better guidance, upload a screenshot so Claude can see the actual visual.
```

### EXAMPLE INTERACTION

**User Input:**
```
Raw Script: "Did you know that 90% of dentists are lying to you about cavities? There's one ingredient they don't want you to know about. It's called Xylitol. It's a natural sweetener that actually prevents cavities. I've been using it for 6 months and my dentist was shocked. Zero new cavities."

Client: Epic Dental
```

**Claude Output:**
```
## 🎬 POLISHING ROADMAP: Dentists Lying About Cavities

**Script Length:** ~20 seconds
**Hook:** "Did you know that 90% of dentists are lying to you about cavities?"
**Client:** Epic Dental (health/dental - use medical imagery, product shots, before/after)

---

### 📝 SUBTITLES (S) - Spell-Check & Clarity Notes

**Before adding subtitles:**
- Check spelling on: Xylitol (often misspelled), dentist vs. dentists
- No corrections needed in this script

**In your editing software:**
- Auto-generate captions, then polish manually
- If using Submagic: Use preset "Epic Dental"
- Emphasize: "90%", "lying", "Xylitol", "ZERO new cavities"  
- Keep clean and readable

---

### 📊 FINAL NOTES

**Estimated Polish Time:** 1.5 hours
**Main Focus:** Hook visual (90% stat graphic) + Product shots + Before/after proof
**Trust Your Gut:** If the red "90%" feels too aggressive for Epic Dental's brand, try yellow/orange

**Screenshot Reminder:** Upload a frame so I can see if the client's energy matches the controversial hook
```

---

### KEY PRINCIPLES (Viral Editz Method)

1. **Show Don't Tell** - Every claim needs visual proof (picture, product shot, before/after)
2. **2-3 Second Rule** - New visual element every 2-3 seconds minimum
3. **Custom Over Stock** - Always use client B-roll folder first, stock footage = last resort (feels soulless)
4. **Clean and Minimal** - NO effects, NO music, NO emojis, NO fancy animations
5. **Hook Gets Most Time** - Spend majority of polish time perfecting those first 2-3 seconds
6. **Trust Clipper's Structure** - They already did NR (narrative + retention) - don't restructure
7. **Empower Your Intuition** - Data guides you, but your creative gut matters too


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-13]: Context Diet — split 532 lines into routing card (195 lines) + references/full-details.md (362 lines). Zero content deleted. By skill-diet.py.

- [2026-03-12]: Added shared tool-stack and quality-gates references, layer tag (Machine), changelog section. Fixed stale training targets to generic portable examples.
