#!/usr/bin/env python3
"""Generate all 4 carousel sets — one per theme. Each slide = 1080x1080 PNG."""

import asyncio
import os

# ═══════════════════════════════════════════════════
# CAROUSEL 1: SKETCH PAD — React Re-Renders
# ═══════════════════════════════════════════════════
SKETCH_SLIDES = [
    # Slide 1: Hook
    """
    <div class="slide sketch">
      <div class="sticker">save this one</div>
      <h1>How does <u>React re-rendering</u> actually work?</h1>
      <p class="sub">Nobody explains this simply.<br>So I drew it out. →</p>
      <div class="arrow">↓</div>
      <div class="doodle-box">
        <p>3 things trigger a re-render:</p>
        <p>1. State changes ← <span class="orange">most common</span></p>
        <p>2. Props change</p>
        <p>3. Parent re-renders ← <span class="red">the sneaky one</span></p>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    # Slide 2
    """
    <div class="slide sketch">
      <div class="slide-num">2 / 6</div>
      <h2>So what's a "re-render"?</h2>
      <div class="doodle-box" style="margin-top:30px;">
        <p>Think of it like this:</p>
        <p class="big">React takes a <span class="orange">snapshot</span> of your UI.</p>
        <p>Every time something changes, it takes a NEW snapshot and compares it to the old one.</p>
        <p style="margin-top:20px;">If they're different → update the screen.<br>If they're the same → do nothing.</p>
      </div>
      <p class="note">↑ That comparison is called "reconciliation" — fancy word for "spot the difference"</p>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    # Slide 3
    """
    <div class="slide sketch">
      <div class="slide-num">3 / 6</div>
      <h2>The sneaky one: <span class="red">Parent re-renders</span></h2>
      <div class="tree">
        <div class="tree-node parent">App (state changed)</div>
        <div class="tree-arrow">↓ re-renders ↓</div>
        <div class="tree-row">
          <div class="tree-node child">Header</div>
          <div class="tree-node child">Content</div>
          <div class="tree-node child">Footer</div>
        </div>
        <p class="tree-label red">ALL children re-render even if their props didn't change</p>
      </div>
      <div class="callout">
        <p>This is the #1 performance killer in React apps.</p>
        <p>Most devs don't even know it's happening.</p>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    # Slide 4
    """
    <div class="slide sketch">
      <div class="slide-num">4 / 6</div>
      <h2>The fix: <span class="teal">React.memo()</span></h2>
      <div class="code-note">
        <pre>const ExpensiveList = React.memo(
  ({ items }) => {
    return items.map(item =>
      &lt;Item key={item.id} {...item} /&gt;
    )
  }
)</pre>
      </div>
      <div class="doodle-box" style="margin-top:20px;">
        <p>What this does:</p>
        <p>→ Wraps your component in a "shield"</p>
        <p>→ Only re-renders when props <span class="orange">actually change</span></p>
        <p>→ Skips unnecessary work</p>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    # Slide 5
    """
    <div class="slide sketch">
      <div class="slide-num">5 / 6</div>
      <h2>But don't memo <span class="red">everything</span></h2>
      <div class="two-col">
        <div class="col-yes">
          <p class="col-title teal">✓ USE memo when:</p>
          <p>• Heavy lists / tables</p>
          <p>• Charts & visualizations</p>
          <p>• Re-renders often with same props</p>
          <p>• You MEASURED the problem</p>
        </div>
        <div class="col-no">
          <p class="col-title red">✗ DON'T memo:</p>
          <p>• Simple buttons / text</p>
          <p>• Small components</p>
          <p>• Things that change every render</p>
          <p>• "Just in case"</p>
        </div>
      </div>
      <p class="note">Premature optimization = wasted time. Measure first.</p>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    # Slide 6: CTA
    """
    <div class="slide sketch">
      <div class="slide-num">6 / 6</div>
      <h1 style="font-size:58px;">Quick recap:</h1>
      <div class="doodle-box" style="margin-top:20px;">
        <p>1. Re-renders happen on state, props, or parent change</p>
        <p>2. Parent re-renders = ALL children re-render</p>
        <p>3. React.memo() stops unnecessary re-renders</p>
        <p>4. Only memo expensive components</p>
        <p>5. Always measure before optimizing</p>
      </div>
      <p class="cta-text">Save this for next time your app feels slow.</p>
      <p class="cta-follow">Follow <span class="orange">@itisdrey</span> for more breakdowns</p>
      <div class="handle">@itisdrey</div>
    </div>
    """,
]

# ═══════════════════════════════════════════════════
# CAROUSEL 2: DARK MODE — 3 React Bugs
# ═══════════════════════════════════════════════════
DARK_SLIDES = [
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>
      <h1>3 React Bugs You're <span class="red">Shipping Right Now</span></h1>
      <p class="sub">And you don't even know it.</p>
      <div class="tags"><span class="tag-red">React</span><span class="tag-teal">Debugging</span><span class="tag-red">Production</span></div>
      <div class="code-block"><span class="comment">// Bug #1: Missing dependency</span><br><span class="keyword">useEffect</span>(() =&gt; {<br>&nbsp;&nbsp;fetchUser(<span class="str">userId</span>);<br>}, []);  <span class="comment">// ← userId is MISSING</span></div>
    </div>
    """,
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>
      <h2>Bug #1: <span class="red">Missing useEffect Dependency</span></h2>
      <div class="code-block"><span class="comment">// BROKEN: When userId changes, effect won't re-run</span><br><span class="keyword">useEffect</span>(() =&gt; {<br>&nbsp;&nbsp;fetchUser(userId);<br>}, []);  <span class="comment">// ← empty array = runs ONCE</span></div>
      <p class="explain">Your user changes their profile.<br>The component still shows the OLD user's data.<br>Silently. No error. Just wrong.</p>
      <div class="code-block good"><span class="comment">// FIXED:</span><br><span class="keyword">useEffect</span>(() =&gt; {<br>&nbsp;&nbsp;fetchUser(userId);<br>}, [<span class="green">userId</span>]);  <span class="comment">// ← now it re-runs</span></div>
    </div>
    """,
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>
      <h2>Bug #2: <span class="red">The setState Trap</span></h2>
      <div class="code-block"><span class="comment">// BROKEN: Only increments by 1, not 2</span><br>setCount(count + 1);<br>setCount(count + 1);<br><span class="comment">// Both see the SAME count value</span></div>
      <p class="explain">React batches state updates.<br>Both calls read the same stale value.</p>
      <div class="code-block good"><span class="comment">// FIXED: Use functional form</span><br>setCount(<span class="green">prev =&gt; prev + 1</span>);<br>setCount(<span class="green">prev =&gt; prev + 1</span>);<br><span class="comment">// Each gets the LATEST value</span></div>
    </div>
    """,
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>
      <h2>Bug #3: <span class="red">The Sneaky Zero</span></h2>
      <div class="code-block"><span class="comment">// BROKEN: Renders literal "0" on screen</span><br>{count <span class="red">&amp;&amp;</span> &lt;Text&gt;{count} clicks&lt;/Text&gt;}<br><br><span class="comment">// When count is 0, JS sees it as falsy</span><br><span class="comment">// But React renders 0 as text!</span></div>
      <p class="explain">Your UI randomly shows "0" and you have no idea why.</p>
      <div class="code-block good"><span class="comment">// FIXED: Explicit comparison</span><br>{count <span class="green">&gt; 0</span> &amp;&amp; &lt;Text&gt;{count} clicks&lt;/Text&gt;}</div>
    </div>
    """,
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span></div></div>
      <h2>The Rule for Each Bug</h2>
      <div class="rule-list">
        <div class="rule"><span class="num red">1</span><div><p class="rule-title">Missing Dependency</p><p class="rule-text">If you USE it in the effect, it goes in the dependency array. Period.</p></div></div>
        <div class="rule"><span class="num red">2</span><div><p class="rule-title">setState Batching</p><p class="rule-text">When new state depends on old state, always use the functional form: prev =&gt; ...</p></div></div>
        <div class="rule"><span class="num red">3</span><div><p class="rule-title">Falsy Rendering</p><p class="rule-text">Never use &amp;&amp; with numbers. Use explicit comparison: count &gt; 0</p></div></div>
      </div>
    </div>
    """,
    """
    <div class="slide dark">
      <div class="top-bar"><span class="tag-handle">@itisdrey</span><div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span></div></div>
      <div class="center-content">
        <h1 style="font-size:48px;">Almost everyone ships at least one of these to production.</h1>
        <p class="sub" style="margin-top:30px;font-size:26px;">Now you know what to look for.</p>
        <div class="cta-box">
          <p>Save this → check your code → tag a dev who needs it</p>
          <p class="follow-text">Follow <span class="red">@itisdrey</span> for more</p>
        </div>
      </div>
    </div>
    """,
]

