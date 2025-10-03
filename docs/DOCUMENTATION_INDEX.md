# 📚 Colony.sh & Lattice Engine - Documentation Index

**Null Point Studios** | **Version 0.1 Alpha** | October 2025

---

## 🎯 Quick Navigation

**New to the project?** Start here:
1. Read [ONE_PAGER.md](ONE_PAGER.md) - 2 minute overview
2. Read [colony/README.md](colony/README.md) - How to play
3. Run `./colony.sh` - Try the game!

**Want to understand the systems?**
- [colony/MECHANICS.md](colony/MECHANICS.md) - All formulas and stats

**Want to develop with Lattice Engine?**
- [engine/README.md](engine/README.md) - Engine documentation
- [TUTORIAL.md](TUTORIAL.md) - How the game was built

**Press & Marketing**:
- [PRESS_KIT.md](PRESS_KIT.md) - Complete press kit
- [DEVLOG.md](DEVLOG.md) - Development blog

---

## 📄 All Documentation Files

### Core Game Documentation

**[colony/README.md](colony/README.md)**
*Player-facing game documentation*
- Quick start guide
- Game overview and objectives
- Resources and Sol cycle explanation
- All commands (build, research, save, etc.)
- Structure and research details
- Strategy tips

**[colony/MECHANICS.md](colony/MECHANICS.md)**
*Technical reference for all game systems*
- Tick system (60 FPS logic, 5 FPS display)
- Resource formulas and color coding
- Structure costs, production, consumption
- Research effects and multipliers
- Balancing calculations
- Progression gates
- Save format specification
- Event log system
- UI layout
- Performance metrics
- Expansion points

**[colony/TUTORIAL.md](colony/TUTORIAL.md)**
*How the game was built (developer guide)*
- Architecture overview
- Engine vs. game code separation
- Step-by-step implementation
- Design decisions
- Testing approach
- Future expansion guide

---

### Engine Documentation

**[engine/README.md](engine/README.md)**
*Lattice Engine framework documentation*
- What is Lattice Engine
- Why "Lattice" as the name
- Core features (implemented + planned)
- Architecture overview
- Quick start guide with code examples
- Design principles
- Games built on Lattice
- Philosophy: why terminal games
- Version history

---

### Marketing & Press Materials

**[PRESS_KIT.md](PRESS_KIT.md)**
*Complete press kit for media/community*
- What is colony.sh (enticing description)
- The making of colony.sh
- Development team (Donovan + Claude)
- Technology stack
- Inspirations (games + aesthetic)
- Developer blog posts:
  - Claude's perspective
  - Handoff guide for future Claude instances
- v0.2 vision and roadmap
- FAQ
- Contact info
- Screenshots (ASCII art)

**[ONE_PAGER.md](ONE_PAGER.md)**
*Quick marketing overview*
- Elevator pitch
- Key features
- Team info
- Tech highlights
- Inspirations
- What's next
- Contact

**[DEVLOG.md](DEVLOG.md)**
*Development blog and post-mortem*
- v0.1 timeline and achievements
- Claude's post-mortem (what worked, struggled with, learned)
- Donovan's post-mortem [to be filled]
- Technical decisions log (why Python, why terminal, etc.)
- Code statistics
- Known issues
- Full roadmap (v0.2, v0.3, v1.0)
- Credits

---

### Project Planning & Ideas

**[CLAUDE.md](CLAUDE.md)**
*Instructions for Claude (project requirements)*
- Original prompt for the game
- Development requirements
- Important instruction reminders

**[Idea_Reservoir.md](Idea_Reservoir.md)**
*Future game concepts and expansion ideas*
- Game name brainstorming (chose: colony.sh)
- Colony.sh implementation phases
- Future game themes:
  - AI Research Lab
  - Space Mining Colony
  - Post-Apocalyptic Survivor
  - Mad Scientist Laboratory
  - Medieval Kingdom
- Engine features to add
- Visual improvements
- Design notes

**[Title Ideas for Terminal Dark Sci-Fi Colony Incremental Terminal Sim.md](Title%20Ideas%20for%20Terminal%20Dark%20Sci-Fi%20Colony%20Incremental%20Terminal%20Sim.md)**
*Original brainstorming document*
- Name ideas from chatGPT collaboration
- Themes: Mothership, Cosmic, Terminal, Code-flavored
- Final choice: colony.sh

**[GAME_MODULES_DOCUMENTATION.md](GAME_MODULES_DOCUMENTATION.md)**
*Module structure documentation*
- [Content to be verified]

---

## 🎮 Game Files Reference

