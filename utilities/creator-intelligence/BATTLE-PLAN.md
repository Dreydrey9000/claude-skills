# Viral Editz Brain Intelligence — Battle Plan v2.0

## The Vision (In Drey's Words)

"We're playing god at this level. Viral god. Because we can with data just know 100% with certainty this is going to work. We have the playbook. We have the examples. We have the source. We have even recommendations on tonality."

"Claude is modern-day Jarvis from Iron Man. You just show up, you have your documents, your info with bullet points and titles and what you need to do. It's an unfair advantage."

**In One Line:** Track what's working across every client, every platform, every week — then feed those winning patterns into content generation for Drey, Ryan, Claudia, their clones, and every future client. Data in. Viral content out. Rinse. Repeat. Dominate.

---

## The Unfair Advantage Levels

```
LEVEL 5: Auto-generate scripts in each creator's voice using proven patterns (NOBODY does this)
    ↑
LEVEL 4: Cross-reference across clients and niches (almost nobody)
    ↑
LEVEL 3: Extract hooks and frameworks (few do this)
    ↑
LEVEL 2: Track what goes viral (some agencies do this)
    ↑
LEVEL 1: Have client data (everyone has this)

Viral Editz operates at Level 5.
```

---

## The System: 5 Layers

```
Layer 5: EXECUTION (Content output for every client + clones)
    ↑
Layer 4: WEEKLY WINS (100K+ videos tracked, patterns surfaced)
    ↑
Layer 3: INDUSTRY INTELLIGENCE (Culture, trends, competitor tracking)
    ↑
Layer 2: CLIENT INTELLIGENCE (Every client fully profiled + compared)
    ↑
Layer 1: DATA COLLECTION (Scrape, track, measure everything)
```

---

## Layer 1: DATA COLLECTION

### What We Scrape

| Platform | Data | Tool | Frequency | Priority |
|----------|------|------|-----------|----------|
| **Instagram** | All posts, reels, carousels, stories, engagement | Apify | Weekly per client | 1 (Primary) |
| **YouTube** | Shorts + long-form, views, watch time, CTR, subs | YouTube Data API v3 / Apify | Daily pull, weekly rollup | 2 |
| **TikTok** | All videos, views, likes, shares, comments | TikTok Research API / Apify | Daily pull, weekly rollup | 3 |
| **Facebook** | Posts, reels if available | Apify | Monthly (when available) | 4 |
| **X/Twitter** | Posts, engagement, viral threads | X API v2 | Weekly (low priority, future) | 5 (Not current) |
| **LinkedIn** | Posts, articles, engagement | Apify | Weekly (low priority, future) | 6 (Not current) |
| **Social Blade** | Historical follower growth, milestones | Social Blade API / scrape | Monthly per client | Supporting |

**Priority order: Instagram > YouTube > TikTok > Facebook > X > LinkedIn.**
X and LinkedIn are not current services but are in-demand — future expansion.

### What We Track Per Post

| Field | Purpose |
|-------|---------|
| Post URL | Source link |
| Platform | IG / TikTok / YT / FB / LinkedIn |
| Post type | Reel / Carousel / Image / Short / Long-form / Story |
| Posted date | Timeline tracking |
| Views | Performance |
| Likes | Engagement |
| Comments | Engagement depth |
| Shares / Saves | Viral potential |
| Engagement rate | Normalized performance (likes + comments + saves + shares / views) |
| Caption / Hook | First line (the hook) |
| Topic category | What it's about |
| Video format | Solo / Podcast / Street / Greenscreen / B-roll / Two people / Carousel |
| Duration | Length analysis |
| Filmed by us? | Checkbox — did Viral Editz film this? |
| Edited by us? | Checkbox — did Viral Editz edit this? |

### Growth Tracking (Social Blade Integration)

Per client, per platform:
- Follower count at start of partnership
- Follower count at end of partnership (or current)
- Monthly follower growth rate
- Pivotal growth moments (spikes) — correlate with specific videos/events
- Before/after delta: "Gained X followers during our partnership"

### The Weekly Scan (Automated)

Every Monday:
1. Pull ALL posts from ALL client accounts for last 7 days
2. Flag anything with 100K+ views
3. Extract from each flagged post:
   - Exact hook (first line / first 3 seconds)
   - Topic category
   - Format (talking head, green screen, B-roll, carousel, podcast clip, etc.)
   - Duration
   - Engagement rate
   - Whether it's an outlier vs. their average
4. Push winning posts into the Weekly Wins database
5. Extract hooks into Hook Library
6. Generate weekly intelligence report

---

## Layer 2: CLIENT INTELLIGENCE

### Client Account Registry (Notion: Client Profiles - Viral Editz Roster)

Every Viral Editz client gets an entry with:

| Field | Type | Purpose |
|-------|------|---------|
| Name | Title | Client name |
| Instagram Handle | URL | Primary tracking |
| TikTok Handle | URL | Secondary tracking |
| YouTube Channel | URL | Video tracking |
| Facebook Page | URL | When available |
| Industry / Niche | Select | Real Estate, Business, Creator, Fitness, etc. |
| Follower Count (IG) | Number | Updated weekly via API |
| Follower Count (YT) | Number | Updated weekly |
| Follower Count (TikTok) | Number | Updated weekly |
| Status | Select | Current / Viral Accelerator / Past |
| Tier | Select | Tier 1-4 |
| Package | Select | $6K / $10K / $30K Accelerator |
| Growth Rate (weekly) | Number | Social Blade data |
| Content Market Fit | Relation | Links to their CMF profile |
| Comparable Creators | Relation | 2-5 matched creators |
| Start Date | Date | When partnership began |
| End Date | Date | When partnership ended (if past) |

### Every Client Gets