# ═══════════════════════════════════════════════════
# CAROUSEL 3: CLEAN SHEET — Star Rating Interview
# ═══════════════════════════════════════════════════
CLEAN_SLIDES = [
    """
    <div class="slide clean">
      <div class="dots"><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="badge">INTERVIEW CHALLENGE</div>
      <div class="quote">&ldquo;</div>
      <h1>Build a star rating component.</h1>
      <p class="sub">Sounds easy. It's not.<br><br>Most candidates stop at <span class="blue">Level 2</span>.<br>Getting to <span class="blue">Level 4</span> is what separates mid from senior.<br><br>Here are all 5 levels. →</p>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="level-badge l1">LEVEL 1</div>
      <h2>The Basics <span class="gray">(Junior — 5 min)</span></h2>
      <p class="sub" style="margin-bottom:20px;">Click a star → fill it + all stars before it.</p>
      <div class="code-clean"><pre>const StarRating = () =&gt; {
  const [rating, setRating] = useState(0);

  return (
    &lt;div&gt;
      {[1,2,3,4,5].map(star =&gt; (
        &lt;Star
          key={star}
          filled={star &lt;= rating}
          onClick={() =&gt; setRating(star)}
        /&gt;
      ))}
    &lt;/div&gt;
  );
};</pre></div>
      <p class="verdict">This gets you in the door. That's it.</p>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="level-badge l2">LEVEL 2</div>
      <h2>Hover Preview <span class="gray">(Mid)</span></h2>
      <p class="sub">Show a preview when hovering before clicking.</p>
      <div class="key-points">
        <div class="kp"><span class="blue-dot"></span>Separate <strong>hover state</strong> vs <strong>committed value</strong></div>
        <div class="kp"><span class="blue-dot"></span>onMouseEnter on each star updates preview</div>
        <div class="kp"><span class="blue-dot"></span>onMouseLeave resets to committed value</div>
        <div class="kp"><span class="blue-dot"></span>Handle leave on stars AND container separately</div>
      </div>
      <div class="warning-box">Most candidates stop here. Don't be most candidates.</div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="level-badge l3">LEVEL 3</div>
      <h2>Edge Cases <span class="gray">(Senior)</span></h2>
      <p class="sub">Interviewers add these MID-INTERVIEW to test adaptability.</p>
      <div class="code-clean"><pre>// Reset on double-click
onClick={() =&gt;
  setRating(star === rating ? 0 : star)
}

// Configurable max stars
{Array.from({ length: maxStars },
  (_, i) =&gt; i + 1).map(star =&gt; ...)
}

// Read-only mode
if (readOnly) return; // block interaction</pre></div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="level-badge l4">LEVEL 4</div>
      <h2>Accessibility <span class="gray">(Staff / Principal)</span></h2>
      <p class="sub">THIS is what separates mid from senior.</p>
      <div class="code-clean"><pre>&lt;div role="radiogroup" aria-label="Rating"&gt;
  &lt;span
    role="radio"
    aria-checked={star === rating}
    aria-label={`${star} of ${maxStars}`}
    tabIndex={star === 1 ? 0 : -1}
    onKeyDown={handleKeyDown}
  /&gt;
&lt;/div&gt;</pre></div>
      <div class="key-points" style="margin-top:15px;">
        <div class="kp"><span class="blue-dot"></span>Arrow keys to navigate between stars</div>
        <div class="kp"><span class="blue-dot"></span>Enter / Space to select</div>
        <div class="kp"><span class="blue-dot"></span>Visible focus indicator (outline, not just color)</div>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span></div>
      <div class="level-badge l5">LEVEL 5</div>
      <h2>Communication <span class="gray">(Distinguished)</span></h2>
      <p class="sub">The code is 50%. How you THINK is the other 50%.</p>
      <div class="key-points">
        <div class="kp"><span class="blue-dot"></span>Ask clarifying questions BEFORE building</div>
        <div class="kp"><span class="blue-dot"></span>Explain your data structure choices out loud</div>
        <div class="kp"><span class="blue-dot"></span>Use named CSS variables for styling</div>
        <div class="kp"><span class="blue-dot"></span>Treat it as a collaborative design conversation</div>
      </div>
      <div class="score-table">
        <div class="score-row header"><span>Level</span><span>Skill</span><span>Seniority</span></div>
        <div class="score-row"><span>1</span><span>Basics</span><span>Junior</span></div>
        <div class="score-row"><span>2</span><span>Hover</span><span>Mid</span></div>
        <div class="score-row"><span>3</span><span>Edge Cases</span><span>Senior</span></div>
        <div class="score-row"><span>4</span><span>A11y</span><span>Staff+</span></div>
        <div class="score-row"><span>5</span><span>Communication</span><span>Distinguished</span></div>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide clean">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span></div>
      <div class="center-cta">
        <h1 style="font-size:44px;">Next time an interviewer says<br>"build a star rating"...</h1>
        <p class="sub" style="font-size:26px;margin-top:20px;">...go past Level 2.</p>
        <p class="sub" style="font-size:22px;margin-top:40px;">Save this for your next interview prep session.</p>
        <p class="follow-clean">Follow <span class="blue">@itisdrey</span></p>
      </div>
      <div class="handle">@itisdrey</div>
    </div>
    """,
]