### Entry Point
- `colony.sh` - Main launcher script (run this!)
- `colony/main.py` - Game loop and initialization

### Content Definitions (Data)
- `colony/content/resources.py` - All resources
- `colony/content/structures.py` - All buildings
- `colony/content/research.py` - All upgrades
- `colony/content/loader.py` - Loads content into engine

### Game Systems
- `colony/systems/event_log.py` - Event logging with Sol timestamps
- `colony/config.py` - Game configuration

### UI Screens
- `colony/ui/main_screen.py` - Primary game display
- `colony/ui/build_menu.py` - Structure building menu
- `colony/ui/research_menu.py` - Research/upgrade menu
- `colony/ui/help_screen.py` - In-game help

### Saves & Logs
- `colony/saves/` - Save file directory (JSON)
- `colony/game_debug.log` - Debug output

---

## ⚙️ Engine Files Reference

### Core Systems
- `engine/core/managers.py` - ResourceManager, BuildingManager, UpgradeManager
- `engine/core/state.py` - GameState, save/load
- `engine/core/tick.py` - TickSystem for fixed timestep

### UI Framework
- `engine/ui/framework.py` - UIFramework, rendering
- `engine/ui/colors.py` - Color definitions, ANSI codes
- `engine/ui/components.py` - Panel, BorderStyle

### Modules
- `engine/systems/` - Reusable systems (tick, event, etc.)
- `engine/__init__.py` - Public API exports

---

## 🧪 Testing

**[test_game.py](test_game.py)**
*Automated test suite*
- Game state loading
- Build menu rendering
- Research menu functionality
- Save/load verification

**Run tests**:
```bash
python3 test_game.py
```

**Expected output**: `ALL TESTS PASSED ✓`

---

## 📊 Project Statistics

### Documentation
- **Player docs**: 2 files (~500 lines)
- **Technical docs**: 2 files (~700 lines)
- **Marketing docs**: 3 files (~800 lines)
- **Planning docs**: 3 files (~300 lines)
- **Total**: ~2300 lines of documentation

### Code
- **Engine**: ~800 lines
- **Game**: ~900 lines
- **Total**: ~1700 lines of Python

### Files
- **Python files**: 24
- **Markdown docs**: 10
- **Total project files**: 34+

---

## 🎯 Recommended Reading Order

### For Players
1. [ONE_PAGER.md](ONE_PAGER.md) - What is this?
2. [colony/README.md](colony/README.md) - How do I play?
3. [colony/MECHANICS.md](colony/MECHANICS.md) - How does it work?
4. Play the game: `./colony.sh`

### For Developers
1. [engine/README.md](engine/README.md) - What is Lattice Engine?
2. [colony/TUTORIAL.md](colony/TUTORIAL.md) - How was this built?
3. [DEVLOG.md](DEVLOG.md) - Development process
4. Read source: `engine/core/`, `colony/content/`

### For Press/Media
1. [PRESS_KIT.md](PRESS_KIT.md) - Complete press kit
2. [ONE_PAGER.md](ONE_PAGER.md) - Quick facts
3. [DEVLOG.md](DEVLOG.md) - Developer perspectives

### For Future Claude Instances
1. [PRESS_KIT.md](PRESS_KIT.md) - Read "Entry 2: Handoff Guide"
2. [CLAUDE.md](CLAUDE.md) - Original instructions
3. [Idea_Reservoir.md](Idea_Reservoir.md) - Planned features
4. [DEVLOG.md](DEVLOG.md) - What we've built so far

---

## 🚀 Quick Links

**Play the game**:
```bash
./colony.sh
```

**Run tests**:
```bash
python3 test_game.py
```

**Check git status**:
```bash
git status
```

**View save files**:
```bash
ls -lh colony/saves/
```

**Read debug log**:
```bash
tail -f colony/game_debug.log
```

---

## 📝 Notes

- All documentation is current as of **v0.1 Alpha (October 3, 2025)**
- Documentation is updated manually - check git commit dates for freshness
- If code and docs conflict, **code is source of truth** (then file a bug!)
- Press kit includes sections for Donovan to fill in with personal perspective

---

## 🎨 Branding

**Studio Name**: Null Point Studios
**Engine Name**: Lattice Engine
**Game Name**: colony.sh
**Tagline**: *"Building from zero, one tick at a time."*

**Studio Philosophy**:
- Human/AI collaboration
- Data-oriented design
- Terminal-first aesthetics
- Open development
- Rapid prototyping
- Clean, documented code

---

**Null Point Studios**
*Building from zero, one tick at a time.*

Last updated: October 3, 2025