1. **Content Market Fit Profile** (from content-market-fit skill)
   - Corner 1: Their worldview (who they are, story, values)
   - Corner 2: Their audience (demographics, psychographics, 2AM problems)
   - Corner 3: Their offer (products, pricing, funnel)

2. **Performance Dashboard** (Client Performance — weekly rollup)
   - Total posts this week / total all-time
   - Posts over 100K this week
   - Best performing post / worst performing post
   - Average views per video (by platform)
   - Follower delta (weekly/monthly)
   - Viral hit rate (% of videos that cross 100K views)
   - Viral frequency: "1 in every X posts"
   - Avg viral video cadence (days between 100K+ hits)
   - Growth trajectory (up / down / flat)

3. **Style DNA**
   - What format works best for them
   - What topics drive the most views
   - What hook types perform best
   - What editing style produces the best results
   - What posting time/frequency works
   - What platform is strongest

4. **2-5 Comparable Creators/Clients**
   - Matched by industry, personality, business structure, audience
   - Cross-pollinate what works: "This hook worked for @competitor, use it for your client"

5. **Industry Context**
   - What's trending in their niche right now
   - What cultural conversations they should be part of
   - What competitors are doing that's working
   - What topics are saturated vs untapped

### Pivotal Moment Tracking

For each client, log events that correlate with growth:

| Event Type | Example | Impact |
|-----------|---------|--------|
| Viral video | Single post > 1M views | Follower spike |
| Podcast appearance | Guest on big show | Authority spike |
| Collab | Posted with bigger creator | Cross-audience growth |
| Controversy/PR | Called someone out, got called out | Engagement spike |
| Platform change | Started Reels, started Shorts | New audience |
| Milestone | Hit 100K / 500K / 1M followers | Momentum marker |
| Format shift | Switched from talking head to podcast clips | Performance change |

Cross-reference these events with Social Blade growth curves to identify WHAT actually drives growth for each niche.

---

## Layer 3: INDUSTRY INTELLIGENCE

### Per Industry, Track

| Data Point | Example |
|-----------|---------|
| Top-performing hooks this month | "Stop doing X" hooks crushing in fitness |
| Trending topics | AI tools trending in business coaching |
| Format shifts | Podcast clips outperforming solo talking head in real estate |
| Algorithm changes | Carousel reach up 40% on IG this month |
| Cultural moments | "What just happened in this industry that everyone's talking about?" |
| Competitor wins | "@competitor just hit 1M views with [topic] — should our client do this too?" |
| Saturated topics | "Day in my life" content declining in engagement |
| Screenshot opportunities | Reaction content to articles/posts/events |

### Competitor Intelligence (Per Client)

For each client's 2-5 tracked competitors:

| Data Point | Why |
|-----------|-----|
| Their top performing content (last 30 days) | What's working in this niche RIGHT NOW |
| Their format mix | What formats dominate this space? |
| Their hooks | What language resonates with this audience? |
| Their growth rate | Are they growing faster? Why? |
| Their posting frequency | Are they outworking our client? |
| Format gaps | "4 of your 5 competitors are doing podcast clips. You're not. Strategic gap." |

### Audience Research Stack

| Source | What We Extract |
|--------|----------------|
| Reddit (niche subreddits) | Exact language, complaints, desires, questions in their own words |
| Perplexity | Real-time trending questions, what people are searching |
| Grok | X/Twitter pulse, what's being debated right now |
| ChatGPT search trends | What people are asking AI about in this niche |
| Amazon reviews (competitor products) | What they loved, what they hated, what they wished existed |
| YouTube comments | Engagement signal from people who already follow |
| Instagram comments | Direct audience feedback on what resonates |

This data feeds directly into script generation. When we write a hook, we're not guessing — we're using the audience's own words back at them.

### How We Gather This

- **Client scrapes** — Our own clients' data aggregated by industry
- **Competitor scrapes** — 2-5 competitors per client tracked
- **Creator Intelligence** — Creators Drey follows, deconstructed
- **Perplexity / Grok / Reddit** — Real-time industry pulse
- **Platform trend APIs** — TikTok trending, YouTube trending, IG explore

### Output

Weekly industry brief per niche:
```
## [Industry] Weekly Intelligence — Week of [Date]

### What's Working Right Now
- Topic: [X] — avg 150K views across 5 creators
- Hook type: [Y] — 3x better engagement than average
- Format: [Z] — outperforming other formats by 2x

### Cultural Moments to Join
- [Event/conversation happening in this industry]
- Screenshot/greenscreen opportunity: [specific post/article]

### What's Declining
- [Topic/format] losing steam — avoid or innovate

### Competitor Alert
- [Competitor] did [X] that worked — consider adapting
- Format gap detected: [insight]

### Recommendation for [Client]
Film this: [specific video concept with hook]
Confidence: [score]%
```

---

## Layer 4: WEEKLY WINS

### The System

Every Monday (or automated weekly):

1. **Scrape all client accounts** — Last 7 days of content across all platforms (IG + TikTok + YT + FB)
2. **Filter for 100K+ views** — These are the "Weekly Wins"
3. **Tag in Notion** — Each win gets an entry in the Weekly Wins database
4. **Extract** from each win:
   - Exact hook (first line / first 3 seconds)
   - Topic category
   - Video format
   - Editing style used
   - Was this filmed/edited by us?
   - Client name
   - Platform
   - View count
5. **Extract hook → Hook Library** — Every winning hook gets templatized and categorized
6. **Detect outliers** — Is this video an outlier for this client? (above their average)
7. **Surface patterns** — "3 of our dental clients went viral with [topic] this week"

