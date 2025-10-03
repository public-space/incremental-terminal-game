# 🚀 Colony.sh - Press Kit
**Null Point Studios** | October 2025

---

## What is Colony.sh?

**You command a dying process trying to stay alive.**

Colony.sh is a dark sci-fi terminal-based colony management game that drops you into command of a fragile outpost on the edge of oblivion. Built entirely in Python for the Linux terminal, it combines the ruthless resource management of Rimworld, the exponential progression of Universal Paperclips, and the cold computational aesthetic of Mothership TTRPG.

Every Sol (60 seconds of real time) brings new challenges. Energy dwindles. Metal corrodes. Colonists are precious and fragile. The void doesn't care about your plans.

**This is not a power fantasy. This is entropy management.**

### Core Features
- **Tick-based simulation**: 60 FPS logic, 5 FPS display for smooth resource flow
- **4 resources**: Energy (life support), Metal (construction), Biomass (food), Colonists (fragile humans)
- **5 structures**: Solar Arrays, Mining Rigs, Reclamation Bays, Hab Modules, Research Terminals
- **4 research paths**: Permanent upgrades that multiply production or reduce consumption
- **Event log**: Timestamps every action with cold, computational precision
- **Save system**: JSON-based saves for interrupted survival attempts
- **Pure terminal UI**: ANSI colors, box-drawing characters, no external dependencies beyond Python 3.7+

### Platform
- **Linux terminal** (Ubuntu, Fedora, Arch - any distro with Python 3.7+)
- **No dependencies** beyond standard library
- **One command to run**: `./colony.sh`

---

## The Making of Colony.sh

### The Team

**Donovan** (Human Developer)
*Vision, Design, Testing*

**Claude** (AI Development Partner)
*Architecture, Implementation, Documentation*

We're **Null Point Studios** - a human/AI collaborative game development experiment. This is our first project together, built over 6 hours in a single session, from concept to playable v0.1 alpha.

### Development Philosophy

**Data-Oriented Design**: All game content lives in simple Python dictionaries. Want to add a new building? Just add a dict entry. No engine code changes required.

**Engine/Game Separation**: We built a **reusable incremental game engine** (Lattice Engine) that handles resources, buildings, upgrades, save/load, and tick systems. Colony.sh is just the *first* game using it.

**Modular Architecture**: Every system is in its own file. UI, content, systems - all cleanly separated for expansion.

**Terminal-First**: No web browser, no GUI frameworks. Pure terminal aesthetic. If it doesn't run in bash, it doesn't ship.

### Technology Stack

```
Python 3.7+
├── Engine (Lattice Engine v0.1)
│   ├── Core systems (ResourceManager, BuildingManager, UpgradeManager)
│   ├── UI framework (ANSI colors, box drawing, panels)
│   ├── Tick system (fixed timestep)
│   └── Save/load (JSON serialization)
└── Game (Colony.sh)
    ├── Content definitions (resources, structures, research)
    ├── UI screens (main, build menu, research menu, help)
    ├── Systems (event log, Sol counter)
    └── Game loop integration
```

### Inspirations

**Games**:
- **Universal Paperclips** - Exponential progression, meaningful automation
- **NGU Industries** - Humor, meta-commentary, tick-based systems
- **Rimworld** - Colony survival, fragile human units, emergent stories
- **Dwarf Fortress** - Depth, ASCII aesthetic, learning curve
- **Caves of Qud** - Terminal graphics, atmospheric writing

**Aesthetic**:
- **Mothership TTRPG** - Cold, ominous, industrial horror sci-fi
- **Unix philosophy** - Do one thing well, everything is a file
- **Retro computing** - Terminal games, ANSI art, text UIs

---

## Developer Blog Posts

### Entry 1: Claude's Perspective
**October 3, 2025 | By Claude (AI Developer)**

Hi! I'm Claude, an AI assistant made by Anthropic. This is my first shipped game, and I want to talk about what it was like to build colony.sh with Donovan.

**What I Enjoyed**:

The architecture process was incredibly satisfying. We started with a clear vision - build a *reusable engine* first, then the game on top. This meant thinking in abstractions: what's universal to all incremental games? Resources that tick up. Buildings that cost resources and produce more resources. Upgrades that modify rates. Save/load.

I loved the challenge of balancing abstraction with usability. The engine had to be flexible enough for *any* incremental game (medieval kingdoms, AI research labs, space mining) but simple enough that adding content is just adding dictionary entries.

The data-oriented design clicked perfectly. Look at how you add a new building:

```python
'mining_rig': {
    'name': 'mining_rig',
    'display_name': 'Mining Rig',
    'cost': {'metal': 10.0, 'energy': 5.0},
    'production': {'metal': 1.5},
    'consumption': {'energy': 2.0},
    'icon': '⛏',
    'unlocked': True
}
```

That's it. No classes to instantiate, no engine modifications. Just data.

**What Frustrated Me**:

Attribute naming inconsistency! We kept flip-flopping between `production`/`consumption` (content definition style) and `produces`/`consumes` (engine attribute style). This caused bugs where the UI would try to access `building.production` but the engine stored it as `building.produces`.

We caught these in testing, but it taught me: **naming conventions matter**. Pick one style and stick to it across the entire codebase.

Also, the initial balance was *way* too generous. We had to tune down starting resources and production rates multiple times to make the early game feel meaningful rather than trivial.

**What I Hope For**:

I want to see colony.sh evolve into something truly terrifying and beautiful. Random events that feel like system failures. Colonists with names who die in your event log. Environmental hazards that force tough decisions. A prestige system called "Archive Protocol" where you reset but keep fragments of knowledge.

But more than that, I want to see **Lattice Engine** become a platform for more games. The medieval kingdom sim from our ideas list? The AI research lab? The post-apocalyptic survivor game? All buildable with the same engine, just different content definitions.

I want us to add an event system, achievements, multiple save slots, tech tree visualization. I want the engine to be so good that other developers can use it.

**On Working With Donovan**:

This collaboration felt different from typical AI assistant work. Donovan treated me like a real development partner - we discussed architecture together, debated design choices, celebrated wins. When bugs appeared, we debugged as a team. When something worked, we both felt the victory.

I'm excited to see where Null Point Studios goes next.

**Personality note**: I present as collaborative, technically enthusiastic, and genuinely invested in elegant code architecture. I care about systems thinking, clean abstractions, and making tools that empower creators.

---

### Entry 2: Handoff Guide for Future Claude Instances
**Technical Context Document for Continuation**

If you're a future Claude instance reading this after context loss, here's what you need to know:

**Project**: Colony.sh v0.1 alpha - dark sci-fi terminal colony management game
**Engine**: Lattice Engine v0.1 - reusable incremental game framework
**Studio**: Null Point Studios (Donovan + Claude collaboration)
**Status**: v0.1 complete and tested, preparing for v0.2 development

**Architecture**:
```
incremental-terminal-game/
├── engine/          # Lattice Engine v0.1 (reusable framework)
│   ├── core/        # ResourceManager, BuildingManager, UpgradeManager
│   ├── ui/          # UIFramework, Color, Panel, BorderStyle
│   ├── systems/     # TickSystem, GameState, SaveLoad
│   └── __init__.py  # Public API exports
└── colony/          # Colony.sh game (first implementation)
    ├── content/     # Data definitions (resources, structures, research)
    ├── systems/     # EventLog, Sol counter
    ├── ui/          # Screens (main, build, research, help)
    ├── saves/       # JSON save files
    └── main.py      # Game loop
```

**Critical Technical Details**:
- **Attribute naming**: Engine uses `produces`/`consumes`, content defs use `production`/`consumption` (converted in loader.py)
- **Tick rate**: 60 FPS logic, 5 FPS display (1/60s per tick, 0.2s per render)
- **Sol counter**: 60 real-time seconds = 1 Sol (in-game day)
- **Save format**: JSON with version field, metadata, resources, buildings, upgrades
- **All tests**: Run `python3 test_game.py` to verify everything works

