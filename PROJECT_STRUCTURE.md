# Project Structure

**Last Updated:** October 3, 2025

Clean, organized structure for maximum readability and maintainability.

---

## 📁 Root Directory

```
incremental-terminal-game/
├── colony.sh              # Game launcher script
├── CLAUDE.md              # Development instructions for Claude
├── PROJECT_STRUCTURE.md   # This file
│
├── colony/                # Main game source code
├── engine/                # Lattice Engine framework
├── development/           # Development notes & conversations
├── docs/                  # Project documentation
├── lore/                  # Game narrative & worldbuilding
├── marketing/             # Marketing materials
├── web/                   # Website files
├── tests/                 # Test suite
└── logs/                  # Debug & runtime logs
```

---

## 🎮 Game Files

### `colony/` - Main Game
```
colony/
├── main.py                # Entry point
├── config.py              # Game configuration
├── content/               # Game content definitions
│   ├── resources.py       # Resource data
│   ├── structures.py      # Building data
│   └── research.py        # Research/upgrade data
├── systems/               # Game systems
│   └── event_log.py       # Event logging system
├── ui/                    # User interface
│   ├── main_screen.py     # Main game display
│   ├── build_menu.py      # Building menu
│   ├── research_menu.py   # Research menu
│   └── help_screen.py     # Help screen
├── docs/                  # Game documentation
│   ├── README.md          # How to play
│   ├── TUTORIAL.md        # Step-by-step guide
│   └── MECHANICS.md       # Game mechanics breakdown
└── saves/                 # Save files (user data)
```

### `engine/` - Lattice Engine Framework
```
engine/
├── README.md              # Engine documentation
├── game_state.py          # Core state management
├── state_manager.py       # Save/load system
├── resources.py           # Resource system
├── buildings.py           # Building system
├── upgrades.py            # Upgrade/research system
├── tick_system.py         # Game loop & ticks
├── game_loop.py           # Main game loop
├── ui_framework.py        # Terminal UI framework
├── animator.py            # Animation system
├── input_handler.py       # Input processing
└── units.py               # Unit management
```

---

## 📚 Documentation & Content

### `docs/` - Project Documentation
```
docs/
├── DOCUMENTATION_INDEX.md       # Master index of all docs
└── GAME_MODULES_DOCUMENTATION.md # Technical module docs
```

### `lore/` - Narrative & Worldbuilding
```
lore/
├── LORE.md                # Main lore document
└── LORE_IDEAS.md          # Lore brainstorm reservoir
```

### `development/` - Dev Notes & History
```
development/
├── CONVERSATION_LOG.md              # Development conversations
├── DEVLOG.md                        # Development blog
├── colony.sh-lore-and-first-playtest-comments-ideas.md  # Playtest feedback
├── Idea_Reservoir.md                # General ideas
└── Title Ideas for Terminal Dark Sci-Fi Colony Incremental Terminal Sim.md
```

---

## 🌐 Website & Marketing

### `web/` - Website Files
```
web/
├── WEB_IDEAS.md           # Website design ideas
└── site/                  # Actual website files
    ├── index.html         # Homepage
    ├── about.html         # About page
    ├── games.html         # Games showcase
    ├── engine.html        # Lattice Engine info
    ├── devlog.html        # Development blog
    ├── download.html      # Download & install
    ├── style.css          # Terminal theme stylesheet
    └── README.md          # Website documentation
```

### `marketing/` - Marketing Materials
```
marketing/
├── LONG_TERM_GOALS.md     # Strategy & roadmap
├── ONE_PAGER.md           # Quick pitch
└── PRESS_KIT.md           # Press kit
```

---

## 🧪 Testing & Debugging

### `tests/` - Test Suite
```
tests/
├── test_game.py           # Game tests
└── test_integration.py    # Integration tests
```

### `logs/` - Debug & Runtime Logs
```
logs/
├── colony_game_debug.log  # Colony game debug output
├── colony_runtime.log     # Colony runtime log
├── game_debug.log         # General debug log
└── colony.log             # General colony log
```

---

## 🎯 File Categories

### Essential Game Files
- `colony.sh` - Launcher
- `colony/main.py` - Entry point
- `colony/config.py` - Configuration
- `colony/content/*` - Game data
- `engine/*` - Framework code

### Documentation
- `colony/docs/*` - Player-facing docs
- `docs/*` - Developer docs
- `engine/README.md` - Engine docs
- `web/site/README.md` - Website docs

### Development
- `development/*` - Dev notes, conversations, ideas
- `lore/*` - Narrative design
- `tests/*` - Test suite
- `logs/*` - Debug output

### Marketing & Web
- `marketing/*` - Marketing materials
- `web/*` - Website files

---

## 🚫 Ignored Files (.gitignore)

The following are ignored by git:
- `__pycache__/` - Python bytecode cache
- `*.pyc` - Compiled Python files
- `*.pyo` - Optimized Python files
- `logs/*.log` - Log files (too large for git)
- `colony/saves/*.json` - User save files (local only)
- `.DS_Store` - macOS metadata
- `.vscode/` - VS Code settings
- `.idea/` - PyCharm settings

---

## 📋 Navigation Quick Reference

| What do you want? | Where to look |
|-------------------|---------------|
| **Play the game** | `./colony.sh` |
| **Game source code** | `colony/` |
| **Engine framework** | `engine/` |
| **How to play** | `colony/docs/README.md` |
| **Game mechanics** | `colony/docs/MECHANICS.md` |
| **Lore & story** | `lore/LORE.md` |
| **Development history** | `development/DEVLOG.md` |
| **Playtest feedback** | `development/colony.sh-lore-and-first-playtest-comments-ideas.md` |
| **Website** | `web/site/` |
| **Marketing materials** | `marketing/` |
| **Long-term roadmap** | `marketing/LONG_TERM_GOALS.md` |
| **Engine documentation** | `engine/README.md` |
| **All documentation** | `docs/DOCUMENTATION_INDEX.md` |

---

## 🔄 Version Control

**Branch Strategy:**
- `main` - Stable releases (v0.1, v0.2, etc.)
- `v0.2-dev` - Development branch for v0.2 features
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches

**Current Version:** v0.1 (released October 3, 2025)

**Next Version:** v0.2 (in planning)

---

## 📝 Notes

- All documentation uses Markdown format
- Game uses Python 3.8+ (no external dependencies)
- Save files are JSON (human-readable)
- Website is static HTML/CSS (no JavaScript required)
- Logs are auto-generated (don't commit to git)

---

**Null Point Studios**
*Building from zero, one tick at a time.*
