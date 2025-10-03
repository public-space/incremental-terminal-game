# ⚙️ Lattice Engine
**A data-oriented framework for terminal incremental games**

Version 0.1 Alpha | Null Point Studios | October 2025

---

## What is Lattice Engine?

Lattice Engine is a reusable Python framework for building incremental/idle games in the terminal. It provides all the core systems - resources, buildings, upgrades, tick simulation, save/load, UI - so you can focus on game content.

**Philosophy**: Data-oriented design. Content is data, engine is logic. No engine changes needed to add resources, buildings, or research.

---

## Why "Lattice"?

A lattice is a **structure** - interconnected points forming a framework. Perfect metaphor for:
- **Game systems** (resources connect to buildings connect to upgrades)
- **Terminal aesthetics** (box-drawing characters form visual lattices)
- **Extensibility** (lattice structures grow by adding nodes)
- **Any game theme** (not locked to sci-fi or fantasy)

From "Oblivion Lattice" - one of our original game name ideas.

---

## Core Features

### ✅ Implemented (v0.1)

**Resource Management**:
- ResourceManager with automatic generation/consumption
- Color-coded status (green/yellow/red based on % full)
- Integer-only mode for discrete resources (e.g., colonists)
- Metadata support (icons, thresholds, custom properties)

**Building System**:
- BuildingManager with production/consumption tracking
- Cost calculation and affordability checks
- Count-based (build multiple of same structure)
- Max count limits per building type
- Unlock gates for progression

**Upgrade System**:
- UpgradeManager for permanent one-time purchases
- Effect multipliers (production, consumption)
- Prerequisite chains (for tech trees)
- Unlock conditions

**Tick System**:
- Fixed timestep simulation (60 FPS logic)
- Delta time support for smooth resource accumulation
- Decoupled from display refresh rate
- Deterministic (same inputs = same outputs)

**Save/Load**:
- JSON-based serialization
- Version field for migration support
- Metadata preservation
- Graceful error handling (falls back to new game if corrupted)

**UI Framework**:
- ANSI color support with fallback
- Box-drawing characters for borders
- Panel system for layout
- Color presets (success, warning, critical, etc.)
- Terminal clearing and cursor positioning

### 🚧 Planned (v0.2+)

**Event System**:
- Random events with triggers and consequences
- Timed events
- Event categories and filtering
- Event history logging

**Achievement System**:
- Unlock conditions
- Progress tracking
- Save to player profile
- Categories (survival, building, research, etc.)

**Statistics Tracker**:
- Total resources gathered
- Buildings built
- Upgrades purchased
- Time survived
- Historical graphs

**Prestige System**:
- Reset with bonuses
- Currency/points for resets
- Unlock new starting options
- Meta-progression

**Advanced UI**:
- Progress bars with ETA
- Scrollable lists
- Modal dialogs
- Notification queue
- Multiple screen layouts

---

## Architecture

```
engine/
├── __init__.py          # Public API exports
├── core/
│   ├── managers.py      # ResourceManager, BuildingManager, UpgradeManager
│   ├── state.py         # GameState, save/load logic
│   └── tick.py          # TickSystem for fixed timestep
├── ui/
│   ├── framework.py     # UIFramework, rendering utilities
│   ├── colors.py        # Color definitions and ANSI codes
│   └── components.py    # Panel, BorderStyle, etc.
└── README.md            # This file
```

---

## Quick Start

### 1. Import the engine

```python
from engine import (
    GameState,
    ResourceManager,
    BuildingManager,
    UpgradeManager,
    UIFramework,
    Color
)
```

### 2. Create game state

```python
game = GameState()
```

### 3. Define content (data-oriented)