### Weekly Wins Database (Notion — Machine Layer)

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Hook text or video description |
| Client | Relation | → Client Profiles Roster |
| Platform | Select | IG / TikTok / YT / FB |
| URL | URL | Direct link to the post |
| Views | Number | View count |
| Engagement Rate | Number | Likes + comments + saves + shares / views |
| Posted Date | Date | When published |
| Topic | Multi-select | Category tags |
| Hook Type | Select | Question / Bold Claim / Pattern Interrupt / Story / Stat / Accusation |
| Video Format | Select | Solo / Podcast / Street / Greenscreen / B-roll / Carousel / etc. |
| Filmed By Us | Checkbox | Did Viral Editz film this? |
| Edited By Us | Checkbox | Did Viral Editz edit this? |
| Outlier | Checkbox | Above client's average by 2x+ |
| Industry | Multi-select | Client's industry |
| Hook | Relation | → Hook Library |
| Recreate Script | Rich text | Generalized template for clones |
| Image Gen Prompt | Rich text | For clone visual |
| Video Gen Prompt | Rich text | For clone animation |

### Hook Library (Notion — Machine Layer)

**Dave Gate Justification:** Hooks are the #1 thing creators ask for. "What hook should I use?" is a daily bottleneck for every client session, every filming day, every script. Hooks are also a sellable/leverageable asset — they can be packaged for lead magnets, courses, consulting materials. The Hook Library is fed automatically from Weekly Wins and Video Deconstruction entries.

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | The exact hook text |
| Hook Framework | Select | Question / Bold Claim / Pattern Interrupt / Accusation / Story Open / Stat / Controversy / How-To |
| Psychology Key | Select | MIRROR / TRIGGER / PATTERN / LEVERAGE / TRUST |
| Template Version | Rich text | Generalized: "I [achieved result] in [timeframe] with [simple method]" |
| Source Post URL | URL | Where this hook came from |
| Source Views | Number | How many views the source post got |
| Platform | Select | IG / TikTok / YT / FB |
| Niche / Industry | Multi-select | What industries this hook works in |
| Cross-Niche Proven | Checkbox | Has this hook pattern worked in 2+ industries? |
| Client | Relation | → Client Profiles Roster |
| Used In | Relation | → Content Scripts (track reuse) |
| Times Reused | Number | How many scripts have used this hook pattern |
| Avg Performance When Reused | Number | Average views when this hook pattern is used |
| Date Added | Date | When extracted |
| Source | Select | Weekly Wins / Creator Intelligence / Competitor Scrape / Manual |

**How Hook Library Gets Fed:**
```
Weekly Wins (100K+ videos) ──→ Extract hook ──→ Hook Library entry
                                                    ↓
Video Deconstruction DB ────→ Extract hook ──→ Hook Library entry
                                                    ↓
Competitor Scrapes ─────────→ Extract hook ──→ Hook Library entry
                                                    ↓
Manual entry (Drey/Ryan) ──→ Direct add ────→ Hook Library entry

Every hook gets:
1. Exact text preserved
2. Framework categorized (question, accusation, stat, etc.)
3. Psychology key tagged (MIRROR, TRIGGER, PATTERN, LEVERAGE, TRUST)
4. Template version created ("I [X] in [Y] with [Z]")
5. Performance data attached
6. Cross-niche flag if proven in multiple industries
```

**Internal + External Use:**
- **Internal:** Every script generation pulls from Hook Library. "Give me the top 5 question hooks that worked in real estate this month."
- **External/Sellable:** Package top hooks as lead magnets, course materials, consulting deliverables. "Here are 50 hooks proven to get 100K+ views in your niche."

### Who Uses the Weekly Wins

| User | How They Use It |
|------|----------------|
| **Ryan Magin (real)** | "What should I film this week?" → Top wins across all clients |
| **Ryan Magin (clone)** | Auto-generate scripts modeled after wins, in Ryan's voice |
| **Drey (real)** | "What should I film this week?" → Wins matched to his CMF |
| **Luis Carrillo (clone)** | Auto-generate scripts in Luis's voice |
| **Claudia (clone)** | Auto-generate podcast scripts modeled after wins |
| **Viral Editz team** | Know what's working, double down for each client |
| **Client strategy sessions** | "Here's what worked this week in your industry" |
| **Consulting clients** | "Here are your 7 videos to film, backed by data" |

### The Weekly Wins → Content Pipeline

```
WEEKLY WINS (raw data from 100K+ posts)
    │
    ├── STEP 1: Extract hook + framework
    │   "What made this work? What's the psychology?"
    │
    ├── STEP 2: Templatize the hook → Hook Library
    │   Original: "I made $100K from one video"
    │   Template: "I [achieved result] in [timeframe] with [simple method]"
    │
    ├── STEP 3: Run through Content Market Fit filter
    │   For Drey: How does this hook serve Drey's offer/worldview/audience?
    │   For Ryan: How does this hook serve Ryan's offer/worldview/audience?
    │   For Claudia: How does this hook serve Claudia's 5 Keys?
    │   For Client: How does this hook serve their CMF triangle?
    │
    ├── STEP 4: Generate scripts (per persona)
    │   Drey version (real Drey voice, his topics, his audience)
    │   Ryan version (Ryan's energy, his topics, his audience)
    │   Claudia version (her 5 Keys, her AI angle, her audience)
    │   Client version (their niche, their voice, their audience)
    │
    ├── STEP 5: Generate image + video prompts (clone era)
    │   Thumbnail / key visual (Nano Banana Pro / Gemini API)
    │   Video animation prompt (Higgsfield / Kling 2.1)
    │
    └── STEP 6: Package for filming
        Bullet points, context, screenshots, articles
        "Here's what you film today. Here's why. Here are your talking points."
```

### Outlier Detection

Per client, calculate:
- Average views per video (rolling 30 days)
- Standard deviation
- Any video > 2x average = "Outlier" tag
- Track: "What % of videos become outliers?"
- Track: "Average outlier frequency per client" (e.g., 1 in every 5 videos)
- Track: "Average time between million-view videos per client"
- Track: "Sudden view spike with normal followers = algorithm push"