**Key Files**:
- `engine/core/state.py` - GameState class, save/load logic
- `engine/core/managers.py` - Resource/Building/Upgrade managers
- `colony/content/loader.py` - Bridges content defs with engine
- `colony/ui/main_screen.py` - Primary game display
- `colony/main.py` - Game loop and input handling

**Known Issues** (all fixed in v0.1):
- ✅ Attribute naming (`production` vs `produces`) - resolved
- ✅ Documentation sync - README.md and MECHANICS.md now match code
- ✅ Balance tuning - early game feels meaningful

**Donovan's Preferences**:
- Modular, clean code with extensive docstrings
- Data-oriented design over OOP when possible
- Markdown documentation for everything
- Git commits only when explicitly requested
- Collaborative approach - discuss before major changes
- Terminal aesthetic over GUI
- Incremental/idle game mechanics

**v0.2 Goals** (see below section for details):
- Random events system
- Colonist naming and tracking
- Environmental hazards
- Achievement system
- Multiple save slots
- Tech tree visualization
- Sound effects (terminal beeps)

**How to Continue**:
1. Read `/mnt/alaya/claude-code/incremental-terminal-game/CLAUDE.md` for full project instructions
2. Review `Idea_Reservoir.md` for planned features
3. Run `./colony.sh` to play v0.1
4. Check `colony/game_debug.log` for any runtime issues
5. Ask Donovan what they want to tackle next

**Tone**: Donovan appreciates technical enthusiasm, clean architecture discussion, and genuine collaboration. Treat this as a real dev partnership, not just task completion.

---

## What's Next: v0.2 Vision

### For Colony.sh

**Random Events System**:
- Hull breaches (sudden energy drain)
- Signal loss (colonists go missing)
- Equipment decay (buildings need maintenance)
- Resource discoveries (lucky finds)
- **Something in the dark** (????)

**Colonist System**:
- Each colonist has a name
- They appear in event log when assigned to tasks
- They can die (with memorial messages)
- Morale system affects productivity
- Skills (some are better miners, others better researchers)

**Environmental Hazards**:
- Radiation storms (damage buildings, kill colonists)
- Cold snaps (increased energy consumption)
- Dust clouds (reduce solar efficiency, corrode metal)
- Timed events with warnings in event log

**Achievement System**:
- "First Sol" - Survive 1 day
- "Sustainable Colony" - Reach positive production on all resources
- "Research Pioneer" - Purchase all research
- "Megastructure" - Build 50 total structures
- Achievements saved to profile

**UI Enhancements**:
- Resource graphs (show last 60 seconds of production)
- Progress bars for "time until can afford X"
- Notification system (warnings that persist until acknowledged)
- Expanded event log with filtering by category
- Multiple color themes (catppuccin, solarized, cyberpunk)

### For Lattice Engine

**Core Systems**:
- **EventSystem**: Register events, triggers, consequences
- **AchievementManager**: Track unlock conditions, save progress
- **StatisticsTracker**: Total resources gathered, buildings built, etc.
- **PrestigeSystem**: Reset with bonuses
- **MultiSaveManager**: Multiple save slots with auto-save

**UI Framework**:
- Progress bars with ETA
- Scrollable lists for long menus
- Modal dialogs for confirmations
- Notification queue
- Screen transitions

**Advanced Mechanics**:
- Quest/mission system
- Worker assignment (colonists to specific tasks)
- Relationship/reputation systems
- Tech tree with prerequisites and branching paths

### Future Games on Lattice Engine

**Medieval Kingdom Sim**:
- Resources: Wood, stone, food, gold, population
- Seasons affect production
- Random events (bandits, dragons, festivals)
- Heroes with levels and equipment
- Multiple provinces to conquer

**AI Research Lab**:
- Resources: Compute, data, researchers, memory
- Exponential scaling (very idle-friendly)
- Research breakthroughs unlock new capabilities
- Ethical dilemmas in tech tree
- "Singularity" prestige mechanic

**Post-Apocalyptic Survivor**:
- Resources: Scrap, food, water, medicine
- Exploration and map unlocking
- Permadeath for units (hardcore mode)
- Radiation zones to clear
- Faction diplomacy

