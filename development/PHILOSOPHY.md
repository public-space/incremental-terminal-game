# Development Philosophy

**Version Stamp:** `[v0.1-v0.2 - 2025-10-03]`

---

## 🌌 Null Point Studios

### Vision
**Tagline:** *"if you want to play a good RPG you're going to have to make it yourself"* - Vince D. Weller

Null Point Studios embraces the philosophy of creating experiences that don't exist elsewhere. We build games that blend:
- Deep, atmospheric storytelling
- Meaningful player agency
- Terminal/retro aesthetics with modern design
- Systems that respect player intelligence

### Core Principles

**1. Atmosphere Over Graphics**
- ASCII and terminal interfaces create unique immersion
- Color palettes set mood and tone
- Minimalism forces imagination

**2. Depth Without Bloat**
- Every system serves gameplay
- Complexity emerges from simple rules
- No features for features' sake

**3. Player Respect**
- No hand-holding, but clear feedback
- Save systems that work
- Information accessible when needed
- Let players discover, don't force tutorials

**4. Incremental Polish**
- Fix what's broken before adding new
- Test thoroughly at each stage
- Version control isn't just for code - it's for ideas

**5. Developer Joy**
- Build tools that make development pleasant
- Debug systems that help, not obscure
- Documentation that teaches

---

## ⚙️ Lattice Engine

### What Is It?
A terminal-based game engine for incremental/idle games with roguelike aesthetics. Built in Python for maximum readability and extensibility.

### Design Philosophy

**Modular Architecture**
```
Every aspect and function should be in its own python file
for maximum organization, modularability, and readable clean code.
```
- Each system isolated and testable
- Easy to extend without breaking existing features
- Future developers (including yourself) can understand it

**Tick-Based Reality**
- Everything updates on game ticks
- Idle mechanics emerge naturally
- Resources flow like time

**Clean Abstractions**
- ResourceManager handles all resources
- BuildingManager handles all buildings
- UpgradeManager handles all research
- MessageLog handles all events
- Each knows its job, does it well

**Error Philosophy**
> "extensive error handling and debugging so the game doesn't crash and so we can figure out what's wrong and fix it promptly"

- Graceful degradation over crashes
- Error messages that explain
- Stack traces for developers, dialogs for players
- Log everything, hide nothing from devs

**Developer Mode (v0.3+)**
- Pseudo-terminal console
- Rich debugging beyond stack traces
- Make development feel like hacking

### Visual Design Principles

**Terminal Aesthetics**
- Borders and boxes create structure
- Colors convey meaning (not just decoration)
- Icons (⛁ ⛀ ⛝ ⛶) show ratios visually
- Animations confirm action without distraction

**Clarity First**
- Numbers always visible
- Stats differentiated from labels
- Progress bars show change
- Dialogs guide without blocking

**Future Vision: Tmux-Style Panels**
- Multiple simultaneous views
- Complex system feeling
- Make players "feel like hackers"
- Alien/MUTHER-style interfaces

---

## 🪐 Colony.sh

### Theme & Atmosphere
**Setting:** Mars colonization with existential dread
**Tone:** Hard sci-fi meets cosmic horror
**Aesthetic:** 1970s computer terminals (Alien's MUTHER)

### Lore Philosophy
> "I'm honestly completely blown away by claude's lore. it's perfect and everything i could want."
> - Donovan, First Playtest

**Narrative Design:**
- Lore reveals through gameplay, not dumps
- Every mechanic has in-world justification
- Message log becomes lore log
- Environmental storytelling through UI

**Player Experience:**
- Start small (basic resources)
- Unlock exponential growth
- Three layers minimum: base → intermediate → advanced
- Choices matter, but not punishing

**Inspirations Blend:**

*Science Fiction:*
- Philip K. Dick (paranoia, identity)
- William Gibson (cyberpunk grit)
- Peter F. Hamilton (vast scope)
- Dune (resource scarcity, ecology)

*Visual:*
- Alien (1979) - MUTHER interface ⭐
- MANIAC - GRTA computer

*Games:*
- NGU Industries (incremental mechanics, humor)
- Universal Paperclips (exponential growth)
- Caves of Qud (weird sci-fi)
- Dwarf Fortress (emergent complexity)
- Mothership TTRPG (horror in space)

*Philosophy:*
- Lovecraft (cosmic insignificance)
- Camus (absurdism)
- Buddhism (cycles, impermanence)

### Gameplay Philosophy

**Early Game (First 10 Minutes):**
- Actions feel meaningful immediately
- Progress visible and rewarding
- Core loop clicks into place
- "I get it" moment happens fast

**Mid Game:**
- Exponential growth unlocked
- Strategic choices emerge
- Systems interconnect
- Prestige/reset on horizon

**Long Game:**
- Can run idle
- Deep optimization possible
- Lore mysteries deepen
- Multiple valid strategies

**Balance Philosophy:**
- Rewarding in 10 minutes
- Engaging for hours
- Respects player's time
- Idle when you want, active when you don't

---

## 🔧 Development Workflow

### Version Strategy

**v0.1** ✅
- Core gameplay loop
- Save/load system
- Basic UI and menus
- Lore foundation
- **Status:** Complete, playtested

**v0.2** 🔧
- **BUGS ONLY**
- Fix construction errors
- Fix research errors
- Fix menu flickering
- Fix border alignment
- No new features

**v0.3** 📋
- Feature additions
- Dialog systems
- Visual enhancements
- Engine improvements
- Polish and animations

### Git Philosophy
- Branch for each version
- Main stays stable
- Commit messages tell story
- Push conversation logs (`.specstory/`)

### Documentation Standards
> "Keep a separate v0.2 devlog and documentation just to keep things isolated and easy to see"

- Each version gets its own devlog
- Bugs tracked separately from features
- Ideas timestamped with version
- Philosophy evolves with project

### Testing Protocol
> "extensive testing to make sure each part works with the whole before fixing"

- Integration testing before commits
- Playtest after each major change
- Log everything during testing
- If it flickers, it's not done

---

## 🎯 Guiding Quotes

> "do what seems smarter in editing each one. little or as much as possible"

> "use your discretion for all these design decisions. you've made it look amazing so far and i don't want to get in the way"

> "fixing the bugs first is priority. and then implementing when set"

> "i'm very impressed and very excited"

> "if it didn't flicker i could get deep into this"

---

## 🌟 The Meta-Philosophy

**Build What You Want To Play**
- Scratch your own itch
- Make the game you wish existed
- Trust your taste

**Iteration Is Love**
- Each version better than last
- Listen to playtests
- Fix before feature

**Document Everything**
- Future you will thank you
- Ideas are precious
- Conversations become lore

**Terminal Magic**
- ASCII isn't limitation, it's aesthetic
- Constraints breed creativity
- Retro visuals, modern feel

---

*"damn i was literally going 'what!' and 'oh fuck' 'that's so good' and laughing and surprised cuz the lore hit so goddamn hard and was so cool and immersive."* - Donovan, discovering Colony.sh for the first time

*"youre a beast my friend. i'm so stoked!"*

---

**Null Point Studios**
**Lattice Engine**
**Colony.sh**

*Making the games we want to play.*
