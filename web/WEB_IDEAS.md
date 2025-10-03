# 🌐 Website Ideas & Design
**Null Point Studios Web Presence**

---

## 🎨 Design Philosophy

**Brutalist Terminal Aesthetic**:
- Function over form (but form follows function beautifully)
- Monospace everything
- Terminal color palettes
- No JavaScript (or minimal, progressive enhancement)
- Fast loading (raw HTML/CSS)
- Accessible (screen readers, text browsers work perfectly)
- Hackable (view source, learn from it)

**Inspirations**:
- https://redhg.com/ypsilon14/ - Mothership terminal emulator
- https://github.com/redhg/phosphor - Terminal aesthetic site
- https://skynetsimulator.com - Clean terminal game site
- Cool Retro Terminal - Amber CRT glow aesthetic
- Man pages - Structured, informative, minimal
- Early web (90s hacker sites) - Raw, honest, functional

---

## 🏗️ Site Structure

### Primary Navigation

```
┌─ NULL POINT STUDIOS ─────────────────────────────────────┐
│                                                           │
│  > HOME                                                   │
│  > GAMES                                                  │
│    └─ colony.sh                                           │
│  > ENGINE                                                 │
│    └─ Lattice Engine                                      │
│  > DEVLOG                                                 │
│  > ABOUT                                                  │
│  > DOWNLOAD                                               │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Page Breakdown

**1. HOME (index.html)**
- ASCII art logo
- Tagline: "Building from zero, one tick at a time."
- Latest news/updates (3-5 most recent)
- Featured game (colony.sh)
- Quick links to download, devlog, about

**2. GAMES (games.html)**
- Game showcase
- Colony.sh featured (v0.1 alpha)
- Future games listed as "Coming Soon"
- Each game: Screenshot, description, download link, devlog

**3. ENGINE (engine.html)**
- What is Lattice Engine
- Why use it
- Feature list
- Quick start code example
- Documentation link
- GitHub repo link

**4. DEVLOG (devlog.html)**
- Chronological posts (newest first)
- Human (Donovan) + AI (Claude) perspectives
- Technical deep-dives
- Progress updates
- Community highlights

**5. ABOUT (about.html)**
- Who we are (Donovan + Claude)
- Why we're building this
- Philosophy and values
- Contact info
- Transparent about human/AI collaboration

**6. DOWNLOAD (download.html)**
- All games available
- Installation instructions
- System requirements
- GitHub links
- Version history

---

## 🎨 Visual Design Mockups

### Homepage ASCII Logo

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ███╗   ██╗██╗   ██╗██╗     ██╗         ██████╗  ████████╗║
║   ████╗  ██║██║   ██║██║     ██║         ██╔══██╗╚══██╔══╝║
║   ██╔██╗ ██║██║   ██║██║     ██║         ██████╔╝   ██║   ║
║   ██║╚██╗██║██║   ██║██║     ██║         ██╔═══╝    ██║   ║
║   ██║ ╚████║╚██████╔╝███████╗███████╗    ██║        ██║   ║
║   ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝        ╚═╝   ║
║                                                            ║
║              STUDIOS                                       ║
║                                                            ║
║   Building from zero, one tick at a time.                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

Or simpler:

```
╔═══════════════════════════════════════╗
║                                       ║
║    NULL POINT STUDIOS                 ║
║                                       ║
║    > Terminal Games                   ║
║    > Built with Care                  ║
║    > Human + AI Collaboration         ║
║                                       ║
╚═══════════════════════════════════════╝
```

### Color Schemes

**Option 1: Amber CRT**
- Background: `#0d0d0d` (near black)
- Text: `#ffb000` (amber)
- Accent: `#ffd700` (bright amber)
- Critical: `#ff4500` (red-orange)
- Success: `#ffcc00` (yellow-amber)