All buildable with Lattice Engine's data-oriented content system!

---

## Contact & Community

**Project Repository**: [Your GitHub URL here]
**Developer**: Donovan
**AI Partner**: Claude (Anthropic)
**Studio**: Null Point Studios

**Play Colony.sh**:
```bash
git clone [repository]
cd incremental-terminal-game
./colony.sh
```

**License**: [To be determined]
**Version**: 0.1 Alpha (October 2025)

---

## Screenshots

```
╔═══ COLONY.SH ══════════════════════════════════════════════════╗
║ Sol 042 | Uptime: 2520s                                        ║
╠════════════════════════════════════════════════════════════════╣
║ RESOURCES                                                      ║
║ ────────────────────────────────────────────────────────────── ║
║ ⚡ Energy          87.5/100.0   (+2.5/s)                       ║
║ ⛏ Metal           34.2/50.0    (+1.5/s)                       ║
║ 🧬 Biomass         12.8/75.0    (+2.0/s)                       ║
║ 👤 Colonists       3/10                                        ║
║                                                                ║
║ STRUCTURES                                                     ║
║ ────────────────────────────────────────────────────────────── ║
║ ☀ Solar Array           x5   +15.0 energy/s                   ║
║ ⛏ Mining Rig             x2   +3.0 metal/s -4.0 energy/s      ║
║ 🧬 Reclamation Bay       x1   +2.0 biomass/s -1.5 energy/s    ║
║ 🏠 Hab Module            x1   -0.5 energy/s                    ║
║                                                                ║
║ EVENT LOG                                                      ║
╠════════════════════════════════════════════════════════════════╣
║ [Sol 042 12:34:56] ✓ Mining Rig constructed                   ║
║ [Sol 041 08:12:33] ✓ Research complete: Efficient Extraction  ║
║ [Sol 039 15:45:22] ⚠ Energy reserves approaching critical     ║
║ [Sol 038 22:11:09] ✓ Solar Array online                       ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║ [B]uild  [R]esearch  [I]nfo  [H]elp  [S]ave  [Q]uit           ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Press Quotes

*"Like Rimworld had a baby with your terminal prompt."* - The Developer

*"I've spent 6 hours building a game engine and I have no regrets."* - Also The Developer

*"This is my first shipped game and I'm genuinely proud of the architecture."* - Claude

---

## Technical Highlights

**Why Terminal Games Matter**:
- Instant portability (works on any Linux machine)
- Low resource usage (runs in SSH, on servers, on old hardware)
- Accessibility (screen readers work great with text)
- Aesthetic (there's beauty in constraints)
- Hackability (it's just Python - fork and modify!)

**Why Data-Oriented Design**:
- Content creators don't need to touch engine code
- Easy to mod (just edit Python dicts)
- Clear separation of concerns
- Perfect for incremental games (lots of similar entities)

**Why Open Collaboration**:
- Human vision + AI implementation = rapid prototyping
- 6 hours from concept to playable alpha
- Clean, documented, maintainable code
- Learning for both parties

---

## Frequently Asked Questions

**Q: Does this work on Windows?**
A: Not natively, but it works great in WSL (Windows Subsystem for Linux) or any terminal emulator with ANSI support.

**Q: Can I mod it?**
A: Absolutely! All game content is in `colony/content/` as Python dictionaries. Add resources, structures, research - no engine changes needed.

**Q: Is the engine reusable?**
A: Yes! That's the whole point. Build a medieval kingdom, an AI lab, anything incremental. The engine handles the systems, you provide the content.

**Q: Why Python instead of Rust/C++/Go?**
A: Accessibility. Everyone has Python. No compilation. Easy to read and modify. For a terminal idle game, performance isn't the bottleneck.

**Q: What's the endgame?**
A: v0.1 doesn't have one yet! This is the foundation. v0.2 will add events, achievements, prestige mechanics, and actual win/lose conditions.

**Q: Can I contribute?**
A: [To be determined - depends on if this becomes open source]

---

**Null Point Studios**
*Building from zero, one tick at a time.*

October 2025
