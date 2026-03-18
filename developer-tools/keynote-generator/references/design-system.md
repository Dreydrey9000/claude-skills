# Keynote Design System — Extracted from Gold Standard

## Color Palette (Apple-inspired)
| Variable | Hex | Use |
|----------|-----|-----|
| `--black` | `#000000` | Background (ALWAYS) |
| `--white` | `#ffffff` | Primary text |
| `--gray` | `#86868b` | Secondary text, subtitles, section labels |
| `--blue` | `#2997ff` | Tech, innovation, accent |
| `--green` | `#30d158` | Solution, success, money |
| `--purple` | `#bf5af2` | Premium, creative, reveal |
| `--orange` | `#ff9f0a` | Attention, energy |
| `--red` | `#ff453a` | Problem, pain, old way |

## Supporting Colors
| Hex | Use |
|-----|-----|
| `#111` | Terminal/demo background |
| `#1a1a1a` | Terminal bar, subtle borders |
| `#222` | Terminal border |
| `#333` | Inactive nav dots, muted borders |
| `#555` | Quote author, very muted text |
| `#999` | List items in VS cards |
| `#1a0a0a` | Old-way card background (red tint) |
| `#0a1a0a` | New-way card background (green tint) |
| `#331a1a` | Old-way card border |
| `#1a331a` | New-way card border |

## Typography Scale
```
Hero:          clamp(48px, 8vw, 96px)  — weight 800, tracking -3px, line-height 1.05
Sub-hero:      clamp(20px, 3vw, 32px)  — weight 400, color gray, line-height 1.4
Section label: 14px                     — weight 600, uppercase, tracking 4px
Quote:         clamp(24px, 4vw, 42px)  — weight 300, italic, color gray
Step number:   72px                     — weight 900, opacity 0.15
Step heading:  24px                     — weight 700, white
Step body:     16px                     — weight 400, gray, line-height 1.6
Stat number:   clamp(48px, 7vw, 80px)  — weight 900, tracking -2px
Stat label:    14px                     — uppercase, tracking 2px, gray
```

## Slide Types with HTML

### Type 1: Statement Slide
```html
<div class="slide">
  <div class="fade-in">
    <div class="hero-text">Big statement<br><span class="accent-red">with color.</span></div>
    <div class="sub-hero">One line of context.</div>
  </div>
</div>
```

### Type 2: VS Comparison
```html
<div class="slide">
  <div class="fade-in">
    <div class="hero-text" style="font-size: clamp(36px, 5vw, 64px);">Two ways.</div>
    <div class="vs-container">
      <div class="vs-side old"><h3>The old way</h3><ul><li>Pain point</li></ul></div>
      <div class="vs-side new"><h3>The new way</h3><ul><li>Solution</li></ul></div>
    </div>
  </div>
</div>
```

### Type 3: Reveal (Gradient)
```html
<div class="slide">
  <div class="fade-in">
    <div class="section-label">Introducing</div>
    <div class="hero-text"><span class="accent-gradient">Product Name.</span></div>
    <div class="sub-hero">One sentence description.</div>
  </div>
</div>
```

### Type 4: Three Steps
```html
<div class="slide">
  <div class="fade-in">
    <div class="section-label">How it works</div>
    <div class="hero-text" style="font-size: clamp(36px, 5vw, 64px);">Three steps.</div>
    <div class="steps-row">
      <div class="step-card">
        <div class="step-num accent-blue">1</div><h3>Name</h3><p>Description</p>
      </div>
      <!-- repeat for 2, 3 -->
    </div>
  </div>
</div>
```

### Type 5: Demo Terminal
```html
<div class="demo-terminal">
  <div class="demo-bar">
    <div class="demo-dot r"></div><div class="demo-dot y"></div><div class="demo-dot g"></div>
    <span>App Name</span>
  </div>
  <div class="demo-body">
    <span class="demo-prompt">user →</span> command here<br>
    <span class="demo-response">Response here</span><br>
    <span class="demo-quote">"Quoted output"</span>
  </div>
</div>
```

### Type 6: Stats Row
```html
<div class="stats-row">
  <div class="stat-item"><div class="stat-num accent-blue">185+</div><div class="stat-label">Label</div></div>
  <!-- repeat for each stat -->
</div>
```

### Type 7: Layer Stack
```html
<div class="layer-stack">
  <div class="layer-row">
    <div class="layer-emoji">🧠</div>
    <div class="layer-info"><h4>Name</h4><p>One line.</p></div>
  </div>
</div>
```

### Type 8: One More Thing
```html
<div class="slide">
  <div class="fade-in">
    <div class="section-label">One more thing.</div>
    <div class="omt-reveal">
      The reveal.<br>
      It <span class="accent-blue">does</span> this.<br>
      It <span class="accent-purple">does</span> that.<br>
      It <span class="accent-green">changes everything</span>.
    </div>
  </div>
</div>
```

## JavaScript (Copy from gold standard)
- IntersectionObserver for `.fade-in` elements (threshold 0.15)
- Nav dots: fixed right, one per `.slide`, click to smooth scroll
- Active dot tracks current slide (threshold 0.5)