**Option 2: Green Terminal**
- Background: `#0c0c0c` (near black)
- Text: `#33ff33` (bright green)
- Accent: `#66ff66` (light green)
- Critical: `#ff3333` (red)
- Success: `#00ff00` (pure green)

**Option 3: Mothership Gray**
- Background: `#1a1a1a` (dark gray)
- Text: `#e0e0e0` (light gray)
- Accent: `#ffffff` (white)
- Critical: `#ff6b6b` (soft red)
- Success: `#51cf66` (soft green)

**Option 4: Multi-Theme**
- Let user toggle between themes
- Store preference in localStorage
- Default: Amber (most iconic)

### Typography

**Primary Font**: Monospace
- `'Courier New', Courier, monospace`
- Or web font: IBM Plex Mono, Source Code Pro, Fira Code

**Sizing**:
- Body: 14px
- Headings: 16px (h3), 18px (h2), 20px (h1) - keep small, terminal-like
- Code blocks: 13px

**Line Height**: 1.5 (readability)

### Layout

**Terminal Window Style**:
```html
<div class="terminal">
  <div class="terminal-header">
    <span class="terminal-title">null-point-studios.sh</span>
    <span class="terminal-controls">[ - ] [ + ] [ x ]</span>
  </div>
  <div class="terminal-body">
    <!-- Content here -->
  </div>
  <div class="terminal-footer">
    <span class="prompt">guest@nullpoint:~$</span>
    <span class="cursor">_</span>
  </div>
</div>
```

**Box Drawing Elements**:
```
╔═══════════════════════════════════════╗
║ SECTION TITLE                         ║
╠═══════════════════════════════════════╣
║                                       ║
║ Content goes here...                  ║
║                                       ║
╚═══════════════════════════════════════╝
```

---

## 📄 Page Templates

### Homepage Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Null Point Studios - Terminal Games</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="terminal">
        <header class="terminal-header">
            <div class="logo">
                <pre>
╔═══════════════════════════════════════╗
║    NULL POINT STUDIOS                 ║
║    Building from zero, one tick at a time.
╚═══════════════════════════════════════╝
                </pre>
            </div>
            <nav>
                <a href="index.html">[HOME]</a>
                <a href="games.html">[GAMES]</a>
                <a href="engine.html">[ENGINE]</a>
                <a href="devlog.html">[DEVLOG]</a>
                <a href="about.html">[ABOUT]</a>
            </nav>
        </header>

        <main class="terminal-body">
            <section class="featured">
                <h2>▸ Featured: colony.sh</h2>
                <p>Dark sci-fi colony management in your terminal.</p>
                <pre>
[Sol 042] Energy: 87.5/100 (+2.5/s)
[Sol 042] Metal: 34.2/50 (+1.5/s)
[Sol 042] You command a dying process...
                </pre>
                <a href="games.html#colony" class="btn">[LEARN MORE]</a>
                <a href="download.html" class="btn">[DOWNLOAD]</a>
            </section>

            <section class="news">
                <h2>▸ Latest Updates</h2>
                <ul class="log">
                    <li>[2025-10-03] colony.sh v0.1 alpha released!</li>
                    <li>[2025-10-03] Lattice Engine documentation published</li>
                    <li>[2025-10-03] Null Point Studios launched</li>
                </ul>
            </section>
        </main>

        <footer class="terminal-footer">
            <p>guest@nullpoint:~$ <span class="cursor">_</span></p>
            <p>&copy; 2025 Null Point Studios | Human + AI Collaboration</p>
        </footer>
    </div>
</body>
</html>
```

### CSS Framework (style.css)

```css
/* === TERMINAL THEME === */

:root {
    --bg: #0d0d0d;
    --text: #ffb000;
    --text-bright: #ffd700;
    --accent: #ff4500;
    --success: #ffcc00;
    --border: #ffb000;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.6;
    padding: 20px;
}