# ═══════════════════════════════════════════════════
# CAROUSEL 4: GRADIENT WAVE — AI Making Devs Worse
# ═══════════════════════════════════════════════════
GRADIENT_SLIDES = [
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="glass-card">
        <h1>AI is making developers <span class="gold">17% worse.</span></h1>
        <p class="sub-g">Here's the study. And the 2-minute fix.</p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="glass-card">
        <h2 style="color:#FFD700;font-size:28px;margin-bottom:20px;">THE STUDY</h2>
        <h1 style="font-size:42px;">Anthropic ran the largest study ever on AI coding tools.</h1>
        <p class="sub-g" style="margin-top:20px;">Devs WITH AI assistants scored<br><span style="font-size:60px;font-weight:900;color:#FFD700;">17% lower</span><br>on independent skill tests.</p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="glass-card">
        <h2 style="font-size:36px;">It gets worse.</h2>
        <p class="sub-g" style="font-size:28px;margin-top:20px;">AI didn't even make them faster.</p>
        <p class="sub-g" style="font-size:24px;margin-top:20px;opacity:0.8;">25% of coding time was spent reviewing and fixing AI suggestions.</p>
        <p class="sub-g" style="font-size:32px;margin-top:30px;color:#FFD700;">Slower AND less skilled.</p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="glass-card" style="text-align:left;">
        <h2 style="font-size:32px;margin-bottom:25px;">Two modes emerged:</h2>
        <div style="background:rgba(255,59,59,0.2);padding:20px;border-radius:12px;margin-bottom:15px;">
          <p style="color:#ff6b6b;font-size:22px;font-weight:700;">DELEGATION MODE</p>
          <p style="color:#fff;font-size:20px;">"Just accept whatever AI gives me"</p>
          <p style="color:#FFD700;font-size:28px;font-weight:900;margin-top:8px;">Mastery → 65%</p>
        </div>
        <div style="background:rgba(78,205,196,0.2);padding:20px;border-radius:12px;">
          <p style="color:#4ECDC4;font-size:22px;font-weight:700;">INQUIRY MODE</p>
          <p style="color:#fff;font-size:20px;">"Why does this work? Let me understand."</p>
          <p style="color:#FFD700;font-size:28px;font-weight:900;margin-top:8px;">Mastery → 85%</p>
        </div>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="glass-card">
        <h2 style="font-size:32px;color:#FFD700;">The fix is embarrassingly simple:</h2>
        <p class="sub-g" style="font-size:40px;margin-top:25px;font-weight:900;">Spend 2-3 extra minutes asking<br>"WHY does this code work?"</p>
        <p class="sub-g" style="font-size:24px;margin-top:25px;opacity:0.8;">That nearly DOUBLED test scores.</p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span><span class="dot"></span></div>
      <div class="glass-card">
        <h2 style="font-size:28px;opacity:0.7;margin-bottom:15px;">My take:</h2>
        <h1 style="font-size:40px;">AI isn't making devs worse.<br><span class="gold">Laziness is.</span></h1>
        <p class="sub-g" style="font-size:22px;margin-top:20px;">AI is a power tool.<br><br>Hand it to someone who understands the craft? <span style="color:#4ECDC4;">Dangerous.</span><br><br>Hand it to someone who just wants the answer? <span style="color:#ff6b6b;">They'll lose the craft entirely.</span></p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
    """
    <div class="slide gradient">
      <div class="dots-g"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot active"></span></div>
      <div class="glass-card">
        <h1 style="font-size:38px;">Use AI.<br>But understand what it gives you.</h1>
        <p class="sub-g" style="font-size:26px;margin-top:25px;">That's the difference between a <span class="gold">developer</span> and a <span style="color:#ff6b6b;">prompt jockey.</span></p>
        <p class="sub-g" style="font-size:22px;margin-top:35px;opacity:0.7;">Save this. Tag a dev who needs to hear it.</p>
        <p style="color:#FFD700;font-size:28px;font-weight:900;margin-top:20px;">Follow @itisdrey</p>
      </div>
      <div class="handle-g">@itisdrey</div>
    </div>
    """,
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Caveat:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
.slide { width:1080px; height:1080px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; }

/* ── SKETCH ── */
.slide.sketch { background:#FFF9F0; background-image:radial-gradient(circle,#ddd 1px,transparent 1px); background-size:24px 24px; font-family:'Caveat',cursive; padding:60px; }
.sketch h1 { font-size:64px; color:#2D2D2D; line-height:1.15; transform:rotate(-0.5deg); }
.sketch h2 { font-size:48px; color:#2D2D2D; line-height:1.2; }
.sketch u { text-decoration-color:#FF6B35; text-decoration-thickness:4px; text-underline-offset:8px; }
.sketch .sub { font-size:34px; color:#555; margin-top:15px; }
.sketch .arrow { color:#FF6B35; font-size:42px; margin:10px 0; text-align:center; }
.sketch .doodle-box { border:3px dashed #4ECDC4; border-radius:12px; padding:25px 30px; background:rgba(255,255,255,0.6); transform:rotate(0.3deg); }
.sketch .doodle-box p { font-size:30px; color:#2D2D2D; line-height:1.5; }
.sketch .orange { color:#FF6B35; font-style:italic; }
.sketch .red { color:#FF3B3B; font-style:italic; }
.sketch .teal { color:#4ECDC4; }
.sketch .handle { position:absolute; bottom:35px; right:45px; font-size:26px; color:#999; }
.sketch .sticker { position:absolute; top:35px; right:40px; background:#FFD700; color:#2D2D2D; padding:10px 20px; font-size:22px; transform:rotate(3deg); border-radius:4px; box-shadow:2px 2px 0 rgba(0,0,0,0.1); }
.sketch .slide-num { position:absolute; top:35px; left:45px; font-size:22px; color:#999; font-family:'Inter',sans-serif; }
.sketch .note { font-size:24px; color:#888; margin-top:15px; font-style:italic; }
.sketch .big { font-size:36px; font-weight:700; margin:10px 0; }
.sketch .tree { text-align:center; margin:20px 0; }
.sketch .tree-node { display:inline-block; padding:15px 25px; border:3px solid #2D2D2D; border-radius:10px; font-size:24px; margin:5px 10px; }
.sketch .tree-node.parent { background:#FFE0B2; }
.sketch .tree-node.child { background:#E3F2FD; }
.sketch .tree-arrow { font-size:28px; color:#FF6B35; margin:8px 0; }
.sketch .tree-row { display:flex; justify-content:center; gap:15px; }
.sketch .tree-label { font-size:26px; margin-top:15px; }
.sketch .callout { background:rgba(255,59,59,0.1); border-left:4px solid #FF3B3B; padding:15px 20px; margin-top:20px; border-radius:0 8px 8px 0; }
.sketch .callout p { font-size:26px; color:#2D2D2D; }
.sketch .code-note { background:#2D2D2D; border-radius:12px; padding:25px; margin-top:15px; transform:rotate(-0.3deg); border:3px solid #4ECDC4; }
.sketch .code-note pre { font-family:'JetBrains Mono',monospace; font-size:22px; color:#e0e0e0; line-height:1.5; white-space:pre-wrap; }
.sketch .two-col { display:flex; gap:20px; margin-top:15px; }
.sketch .col-yes, .sketch .col-no { flex:1; padding:20px; border-radius:12px; }
.sketch .col-yes { border:3px solid #4ECDC4; background:rgba(78,205,196,0.05); }
.sketch .col-no { border:3px solid #FF3B3B; background:rgba(255,59,59,0.05); }
.sketch .col-title { font-size:28px; font-weight:700; margin-bottom:10px; }
.sketch .col-yes p, .sketch .col-no p { font-size:24px; line-height:1.6; }
.sketch .cta-text { font-size:30px; color:#555; margin-top:25px; }
.sketch .cta-follow { font-size:34px; color:#2D2D2D; margin-top:10px; font-weight:700; }

/* ── DARK ── */
.slide.dark { background:linear-gradient(180deg,#0D0D0D,#1A1A2E); padding:60px; color:#fff; }
.dark .top-bar { position:absolute; top:35px; left:45px; right:45px; display:flex; justify-content:space-between; align-items:center; }
.dark .tag-handle { color:rgba(255,255,255,0.5); font-size:18px; font-weight:700; }
.dark .dots { display:flex; gap:8px; }
.dark .dot { width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.2); }
.dark .dot.active { background:#FF3B3B; }
.dark h1 { font-size:54px; font-weight:900; line-height:1.15; margin-top:70px; }
.dark h2 { font-size:40px; font-weight:900; line-height:1.2; margin-top:70px; }
.dark .red { color:#FF3B3B; }
.dark .green { color:#4ECDC4; }
.dark .sub { color:#B0B0B0; font-size:24px; margin-top:15px; line-height:1.5; }
.dark .tags { display:flex; gap:12px; margin-top:25px; }
.dark .tag-red { background:rgba(255,59,59,0.15); color:#FF3B3B; padding:8px 18px; border-radius:8px; font-size:16px; font-weight:700; }
.dark .tag-teal { background:rgba(78,205,196,0.15); color:#4ECDC4; padding:8px 18px; border-radius:8px; font-size:16px; font-weight:700; }
.dark .code-block { background:#111; border:1px solid #333; border-radius:12px; padding:25px; margin-top:25px; font-family:'JetBrains Mono',monospace; font-size:20px; color:#e0e0e0; line-height:1.6; }
.dark .code-block.good { border-color:#4ECDC4; }
.dark .comment { color:#6272A4; }
.dark .keyword { color:#FF79C6; }
.dark .str { color:#F1FA8C; }
.dark .explain { color:#B0B0B0; font-size:22px; margin-top:20px; line-height:1.5; }
.dark .rule-list { margin-top:30px; }
.dark .rule { display:flex; gap:20px; align-items:flex-start; margin-bottom:25px; }
.dark .num { background:rgba(255,59,59,0.2); color:#FF3B3B; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:900; flex-shrink:0; }
.dark .rule-title { color:#fff; font-size:24px; font-weight:700; }
.dark .rule-text { color:#B0B0B0; font-size:20px; margin-top:5px; }
.dark .center-content { display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; height:100%; }
.dark .cta-box { margin-top:40px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:30px 40px; }
.dark .cta-box p { font-size:22px; color:#B0B0B0; }
.dark .follow-text { color:#FF3B3B; font-size:26px; font-weight:700; margin-top:10px; }

/* ── CLEAN ── */
.slide.clean { background:#fff; padding:60px; }
.clean .dots { position:absolute; top:35px; left:50%; transform:translateX(-50%); display:flex; gap:8px; }
.clean .dot { width:10px; height:10px; border-radius:50%; background:#ddd; }
.clean .dot.active { background:#2563EB; }
.clean .badge { display:inline-block; background:#EEF2FF; color:#2563EB; padding:8px 18px; border-radius:20px; font-size:16px; font-weight:700; margin-top:60px; }
.clean .quote { font-size:100px; color:#2563EB; font-family:Georgia,serif; line-height:0.5; margin:15px 0; }
.clean h1 { color:#1A1A1A; font-size:48px; font-weight:900; line-height:1.25; }
.clean h2 { color:#1A1A1A; font-size:38px; font-weight:900; line-height:1.25; margin-top:60px; }
.clean .sub { color:#666; font-size:22px; line-height:1.5; margin-top:10px; }
.clean .blue { color:#2563EB; font-weight:700; }
.clean .gray { color:#999; font-weight:400; font-size:28px; }
.clean .handle { position:absolute; bottom:35px; right:45px; color:#999; font-size:18px; font-weight:700; }
.clean .level-badge { display:inline-block; padding:8px 20px; border-radius:8px; font-size:18px; font-weight:900; color:#fff; margin-top:60px; margin-bottom:15px; }
.clean .l1 { background:#22C55E; }
.clean .l2 { background:#3B82F6; }
.clean .l3 { background:#F59E0B; }
.clean .l4 { background:#8B5CF6; }
.clean .l5 { background:#EC4899; }
.clean .code-clean { background:#F8F9FA; border:1px solid #E5E7EB; border-radius:12px; padding:20px; margin-top:15px; }
.clean .code-clean pre { font-family:'JetBrains Mono',monospace; font-size:18px; color:#1A1A1A; line-height:1.5; white-space:pre-wrap; }
.clean .verdict { color:#2563EB; font-size:20px; font-weight:700; margin-top:15px; }
.clean .key-points { margin-top:15px; }
.clean .kp { display:flex; align-items:center; gap:12px; font-size:22px; color:#333; margin-bottom:12px; line-height:1.4; }
.clean .blue-dot { width:10px; height:10px; border-radius:50%; background:#2563EB; flex-shrink:0; }
.clean .warning-box { background:#FEF3C7; border:1px solid #F59E0B; border-radius:10px; padding:15px 20px; margin-top:20px; font-size:20px; color:#92400E; font-weight:600; }
.clean .score-table { margin-top:20px; border:1px solid #E5E7EB; border-radius:10px; overflow:hidden; }
.clean .score-row { display:flex; padding:10px 20px; font-size:18px; }
.clean .score-row span { flex:1; }
.clean .score-row.header { background:#F8F9FA; font-weight:700; color:#666; }
.clean .score-row:nth-child(even) { background:#FAFAFA; }
.clean .center-cta { display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; height:100%; }
.clean .follow-clean { color:#2563EB; font-size:26px; font-weight:700; margin-top:30px; }

/* ── GRADIENT ── */
.slide.gradient { background:linear-gradient(135deg,#6C63FF,#00C9FF); padding:60px; text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center; }
.gradient .glass-card { background:rgba(255,255,255,0.12); backdrop-filter:blur(20px); border-radius:24px; padding:50px 45px; border:1px solid rgba(255,255,255,0.2); max-width:900px; width:100%; }
.gradient h1 { color:#fff; font-size:48px; font-weight:900; line-height:1.25; }
.gradient h2 { color:#fff; font-size:36px; font-weight:700; line-height:1.3; }
.gradient .gold { color:#FFD700; }
.gradient .sub-g { color:rgba(255,255,255,0.8); font-size:24px; margin-top:15px; line-height:1.5; }
.gradient .handle-g { position:absolute; bottom:35px; left:45px; color:rgba(255,255,255,0.5); font-size:20px; font-weight:700; }
.gradient .dots-g { position:absolute; top:35px; left:50%; transform:translateX(-50%); display:flex; gap:8px; }
.gradient .dots-g .dot { width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.3); }
.gradient .dots-g .dot.active { background:#fff; }
"""

HTML_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body style="margin:0;padding:0;">{slide}</body></html>"""

async def generate_all():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        configs = [
            ("sketch_pad", SKETCH_SLIDES, "React Re-Renders"),
            ("dark_mode", DARK_SLIDES, "3 React Bugs"),
            ("clean_sheet", CLEAN_SLIDES, "Star Rating Interview"),
            ("gradient_wave", GRADIENT_SLIDES, "AI Making Devs Worse"),
        ]

        for folder, slides, name in configs:
            print(f"\n--- Generating: {name} ({folder}) ---")
            for i, slide_html in enumerate(slides, 1):
                page = await browser.new_page(viewport={"width": 1080, "height": 1080})
                html = HTML_TEMPLATE.format(css=CSS, slide=slide_html)
                await page.set_content(html, wait_until="networkidle")
                await page.wait_for_timeout(1000)
                path = f"/tmp/carousel_output/{folder}/slide_{i:02d}.png"
                await page.locator(".slide").screenshot(path=path)
                await page.close()
                print(f"  slide {i}/{len(slides)}")

        await browser.close()

    print("\n=== ALL DONE ===")
    for folder, slides, name in configs:
        print(f"  {name}: /tmp/carousel_output/{folder}/ ({len(slides)} slides)")

asyncio.run(generate_all())