**Why this matters:** A 100K view video for a 500K follower account is average. A 100K view video for a 10K follower account is an outlier. We need to know the difference.

---

## Layer 5: EXECUTION

### The "What Do I Film Today?" Command

This is the killer feature. Any creator (Drey, Ryan, or client) opens Claude and asks:

**"What do I film today?"**

Claude responds with:

```
═══════════════════════════════════════════════════════
 DAILY FIRE BRIEF — [Name] — [Date]
═══════════════════════════════════════════════════════

 TOP 3 VIDEOS TO FILM TODAY:

 #1 — DATA-BACKED BANGER
 Topic: [X]
 Hook: "[exact hook]"
 Why now: [trending + proven by client data]
 Inspired by: [Client X's post that got 450K views]
 Format: [talking head / green screen / etc.]
 Duration: [30-60 seconds]
 Key: [MIRROR/TRIGGER/PATTERN/LEVERAGE/TRUST]
 Filming notes: [bullet points, context, energy direction]
 Confidence score: 94%

 #2 — CULTURAL MOMENT
 Topic: [X]
 Hook: "[exact hook]"
 Why now: [something happened in the industry this week]
 Screenshot/article: [attached]
 Format: [green screen reaction / stitch]

 #3 — EVERGREEN BANGER
 Topic: [X]
 Hook: "[exact hook]"
 Why now: [this framework works every time, your audience
          hasn't seen your take on it yet]

 ─────────────────────────────────────────────────────
 PULSE CHECK:
 - 7 videos hit 100K+ across clients this week
 - Top performing niche: [X]
 - Top performing format: [X]
 - Your last viral was [X] days ago (avg cadence: [X] days)
 - You're due for a hit. Film #1 first.
═══════════════════════════════════════════════════════
```

### Weekly Filming Package

The deliverable each client/persona receives:

```
═══════════════════════════════════════════════════════
 FILMING PACKAGE — [Name] — Week of [Date]
═══════════════════════════════════════════════════════

 7 VIDEOS TO FILM THIS WEEK:

 For each video:
 ├── Title / Topic
 ├── Hook (exact first line) → from Hook Library
 ├── Key talking points (3-5 bullets)
 ├── Why this works (data backing)
 ├── Inspired by (link to winning post from Weekly Wins)
 ├── Format (talking head / podcast / green screen / etc.)
 ├── Duration target
 ├── Tonality direction ("get agitated" / "be calm and
 │   measured" / "laugh about how absurd this is")
 ├── Screenshots / articles / context (if needed)
 ├── CTA
 ├── Image Gen Prompt (for thumbnail/visual)
 ├── Video Gen Prompt (for clone animation)
 └── Confidence score (how likely to perform based on data)

 BONUS CONTEXT:
 ├── Industry trending this week: [3 topics]
 ├── Cultural moment to react to: [description + link]
 ├── Competitor doing something interesting: [link]
 └── Your audience is asking about: [Reddit/search data]
═══════════════════════════════════════════════════════
```

### Content Scripts Database (Notion — Machine Layer)

Track the full lifecycle from script to performance:

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Script title / topic |
| Script Text | Rich text | Full script with hook, talking points, CTA |
| For Whom | Select | Drey / Ryan / Claudia / [Client Name] |
| Clone or Real | Select | Clone (AI-generated) / Real (human films) |
| Hook | Relation | → Hook Library |
| Psychology Key | Select | MIRROR / TRIGGER / PATTERN / LEVERAGE / TRUST |
| Topic Score | Number | Data-backed confidence score |
| Inspired By | Relation | → Weekly Wins (source post) |
| Format Recommendation | Select | Talking head / Podcast / Green screen / etc. |
| Tonality | Rich text | Energy/delivery direction |
| Filming Notes | Rich text | Context, screenshots, articles |
| Image Gen Prompt | Rich text | Thumbnail / visual prompt |
| Video Gen Prompt | Rich text | Clone animation prompt |
| Status | Select | Draft / Approved / Filmed / Posted / Tracking |
| Post URL | URL | Link to published post (after posting) |
| Post Views | Number | Performance (after posting) |
| Post Engagement | Number | Engagement rate (after posting) |
| Was It an Outlier? | Checkbox | Did it outperform average? |

### Output Volume Per Persona

| Persona | Content Source | Voice/Style | Volume |
|---------|--------------|-------------|--------|
| Real Drey | Weekly Wins + CMF + Industry Intel | Drey's voice, his worldview, his audience | 5-7 videos/week |
| Luis Clone | Same + auto-filtered by CMF | Luis's voice (AI-generated scripts) | 3-5 additional/week |
| Real Ryan | Weekly Wins + CMF + Industry Intel | Ryan's energy, Speed to Post | 5-7 videos/week |
| Ryan Clone | Same + auto-filtered by CMF | Ryan's voice (AI-generated scripts) | 3-5 additional/week |
| Claudia | Weekly Wins + 5 Keys filter + CMF | Claudia's voice, psychology angle | 7-10 Reels/week |
| Each Client | Industry Intel + their CMF + Wins | Their brand voice, their niche | Per package (2/day for $6K) |

### For Consulting / Strategy Sessions

When Ryan (or anyone on team) does a strategy session with a client or prospect:

```
Pre-session briefing (auto-generated):
1. Client's CMF profile (who they are, audience, offer)
2. Their last 30 days performance (what worked, what didn't)
3. Their industry's last 30 days (what's trending, what's declining)
4. 3 comparable creators + what's working for them
5. 5 specific video concepts with hooks (ready to film)
6. Recommended format based on data (podcast? solo? street?)
7. Tonality recommendation ("Get Ryan agitated — that's when he films best")
8. Competitor analysis ("Your top competitor posted 3x more and grew 2x faster")
9. Audience language ("Your audience is asking about X on Reddit right now")
```

**What this means for consulting:**

When Ryan or Drey sits down with a consulting client, they're not giving generic advice. They're saying:

"In your niche, the top performing format right now is podcast clips. The hooks that work use accusation frameworks. Your competitor posted 3x more than you last month and grew 2x faster. Here are the exact 7 videos you need to film this week, with hooks proven to work by our data across 15+ accounts in your space. Here's the script. Here's the energy. Film it."

That's not a strategy session. That's a cheat code.

### The Unfair Advantage Stack

| Advantage | What It Means |
|-----------|--------------|
| **90 client history** | We've seen what works across 20+ industries |
| **Weekly real-time data** | We know what's working RIGHT NOW, not 6 months ago |
| **Cross-industry pattern matching** | "This hook works in dental AND real estate" |
| **Hook Library** | Sellable asset — proven hooks categorized by framework, psychology, niche |
| **Clone-ready templates** | Any winning video can be recreated for any character |
| **AI-powered research** | Perplexity, Grok, Reddit for audience language |
| **Full pipeline automation** | From data → insight → script → image → video → post |
| **Before/after proof** | "We took @client from 20K to 1M followers" |
| **Confidence scores** | Every recommendation backed by data, not guesswork |

---

## Two-Tier Data Architecture

### Why Two Tiers?

We need to track EVERY post (not just 100K+ wins) to monitor performance, catch declines early, and have the full picture. But scale is real:
- Ryan Magin: ~4,000 posts over 5 years
- The Credit Brothers: ~2,000 posts
- Epic Dental: ~1,000 posts
- The Baileys: ~1,000 posts
- 4 clients alone = ~8,000-10,000 entries

Notion handles ~10,000 rows per database before performance degrades. Solution: per-client databases for raw data, unified databases for intelligence.

### Tier 1: Per-Client Content Databases (ALL Posts — Raw Data)

Each client gets their own Notion database with EVERY post scraped across all platforms.

```
[Client Name] Content DB
    ├── Every Instagram post
    ├── Every TikTok video
    ├── Every YouTube Short + long-form
    ├── Every Facebook post (when available)
    └── Updated weekly via automated scrape
```

**Per-Client Content DB Schema:**

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Hook text / first line (human-readable, NOT post_id) |
| Post ID | Rich text | Platform post identifier |
| URL | URL | Direct link |
| Platform | Select | IG / TikTok / YT / FB |
| Post Type | Select | Reel / Carousel / Image / Short / Long-form / Story |
| Date Posted | Date | When published |
| Views | Number | View count |
| Likes | Number | Like count |
| Comments | Number | Comment count |
| Shares | Number | Share count |
| Saves | Number | Save count (IG) |
| Engagement Rate | Number | (likes + comments + saves + shares) / views |
| Duration (seconds) | Number | Length in seconds (NUMBER, not text) |
| Caption | Rich text | Full caption text |
| Transcript | Rich text | Full video transcript |
| Hook | Rich text | First line / first 3 seconds extracted |
| Topic | Multi-select | Category tags |
| Hook Type | Select | Question / Bold Claim / Pattern Interrupt / Accusation / Story / Stat |
| Format | Select | Solo / Podcast / Street / Greenscreen / B-roll / Two people / Carousel |
| # of People | Number | How many people appear |
| Editing Style | Multi-select | Jump cuts / B-roll / Text overlays / etc. |
| Location | Multi-select | Studio / Street / Office / etc. |
| Guest | Rich text | Who appears (if not solo) |
| Year | Number | Year posted |
| Is Outlier | Checkbox | Above client's 2x average |
| Is Win (100K+) | Checkbox | Over 100,000 views |
| Filmed By Us | Checkbox | Did Viral Editz film this? |
| Edited By Us | Checkbox | Did Viral Editz edit this? |
| Script Template | Rich text | Templatized version for reuse |
| CTA | Multi-select | What call to action was used |

**Active Per-Client Databases:**

| Client | Platforms | Est. Posts | Status |
|--------|----------|------------|--------|
| The Credit Brothers | IG + TikTok + YT + FB | ~2,000 | **SCRAPING NOW** |
| Ryan Magin | IG (exists) + TikTok + YT | ~4,000 | Existing IG DB needs migration + expand |
| Epic Dental | IG + TikTok + YT | ~1,000 | Next |
| The Baileys | IG + TikTok + YT | ~1,000 | Next |

### Tier 2: Intelligence Databases (Cross-Client — Filtered)

These stay UNIFIED because they're the queryable intelligence layer:

```
Weekly Wins (100K+ from ALL clients)      — fed from per-client DBs
Hook Library (extracted hooks)             — fed from wins + scrapes
Client Performance (weekly rollups)        — calculated from per-client DBs
Industry Intelligence (per niche)          — aggregated from all data
Content Scripts (output pipeline)          — generated from intelligence
```

### Tier 3: Google Sheets (Backup + Unlimited Query)

Mirror of ALL raw data. Every post, every client, one master spreadsheet.

| Sheet | Contents | Purpose |
|-------|----------|---------|
| All Content (Master) | Every post from every client | Unlimited rows, pivot tables, raw queries |
| Per-client sheets | Filtered views | Quick client-specific analysis |
| Performance Dashboard | Weekly rollups | Charts, trends, alerts |
| Hook Library | All extracted hooks | Shareable, exportable |

Google Sheets is the backup AND the "chat with the data" layer. Notion is for AI integration + Brain Hub. Sheets is for raw power + sharing.

---

## Performance Alert System — "Punch Me in the Face" Protocol

### How It Works

Every week, the system automatically:

1. Pulls all posts from last 7 days per client (from per-client DBs)
2. Calculates: total views, avg views per post, engagement rate, posting frequency
3. Compares against:
   - Their rolling 30-day average
   - Their best month ever
   - Their weekly target (e.g., 1M views/week)
   - Industry benchmark for their niche

### Alert Levels