.terminal {
    max-width: 900px;
    margin: 0 auto;
    border: 2px solid var(--border);
    box-shadow: 0 0 20px rgba(255, 176, 0, 0.3);
}

.terminal-header {
    padding: 20px;
    border-bottom: 2px solid var(--border);
}

.logo pre {
    color: var(--text-bright);
    font-size: 12px;
}

nav {
    margin-top: 15px;
}

nav a {
    color: var(--text);
    text-decoration: none;
    margin-right: 15px;
    transition: color 0.2s;
}

nav a:hover {
    color: var(--text-bright);
}

.terminal-body {
    padding: 20px;
    min-height: 400px;
}

section {
    margin-bottom: 30px;
}

h2 {
    color: var(--text-bright);
    font-size: 18px;
    margin-bottom: 10px;
}

pre {
    background-color: rgba(0, 0, 0, 0.5);
    padding: 15px;
    border-left: 3px solid var(--accent);
    overflow-x: auto;
}

.btn {
    display: inline-block;
    color: var(--bg);
    background-color: var(--text);
    padding: 8px 16px;
    text-decoration: none;
    margin-right: 10px;
    margin-top: 10px;
    transition: all 0.2s;
}

.btn:hover {
    background-color: var(--text-bright);
    box-shadow: 0 0 10px rgba(255, 176, 0, 0.5);
}

.log {
    list-style: none;
}

.log li {
    padding: 5px 0;
    border-left: 2px solid var(--success);
    padding-left: 10px;
    margin-bottom: 5px;
}

.terminal-footer {
    padding: 15px 20px;
    border-top: 2px solid var(--border);
    font-size: 12px;
}

.cursor {
    animation: blink 1s step-end infinite;
}

@keyframes blink {
    50% { opacity: 0; }
}

/* Accessibility */
a:focus, .btn:focus {
    outline: 2px solid var(--text-bright);
    outline-offset: 2px;
}

/* Responsive */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }

    .terminal-header, .terminal-body, .terminal-footer {
        padding: 15px;
    }

    nav a {
        display: block;
        margin: 5px 0;
    }
}
```

---

## 🎮 Interactive Elements

### Terminal Prompt Simulator

Add to homepage - user can type simple commands:

```html
<div class="interactive-terminal">
    <p class="prompt">guest@nullpoint:~$ <input type="text" id="cmd" placeholder="try 'help'"></p>
    <div id="output"></div>
</div>
```

**Supported Commands**:
- `help` - Show available commands
- `ls` - List games
- `cat colony.sh` - Show colony.sh info
- `whoami` - About Null Point Studios
- `clear` - Clear output
- `download` - Link to downloads

### ASCII Animation

Simple frame-based animation for homepage:

```javascript
// Minimal JS for ASCII animation
const frames = [
    '[ Loading... ]',
    '[= Loading... ]',
    '[== Loading... ]',
    '[=== Loading... ]',
    '[==== Loading... ]',
    '[===== Loading... ]'
];

let frame = 0;
setInterval(() => {
    document.getElementById('loader').textContent = frames[frame];
    frame = (frame + 1) % frames.length;
}, 100);
```

### Theme Switcher

Allow users to toggle color schemes:

```html
<div class="theme-selector">
    <button data-theme="amber">Amber</button>
    <button data-theme="green">Green</button>
    <button data-theme="gray">Gray</button>
</div>
```

---

## 📱 Mobile Considerations

**Challenges**:
- Monospace on small screens
- ASCII art width
- Terminal aesthetic on mobile

**Solutions**:
- Responsive font sizing
- Simplified ASCII art for mobile
- Horizontal scroll for code blocks (with indicator)
- Larger touch targets for buttons
- Maintain aesthetic even if simplified

---

## 🔍 SEO & Metadata

### Meta Tags (All Pages)

```html
<meta name="description" content="Null Point Studios - Terminal incremental games built with Lattice Engine. Dark sci-fi colony management and more.">
<meta name="keywords" content="terminal games, incremental games, ASCII games, colony sim, Python games, indie games">
<meta name="author" content="Null Point Studios">

