---
name: niche-dashboard
description: "Build a niche intelligence dashboard for any industry/profession. Real-time RSS feeds, AI summaries, optional map, variant system. Stolen from World Monitor architecture. Triggers: 'niche dashboard', 'intelligence dashboard', 'build a monitor', 'industry dashboard', 'build me a dashboard for [industry]', 'news dashboard', 'sector monitor'"
---

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.
**Quality Gates:** Follow `~/.claude/skills/_shared/quality-gates.md` for ALL quality checks.

# Niche Dashboard Generator

Build a real-time intelligence dashboard for ANY industry or profession. One codebase pattern, infinite niches.

**Stolen from:** World Monitor (worldmonitor.app) — 170+ feeds, dual map engine, AI briefs, 4 variants from one codebase. We extracted the 5 core patterns and simplified them for niche builds.

**Reference architecture:** `./reference-architecture/ (see World Monitor repo)`

---

## The 5 Patterns (Architecture Blueprint)

```
User opens dashboard
       |
  [1. FEED ENGINE] -----> RSS feeds fetched via proxy, parsed, cached
       |
  [2. PANEL SYSTEM] ----> Categorized into panels (regions, topics, signals)
       |
  [3. AI LAYER] ---------> Headlines summarized (Ollama local / Groq cloud / browser T5 fallback)
       |
  [4. MAP ENGINE] -------> Optional: data points plotted on map (deck.gl or simple Leaflet)
       |
  [5. VARIANT SYSTEM] ---> One codebase serves multiple niches via config swap
```

---

## Pattern 4: Map Engine (Optional)

**What it does:** Plots data points on a map for spatial context. World Monitor uses globe.gl (3D) + deck.gl (flat). For niche dashboards, Leaflet or Maplibre is simpler.

**When to include:** Only if your niche has geographic data — real estate (property locations), solar (installation sites), logistics (routes), etc.

**Simplified approach:**
```typescript
// Use Leaflet (lightweight) instead of globe.gl (heavy)
import L from 'leaflet';

const map = L.map('map').setView([39.8, -98.5], 4); // US center
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Plot data points
dataPoints.forEach(point => {
  L.marker([point.lat, point.lng])
    .bindPopup(`<b>${point.title}</b><br>${point.description}`)
    .addTo(map);
});
```

**Key decisions:**
- Leaflet (60KB) vs deck.gl (500KB+) — start with Leaflet, upgrade if needed
- Map is optional — many niche dashboards work great without it
- Toggle layers on/off just like panels

---

## Pattern 5: Variant System (One Codebase, Multiple Niches)

**What it does:** Serves different dashboard configurations from the same codebase. World Monitor does World/Tech/Finance/Happy from one repo.

**How World Monitor does it:**
- `VITE_VARIANT` env var controls which config loads at build time
- `src/config/variant.ts` reads from env, hostname, or localStorage
- Each variant defines its own feeds, panels, and map layers
- Hostname-based routing: `tech.yoursite.com` → tech variant

**How to build yours:**

```typescript
// config/variant.ts
export const VARIANT = (() => {
  const h = location.hostname;
  if (h.startsWith('solar.')) return 'solar';
  if (h.startsWith('realestate.')) return 'realestate';
  return import.meta.env.VITE_VARIANT || 'solar';
})();

// config/feeds.ts
import { VARIANT } from './variant';
import { SOLAR_FEEDS } from './variants/solar';
import { REALESTATE_FEEDS } from './variants/realestate';

export const FEEDS = VARIANT === 'solar' ? SOLAR_FEEDS
  : VARIANT === 'realestate' ? REALESTATE_FEEDS
  : SOLAR_FEEDS;
```

---

## Interactive Decision Points

### 1. What niche?
Ask the user:
- "What industry/profession is this dashboard for?"
- Use their answer to research and curate 15-25 RSS feeds (use Firecrawl/Brave/Perplexity to find industry RSS feeds)
- Organize feeds into 4-8 panels

### 2. How complex?
Ask the user:
- **"Quick monitor (MVP)"** — RSS feeds + panels + basic styling. No AI, no map. Ships in 1-2 hours.
- **"Smart monitor"** — RSS + panels + AI briefs (Ollama/Claude). Ships in 3-4 hours.
- **"Full intelligence dashboard"** — RSS + panels + AI + map + variant system. Ships in 6-8 hours.

### 3. Deployment?
- **Vercel** (recommended) — free tier handles RSS proxy + static frontend. Zero config.
- **Cloudflare Workers** — if already on Cloudflare (the user's setup).
- **Self-hosted** — Docker on any VPS.

---

## Stack (Simplified from World Monitor)

| World Monitor Uses | We Use Instead | Why |
|---|---|---|
| Preact | React or Preact | Same patterns, React has more ecosystem |
| Vite | Vite | Same — fast, simple |
| globe.gl + deck.gl + maplibre | Leaflet (if map needed) | 10x simpler, 10x lighter |
| Convex | None (or Supabase if real-time needed) | Convex is overkill for niche dashboards |
| Upstash Redis | Vercel KV or just CDN caching | Simpler, free tier sufficient |
| 170+ feeds | 15-25 curated feeds | Niche = focused, not exhaustive |
| 22 proto services | Simple REST API routes | No proto generation needed |
| Tauri desktop app | PWA only | Desktop app is overkill for v1 |

---

## File Structure (What We Generate)

```
niche-dashboard/
  src/
    config/
      feeds.ts          # RSS feed definitions
      panels.ts         # Panel layout config
      variant.ts        # Variant detection
      variants/         # Per-niche feed/panel configs
    components/
      Dashboard.tsx     # Main grid layout
      Panel.tsx         # Single panel component
      FeedCard.tsx      # Individual news item card
      AiBrief.tsx       # AI summary component
      Map.tsx           # Optional map component
    services/
      rss.ts            # Feed fetcher + parser + cache
      summarize.ts      # AI summary with fallback chain
      cache.ts          # localStorage/IndexedDB cache
    App.tsx
    main.tsx
  api/
    rss-proxy.ts        # Serverless RSS proxy
    summarize.ts        # AI summary endpoint
  index.html
  package.json
  vercel.json
  README.md
  CHANGELOG.md
```

---

## Gate Protocol
- **Pre-flight:** Confirm niche, complexity level, and deployment target. Research RSS feeds for the niche.
- **Mid-flight:** Feeds must load. Panels must render. Proxy must not leak SSRF.
- **Post-flight:** CUB test. README with setup instructions. CHANGELOG updated. Deploys independently.

## Sources
- Architecture extracted from World Monitor (github.com/koala73/worldmonitor), AGPL-3.0
- Patterns simplified for niche use — no code copied, only architectural patterns referenced


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-13]: Context Diet — split 342 lines into routing card (186 lines) + references/full-details.md (174 lines). Zero content deleted. By skill-diet.py.
- [2026-03-06]: Created. 5 patterns extracted from World Monitor. Interactive decision points defined. Simplified stack chosen. By the user + Claude.