```
🔴 RED ALERT — Total views < 50% of 30-day average
   ═══════════════════════════════════════════════════
   ACCOUNT EMERGENCY — [Client Name] — [Date]
   ═══════════════════════════════════════════════════

   This week: [X] total views
   30-day avg: [Y] total views/week
   Delta: DOWN [Z]%

   WHAT CHANGED:
   ├── Posting frequency: [same / decreased / increased]
   ├── Topic shift detected: [Y/N — if yes, what changed]
   ├── Format shift detected: [Y/N]
   ├── Algorithm indicator: [engagement rate change]
   ├── Competitor gaining: [Y/N — competitor data]
   └── External factor: [platform change / news / etc.]

   IMMEDIATE ACTIONS (auto-researched):
   1. [Specific corrective action with data backing]
   2. [Specific corrective action with data backing]
   3. [Specific corrective action with data backing]

   COMPARABLE DATA:
   - What's working for competitors this week: [X]
   - What's working in this niche this week: [X]
   - Last time this client recovered from a dip: [date, what they did]
   ═══════════════════════════════════════════════════

🟡 YELLOW — Total views < 80% of 30-day average
   "Slight decline detected for [Client]. Monitor next week."
   - Flag specific underperforming posts
   - Note any topic/format changes
   - Suggest 2 corrective actions

🟢 GREEN — On pace or above average
   "[Client] hit [X] views this week. On pace. Top post: [link]"
   - Document what's working
   - Recommend doubling down on winning topics

🚀 BREAKOUT — Any single post > 500K views (or 5x client average)
   "BREAKOUT for [Client]: [post link] hit [X] views!"
   - Extract exactly what made it work
   - Hook, topic, format, timing, editing style
   - "Film 3 more like this immediately"
   - Generate 3 similar scripts with different hooks
```

### Weekly Performance Report (Per Client)

```
═══════════════════════════════════════════════════════
 PERFORMANCE REPORT — [Client Name] — Week of [Date]
═══════════════════════════════════════════════════════

 STATUS: [🔴 RED / 🟡 YELLOW / 🟢 GREEN / 🚀 BREAKOUT]

 THIS WEEK:
 ├── Total views: [X] ([+/-]% vs 30-day avg)
 ├── Total posts: [X]
 ├── Avg views per post: [X]
 ├── Best post: [link] — [X] views
 ├── Worst post: [link] — [X] views
 ├── Engagement rate: [X]% ([+/-]% vs avg)
 ├── New followers: [X] ([platform breakdown])
 └── Posts over 100K: [X] out of [Y]

 VIRAL METRICS:
 ├── Viral frequency: 1 in every [X] posts
 ├── Days since last viral (100K+): [X]
 ├── Avg cadence between virals: [X] days
 └── Growth trajectory: [UP ↑ / DOWN ↓ / FLAT →]

 TOP PERFORMING:
 ├── Topic: [X]
 ├── Format: [X]
 ├── Hook type: [X]
 └── Best posting time: [X]

 RECOMMENDATIONS:
 1. [Action item based on data]
 2. [Action item based on data]
 3. [Action item based on data]

 COMPETITOR CONTEXT:
 ├── [Competitor 1]: [X] views this week ([comparison])
 └── [Competitor 2]: [X] views this week ([comparison])
═══════════════════════════════════════════════════════
```

### Targets (Per Client — Customizable)

| Client | Weekly View Target | Alert Threshold | Current Status |
|--------|-------------------|-----------------|----------------|
| The Credit Brothers | 1,000,000 | < 500K = RED | TBD (scraping now) |
| Ryan Magin | TBD | TBD | TBD |
| Epic Dental | TBD | TBD | TBD |
| The Baileys | TBD | TBD | TBD |

Targets get set after first full scrape establishes baseline.

---

## Notion Database Map (Complete)

```
CLIENT ACCOUNTS (master registry — 86 entries, LIVE)
    │
    ├── PER-CLIENT CONTENT DBs (ALL posts — raw data, Tier 1)
    │       ├── The Credit Brothers Content DB (IG + TT + YT + FB)
    │       ├── Ryan Magin Content DB (IG, existing + expand)
    │       ├── Epic Dental Content DB (IG + TT + YT)
    │       ├── The Baileys Content DB (IG + TT + YT)
    │       └── [Future clients as onboarded]
    │
    ├── WEEKLY WINS (100K+ posts, all clients, rolling)
    │       └── Relation → Hook Library
    │       └── Relation → Client Account
    │       └── Fed FROM per-client content DBs
    │
    ├── HOOK LIBRARY (extracted hooks, categorized, sellable)
    │       └── Relation → Weekly Wins (source)
    │       └── Relation → Content Scripts (usage)
    │
    ├── CONTENT MARKET FIT (per client + per persona)
    │       └── Relation → Client Account
    │
    ├── INDUSTRY INTELLIGENCE (per niche)
    │       └── Relation → Client Accounts in this niche
    │
    ├── CLIENT PERFORMANCE (weekly rollup + ALERTS)
    │       └── Relation → Client Account
    │       └── Alert level: 🔴🟡🟢🚀
    │       └── Pivotal Moments log
    │
    ├── CREATOR INTELLIGENCE (external creators / competitors)
    │       └── Video Deconstruction DB (per-video analysis)
    │       └── Relation → Hook Library (hooks extracted)
    │
    └── CONTENT SCRIPTS (output — what gets filmed)
            └── Relation → Hook Library
            └── Relation → Weekly Wins (inspired by)
            └── Status lifecycle: Draft → Approved → Filmed → Posted → Tracking
```

**GOOGLE SHEETS BACKUP (Tier 3):**
```
Viral Editz Master Sheet
    ├── All Content (every post, every client, every platform)
    ├── Per-client filtered sheets
    ├── Performance Dashboard (weekly rollups, charts)
    └── Hook Library export
```