```python
# Add a resource
game.resources.add_resource(
    name='energy',
    display_name='Energy',
    initial=20.0,
    max_storage=100.0,
    generation_rate=0.0,
    metadata={'icon': '⚡', 'critical_threshold': 10.0}
)

# Add a building
game.buildings.register_building(
    name='solar_array',
    display_name='Solar Array',
    cost={'metal': 5.0},
    produces={'energy': 3.0},
    consumes={},
    metadata={'icon': '☀'}
)

# Add an upgrade
game.upgrades.register_upgrade(
    name='solar_efficiency',
    display_name='Solar Efficiency',
    cost={'metal': 30.0, 'energy': 20.0},
    effects={'energy_production_multiplier': 1.5},
    prerequisites=[]
)
```

### 4. Game loop

```python
import time
from engine import TickSystem

tick_system = TickSystem(target_fps=60)

while True:
    delta_time = tick_system.tick()

    # Update resources based on production
    game.resources.update(delta_time)

    # Render UI (throttled to ~5 FPS)
    if tick_system.should_render():
        ui.clear_screen()
        # ... render game state ...

    # Handle input
    # ... player commands ...
```

### 5. Save/Load

```python
# Save
game.save_game('saves/my_game.json')

# Load
game.load_game('saves/my_game.json')
```

---

## Design Principles

### 1. Data-Oriented
Content is data (dictionaries), not code (classes). Adding a new resource/building/upgrade should never require engine changes.

### 2. Separation of Concerns
- **Engine** = systems (how resources work)
- **Content** = definitions (what resources exist)
- **UI** = presentation (how resources display)

### 3. Composability
Systems should work together cleanly. Buildings consume/produce resources. Upgrades modify rates. Events trigger state changes.

### 4. Extensibility
Every system should have hooks for expansion. Event callbacks, custom metadata, effect systems.

### 5. Debuggability
Clear error messages. Extensive logging. Validation on load. Graceful degradation.

---

## Games Built on Lattice Engine

### 🌌 Colony.sh (v0.1 Alpha)
**Genre**: Dark sci-fi colony management
**Theme**: Fragile outpost on edge of oblivion
**Resources**: Energy, Metal, Biomass, Colonists
**Status**: Released

### 🏰 Medieval Kingdom (Planned)
**Genre**: Kingdom builder
**Theme**: Village to empire progression
**Resources**: Wood, stone, food, gold, population

### 🤖 AI Research Lab (Planned)
**Genre**: AI development simulator
**Theme**: Build AGI from basic algorithms
**Resources**: Compute, data, researchers, memory

### ☢️ Post-Apocalyptic Survivor (Planned)
**Genre**: Survival sim
**Theme**: Rebuild civilization from ashes
**Resources**: Scrap, food, water, medicine, survivors

---

## Philosophy: Why Terminal Games?

**Accessibility**:
- Works over SSH
- Runs on servers, old hardware, minimal systems
- Screen reader friendly
- No GPU required

**Portability**:
- Pure Python, no compilation
- Works on Linux, macOS, WSL
- No dependencies beyond standard library

**Hackability**:
- Just text files - easy to read, modify, fork
- Mod by editing Python dicts
- Version control friendly
- Educational (learn by reading source)

**Aesthetics**:
- Beauty in constraints
- Retro computing nostalgia
- ANSI art and box-drawing characters
- Minimalist, functional design

---

## Contributing

[TBD - depends on if this becomes open source]

---

## License

[TBD]

---

## Credits

**Architecture & Implementation**: Claude (Anthropic AI)
**Design & Vision**: Donovan
**Studio**: Null Point Studios

**Inspired by**:
- Incremental game frameworks (Derivative Clicker, etc.)
- curses/blessed Python libraries
- Roguelike terminal UIs
- Data-oriented game design

---

## Version History

### v0.1 Alpha (October 2025)
- Initial release
- Core systems: Resources, Buildings, Upgrades
- Tick simulation with fixed timestep
- Save/load with JSON
- UI framework with ANSI colors
- First game: colony.sh

### v0.2 (Planned)
- Event system
- Achievement framework
- Statistics tracking
- Prestige mechanics
- Multiple save slots
- Advanced UI components

---

**Lattice Engine**
*Build games. One tick at a time.*

Null Point Studios | 2025