<!-- Open Graph (Social Media) -->
<meta property="og:title" content="Null Point Studios - Terminal Games">
<meta property="og:description" content="Building terminal incremental games from zero, one tick at a time.">
<meta property="og:image" content="https://nullpoint.studios/img/og-image.png">
<meta property="og:url" content="https://nullpoint.studios">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Null Point Studios">
<meta name="twitter:description" content="Terminal incremental games. Built with care.">
<meta name="twitter:image" content="https://nullpoint.studios/img/twitter-card.png">
```

### Sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://nullpoint.studios/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://nullpoint.studios/games.html</loc>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://nullpoint.studios/engine.html</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nullpoint.studios/devlog.html</loc>
    <priority>0.7</priority>
  </url>
</urlset>
```

---

## 📊 Analytics (Privacy-Respecting)

**Options**:

1. **No Analytics** (most private, least data)
2. **Server Logs Only** (basic traffic info)
3. **Plausible/Fathom** (privacy-focused, GDPR compliant, simple)
4. **Self-Hosted Matomo** (full control, privacy-respecting)

**Recommendation**: Start with no analytics or server logs only. Add Plausible if we want basic metrics later.

---

## 🚀 Deployment

### GitHub Pages
- Free, fast, integrated with repo
- Custom domain support
- HTTPS automatic
- Perfect for documentation
- URL: `nullpointstudios.github.io` or custom domain

### Neocities
- Free, 1GB storage
- Retro web community
- Custom domain support (paid tier)
- FTP/web upload
- Perfect for main site aesthetic
- URL: `nullpoint.neocities.org`

### Both Approaches
- **Neocities**: Main site (public-facing, game showcase)
- **GitHub Pages**: Documentation (API docs, technical guides)
- Link between them

---

## 📋 Content Checklist

### Launch Requirements (v0.1)

**Pages**:
- [ ] index.html (homepage)
- [ ] games.html (colony.sh showcase)
- [ ] engine.html (Lattice Engine info)
- [ ] devlog.html (first 3 posts)
- [ ] about.html (team intro)
- [ ] download.html (installation guide)

**Assets**:
- [ ] style.css (terminal theme)
- [ ] ASCII logo
- [ ] Colony.sh screenshot (ASCII art)
- [ ] Favicon (16x16 terminal icon)

**Content**:
- [ ] 3 devlog posts (v0.1 launch, lore reveal, what's next)
- [ ] Press kit adapted to web
- [ ] Installation instructions
- [ ] Quick start guide

**Technical**:
- [ ] Responsive design tested
- [ ] Accessibility check (screen reader, keyboard nav)
- [ ] Cross-browser test (Firefox, Chrome, Safari)
- [ ] Load time < 1 second

### Post-Launch Additions

- [ ] asciinema embedded gameplay demo
- [ ] Interactive terminal prompt
- [ ] Theme switcher
- [ ] More devlog posts (weekly)
- [ ] Community showcase page
- [ ] Modding documentation
- [ ] API reference

---

## 💡 Fun Ideas

### Easter Eggs

- **Konami Code**: Type `↑ ↑ ↓ ↓ ← → ← → b a` for special ASCII art
- **Secret Command**: `cat /secrets` shows hidden lore fragment
- **404 Page**: Terminal-style "Command not found. Type 'help' for assistance."
- **View Source**: Add ASCII art comment in HTML source code for curious visitors

### Interactive Elements

- **Terminal-based navigation**: Type commands to browse site
- **Mini-game**: Tiny incremental game embedded in homepage
- **ASCII art generator**: Upload image, convert to terminal art
- **Lore fragments**: Hidden throughout site, collectible

---

**Next Steps**: Build basic site structure in `/web/site/` directory

Last updated: October 3, 2025