### Database Status

| Database | Layer | Status | Dave Gate |
|----------|-------|--------|-----------|
| Client Profiles - Viral Editz Roster | Machine | **LIVE — 86 clients, social URLs added** | Solves "who are our clients?" |
| Client Profiles (deep) | Machine | EXISTS — 8 detailed entries | Solves "what's their psychology?" |
| Per-client CMF databases | Machine | EXISTS — 4 clients have them | Solves "what's their Content Market Fit?" |
| Viral Editz Intelligence | Machine | **LIVE — company page built** | Solves "what is Viral Editz?" |
| **Ryan Magin Content DB** | Machine | **EXISTS — needs migration + expand** | Solves "what has Ryan posted?" |
| **The Credit Brothers Content DB** | Machine | **SCRAPING NOW — first full scrape** | Solves "what have Credit Bros posted?" |
| Epic Dental Content DB | Machine | TO CREATE — after The Credit Brothers | Solves "what has Epic Dental posted?" |
| The Baileys Content DB | Machine | TO CREATE — after The Credit Brothers | Solves "what have The Baileys posted?" |
| Creator Intelligence DB | Machine | NEW — competitors identified from scrapes | Solves "what makes this creator work?" |
| Video Deconstruction DB | Machine | NEW — created when first scrape runs | Solves "why did this specific video work?" |
| **Weekly Wins DB** | Machine | TO CREATE — Phase 2 | Solves "what should we film this week?" |
| **Hook Library** | Machine | TO CREATE — Phase 2 | Solves "what hook should I use?" + sellable asset |
| **Content Scripts** | Surface | TO CREATE — Phase 3 | Solves "what's the full script + lifecycle?" |
| **Client Performance** | Machine | TO CREATE — Phase 2 (with alert system) | Solves "how is this client doing?" + alerts |
| **Industry Intelligence** | Machine | TO CREATE — Phase 3 | Solves "what's trending in this niche?" |
| Content & Ideas | Surface | EXISTS — scripts route here | Production pipeline output |
| Master Frameworks | Underground | EXISTS — CMF 2026 routes here | Core methodology storage |
| **Google Sheets Master** | Backup | TO CREATE — mirrors all raw data | Unlimited query + backup + sharing |

---

## Dave Compliance

- All new databases → Machine Layer (HOW to execute), except Content Scripts → Surface (WHAT people see)
- All operations → ADDITIVE only
- Source → Asset → Context on every entry
- Change Log on everything
- Database Purity maintained:
  - Creator Intelligence ≠ Council (content patterns vs expertise)
  - Weekly Wins ≠ Content & Ideas (wins tracking vs production pipeline)
  - Client Roster ≠ Client Profiles (lightweight roster vs deep psychology)
  - Hook Library ≠ Weekly Wins (reusable hook templates vs raw win data)
  - Content Scripts ≠ Content & Ideas (full lifecycle tracking vs idea pipeline)
- Dave Gate: Every database solves a specific bottleneck
  - Weekly Wins → "What should we film this week?" (currently a manual guess)
  - Hook Library → "What hook should I use?" (currently intuition + memory) + sellable/leverageable asset
  - Industry Intelligence → "What's trending in this niche?" (currently requires manual research)
  - Creator Intelligence → "What makes this creator's content work?" (currently intuition only)
  - Content Scripts → "What's the status of this script? Did it perform?" (currently no tracking)
  - Client Performance → "How is this client doing week over week?" (currently manual review)

---

## Implementation Phases

### Phase 1: Foundation (NOW — IN PROGRESS)
- [x] Content Market Fit skill built
- [x] Creator Intelligence skill built
- [x] Image Generation skill built
- [x] Viral Editz company page in Notion (109 blocks)
- [x] 86 clients added to Roster (with Status + Tier)
- [x] Battle Plan v3.0 written (merged + alert system + two-tier architecture)
- [x] Social URL properties added to Roster (Instagram, TikTok, YouTube, Facebook)
- [x] The Credit Brothers handles added to Roster (all 4 platforms)
- [x] Performance Alert System designed (🔴🟡🟢🚀 levels)
- [x] Two-Tier Architecture designed (per-client DBs + unified intelligence)
- [ ] **The Credit Brothers full scrape running** (IG + TikTok + YT + FB — other terminal)
- [ ] Identify The Credit Brothers competitors from scrape data
- [ ] Ryan Magin DB migration + expand to TikTok/YT
- [ ] Epic Dental full scrape (all platforms)
- [ ] The Baileys full scrape (all platforms)
- [ ] Run Content Market Fit interview on Drey (AI podcast style)
- [ ] Collect Ryan Magin reference photos for Soul ID

### Phase 2: Weekly Wins + Hook Library (Build Now)
- [ ] Create Weekly Wins database in Notion
- [ ] Create Hook Library database in Notion
- [ ] Create Client Performance database in Notion
- [ ] Set up Apify actors for all current client accounts (15)
- [ ] Build automated weekly scrape → filter → tag pipeline
- [ ] Build hook extraction pipeline (Weekly Wins → Hook Library)
- [ ] First weekly wins report generated
- [ ] First hooks extracted and templatized

### Phase 3: Intelligence + Scripts (Build Next)
- [ ] Create Industry Intelligence database in Notion
- [ ] Create Content Scripts database in Notion
- [ ] Define industries from client roster (group clients by industry)
- [ ] Set up competitor tracking (2-5 per client)
- [ ] Build weekly industry brief template
- [ ] Build "What Do I Film Today?" command (Daily Fire Brief)
- [ ] Build Filming Package weekly output
- [ ] Clone content pipeline: wins → scripts for Ryan/Drey/Claudia
- [ ] Audience research automation (Reddit API + Perplexity + Grok)
- [ ] First industry intelligence report generated

