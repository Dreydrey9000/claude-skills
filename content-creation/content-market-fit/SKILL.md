---
name: content-market-fit
description: >
  Content Market Fit 2026 — Luis Carrillo's framework for extracting creator/client DNA
  through a structured interview process. Three corners: YOU (Worldview), AUDIENCE (Bridge),
  OFFER (Invitation). Use when onboarding a new client, profiling a creator, building a
  clone, or auditing content strategy. Triggers: "content market fit", "onboard client",
  "profile this creator", "extract worldview", "audience bridge", "who is their audience",
  "clone this person", "audit their content", new client intake, creator intelligence extraction.
---

# Content Market Fit 2026

## What This Is

A structured extraction framework for mapping ANY creator or client's complete DNA.
Three corners of a triangle: **YOU** (Worldview) → **AUDIENCE** (Bridge) → **OFFER** (Invitation).

Every creator, client, and clone needs this completed before content strategy begins.

## When To Use

- New client onboarding (Viral Editz)
- Creator intelligence extraction (scraping someone's account)
- Clone preparation (before building an AI clone of anyone)
- Content strategy audit ("why isn't their content working?")
- Competitor analysis (profiling someone's CMF triangle)

## Corner 1: YOU — The Worldview

This is the creator's world. Why someone follows them. Why they're worthy of attention.

## Corner 2: AUDIENCE — The Bridge

Where the audience is in their journey. The gap between finding the creator and buying.

## Corner 3: OFFER — The Invitation

The products, services, content, and value exchange.

## Modes of Operation

### Mode 1: Interview (Interactive)

Use when the creator/client is available to answer questions.

**Process:**
1. Start with Corner 1 (YOU) — ask worldview questions conversationally
2. Move to Corner 2 (AUDIENCE) — explore who they attract and why
3. Finish with Corner 3 (OFFER) — map their products and content strategy
4. Cross-reference: Does the triangle align? (Worldview attracts right audience for this offer?)
5. Identify gaps — what's missing or misaligned

**Interview Questions (ask in order):**

#### YOU Questions
1. Tell me your story. How did you get here?
2. What's the biggest obstacle you've overcome in your career?
3. What do you stand for that most people in your space don't?
4. If your brand was a movie, what would the tagline be?
5. What are 3 stories you keep telling over and over?
6. What pisses you off about your industry?
7. What's your daily life actually look like?
8. How do people describe you when you're not in the room?
9. What's your unfair advantage?
10. What transformation have you personally been through?

#### AUDIENCE Questions
11. Who is your dream client/follower? Describe them specifically.
12. What problem do they have that they can't articulate?
13. What have they already tried that didn't work?
14. What keeps them up at 2 AM?
15. What would they pay anything for if it actually worked?
16. What's the gap between where they are and where they want to be?
17. What belief do they need to change before they can succeed?
18. How do they talk about their problems? (Their exact words)
19. Who else do they follow? Who are you compared to in their mind?
20. What makes them finally take action?

#### OFFER Questions
21. What do you sell? Walk me through every product/service.
22. What do you give away for free?
23. What content format works best for you?
24. What's your best-performing content ever? Why do you think it worked?
25. How do people go from watching your content to buying?
26. What objection do you hear most before someone buys?
27. What's the transformation your product/service delivers?
28. If you could only sell one thing, what would it be?

### Mode 2: Scrape (Passive Extraction)

Use when profiling a creator from their public content (no interview available).

**Process:**
1. Scrape their Instagram (Apify) — all posts, engagement, captions
2. Download top 20-30 videos (yt-dlp)
3. Run AI Cookbook pipeline on each (frames + transcription + visual reading)
4. Run Hume + Twelve Labs for emotion/scene analysis
5. Extract Corner 1 from their content patterns (what stories they tell, values they express)
6. Extract Corner 2 from their comments + audience engagement patterns
7. Extract Corner 3 from their CTAs, links, products mentioned
8. Compile full CMF profile

### Mode 3: Audit (Existing Client)

Use to evaluate why content isn't performing.

**Process:**
1. Pull existing CMF profile from Notion (if exists)
2. Analyze recent content performance
3. Check triangle alignment: Does worldview → attract right audience → for this offer?
4. Identify the weak corner
5. Prescribe fixes

---

## Client Comparison Engine

Every client gets 2-5 comparable creators/clients mapped:

### What Comparisons Unlock

- "Here are topics that work for founders like you (husband-wife, family business)"
- "Creators with your personality type get the most views on [format]"
- "Your comparable @competitor gets 100K+ views when they post about [topic]"
- "The editing style that works for your niche is [jump cuts / smooth / podcast]"

---

## Notion Routing

## Output Format

After completing a CMF extraction, deliver:

```
## Content Market Fit Profile: [Name]
**Date:** [Date]
**Mode:** Interview / Scrape / Audit
**Completeness:** [X/28 questions answered]

### Triangle Summary (1 paragraph)
[How the three corners connect for this person]

### Corner 1: YOU (Worldview)
[Full extraction]

### Corner 2: AUDIENCE (Bridge)
[Full extraction]

### Corner 3: OFFER (Invitation)
[Full extraction]

### Triangle Alignment Score: [1-10]
[Where it's strong, where it breaks]

### Comparable Creators: [2-5 names with reasoning]

### Content Prescription
- Top 3 topics to post about NOW
- Format recommendation
- Hook style that matches their worldview
- Editing style recommendation

## Video Script Integration (MANDATORY)

Every video script produced for any client MUST include:

```
### Image Generation Prompt
[Nano Banana Pro / Gemini API prompt to create a thumbnail or visual for this video]

### Video Generation Prompt
[Higgsfield / Kling prompt to animate a scene from this video]
```

This enables the clone era — any video can be recreated for any character.

---


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-13]: Context Diet — split 356 lines into routing card (190 lines) + references/full-details.md (194 lines). Zero content deleted. By skill-diet.py.

- 2026-02-06: Created. Source: Luis Carrillo brain dump session. Formalized from existing intuitive framework into structured skill with interview process, scrape mode, audit mode. Existing Notion databases confirmed (4 per-client CMF DBs, 2 framework pages). Creator Intelligence and Client Intelligence systems designed to use this as their extraction template.