### Phase 4: Cross-Platform + Growth Tracking
- [ ] Social Blade integration (or alternative API) for historical growth
- [ ] Before/after tracking for all 86 clients
- [ ] Cross-platform dashboard (IG + TikTok + YT + FB)
- [ ] Outlier detection algorithm running
- [ ] Pivotal moment tracking active
- [ ] Confidence scoring on all recommendations

### Phase 5: Financial Intelligence
- [ ] Connect Viral Editz Google Drive (Option 1 or 2)
- [ ] Ingest financial reports, quarterly reviews
- [ ] Client pricing tracker (who pays what, revenue per client)
- [ ] Staff cost tracking
- [ ] Opportunity/bottleneck detection running weekly

### Phase 6: Full Automation
- [ ] Every client has complete CMF profile
- [ ] Every client has 2-5 comparable creators tracked
- [ ] Weekly wins auto-generated every Monday
- [ ] Hook Library growing automatically with every weekly scan
- [ ] Industry briefs auto-generated weekly
- [ ] Daily Fire Brief available on demand for any persona
- [ ] Weekly Filming Packages auto-generated for all active clients
- [ ] Content Scripts tracked from Draft → Posted → Performance
- [ ] Clone content pipeline producing 10+ scripts/week
- [ ] Strategy session briefings auto-generated before each call
- [ ] Financial intelligence surfacing opportunities weekly
- [ ] Client onboarding automation: new client → full CMF → first filming package in 48 hours

---

## The SOP (Standard Operating Procedure)

### Daily (Phase 6 goal)
- "What do I film today?" available for Drey, Ryan, any client
- Content Scripts status updates (Filmed → Posted)
- Performance tracking on posted content

### Weekly (Phase 2+)
1. **Monday AM:** Auto-scrape all current client accounts (last 7 days) across IG + TikTok + YT + FB
2. **Monday AM:** Filter for 100K+ views → Weekly Wins database
3. **Monday AM:** Extract hooks → Hook Library
4. **Monday AM:** Generate industry briefs per niche
5. **Monday AM:** Update Client Performance rollups
6. **Monday PM:** Clone content pipeline → 10+ scripts for Ryan/Drey/Claudia
7. **Monday PM:** Generate Weekly Filming Packages for active clients
8. **Friday:** Review weekly performance, flag any declining clients, update pivotal moments

### Monthly (Phase 3+)
1. Re-scrape competitor accounts
2. Update industry intelligence trends
3. Social Blade growth check for all clients
4. Financial review (once Drive connected)
5. Re-run Viral Accelerator topic generation for active clients
6. Hook Library audit — which hook patterns are performing best?

### Quarterly
1. Full CMF audit for all current clients (is the triangle still aligned?)
2. Comparable creator refresh (are the right 2-5 still comparable?)
3. Before/after report for all clients (growth delta)
4. Strategy for next quarter based on aggregated data
5. Hook Library package — top performing hooks for lead magnets/courses
6. Client onboarding process review — optimize the 48-hour pipeline

---

## Technical Pipeline (How Data Actually Flows)

### Scraping Pipeline
```
Apify Actor (per client, per platform)
    ↓
Raw data → Python processing script
    ↓
Filter: 100K+ views → Weekly Wins DB (Notion API)
    ↓
Extract hooks → Hook Library DB (Notion API)
    ↓
Aggregate by industry → Industry Intelligence DB
    ↓
Update Client Performance rollup
```

### Video Deconstruction Pipeline (Creator Intelligence)
```
Instagram handle → Apify scrape → engagement scoring (S/A/B/C)
    ↓
Top 20-30 videos → yt-dlp download
    ↓
ffmpeg frames (3s intervals) + mlx_whisper transcribe
    ↓
Hume AI (emotion detection) + Twelve Labs (video understanding)
    ↓
Video Deconstruction Card (hook, topic, script, format, editing, CTA, emotion arc)
    ↓
Hooks extracted → Hook Library
    ↓
Patterns surfaced → Creator Intelligence DB + Industry Intelligence
```

### Script Generation Pipeline
```
Weekly Wins + Hook Library + CMF Profile + Industry Intel
    ↓
Filter by persona's Content Market Fit
    ↓
Generate script (Viral Accelerator + YAP Generator)
    ↓
Add image gen prompt (Nano Banana Pro / Gemini API)
    ↓
Add video gen prompt (Higgsfield / Kling 2.1)
    ↓
Content Scripts DB (status: Draft)
    ↓
Review → Approved → Filmed → Posted → Track Performance
```

---

## Change Log

- 2026-02-06: Created v1.0. Source: Luis Carrillo brain dump session. Captures full Viral Editz Brain Intelligence vision.
- 2026-02-06: Updated to v2.0. Merged with second terminal's battle plan. Added: Hook Library (Dave-approved — sellable asset + daily bottleneck solver), Daily Fire Brief output format, Weekly Filming Package template, Pivotal Moment Tracking, Content Scripts database with full lifecycle, Confidence Scores, Audience Research Stack, Competitor Intelligence detail, Output Volume per persona table, Unfair Advantage Levels (1-5), Technical Pipeline diagrams. Platform priorities clarified: IG > YT > TikTok > FB (current), X + LinkedIn (future expansion). All additions Dave-compliant.
- 2026-02-06: Updated to v3.0. Major architecture change: Two-Tier data system (per-client content DBs for ALL posts + unified intelligence DBs for cross-client queries). Added: Performance Alert System ("Punch Me in the Face" Protocol) with 4 alert levels (🔴🟡🟢🚀), per-client content database schema (tracks EVERY post not just 100K+), Google Sheets as Tier 3 backup + unlimited query layer, Weekly Performance Report template, per-client targets with alert thresholds. The Credit Brothers handles added to Notion Roster. "Credit Brothers" → "The Credit Brothers" everywhere. First active scrape: The Credit Brothers (IG + TikTok + YT + FB) running on other terminal.
