# colony.sh

**A dark sci-fi frontier colony survival sim**

> *"You command a dying process trying to stay alive."*

Manage a fragile outpost on the edge of oblivion. Balance energy, resources, and colonists in an unforgiving void. Every Sol brings new challenges. Every decision matters.

## 🎮 Quick Start

### Installation

No dependencies beyond Python 3.7+:

```bash
./colony.sh
```

That's it. The game runs directly from the root directory.

### First Steps

1. **Start the game**: `./colony.sh`
2. **Choose**: New Colony (1) or Load (2)
3. **Survive**: Balance resources, build structures, research tech
4. **Command**: Press `h` for help anytime

## 🌌 Game Overview

### Objective

You're managing a frontier colony on a dead world. Your mission:
- Keep systems online
- Generate resources
- Expand operations
- Research technologies
- Keep your colonists alive

### Resources

| Resource | Icon | Description |
|----------|------|-------------|
| **Energy** | ⚡ | Life support. Without it, everything stops. |
| **Metal** | ⛏ | Construction material from dead rock. |
| **Biomass** | 🧬 | Recycled organic matter. Food for colonists. |
| **Colonists** | 👤 | Fragile human units. Precious. |

### Sol Cycle

- **1 Sol** = 60 seconds of real time
- Sol counter tracks days of survival
- Event log timestamps every action

## 🎯 Commands

| Key | Command | Description |
|-----|---------|-------------|
| `b` | Build | Construct structures (costs resources) |
| `r` | Research | Unlock technologies (permanent upgrades) |
| `i` | Info | View detailed statistics |
| `h` | Help | Show in-game help screen |
| `s` | Save | Save your progress |
| `q` | Quit | Exit the game |

## 🏗️ Structures

### Solar Array
- **Cost**: 5 metal
- **Produces**: +3.0 energy/s
- Harvests dim starlight. Barely enough.

### Mining Rig
- **Cost**: 10 metal, 5 energy
- **Produces**: +1.5 metal/s
- **Consumes**: -2.0 energy/s
- Drills into dead rock. Hungry for power.

### Reclamation Bay
- **Cost**: 15 metal, 8 energy
- **Produces**: +2.0 biomass/s
- **Consumes**: -1.5 energy/s
- Turns waste into something edible. Don't think about it.

### Hab Module
- **Cost**: 20 metal, 10 energy
- **Capacity**: 5 colonists
- **Consumes**: -0.5 energy/s
- Cramped quarters. Better than vacuum.

### Research Terminal
- **Cost**: 25 metal, 15 energy
- **Consumes**: -3.0 energy/s
- **Max**: 3 terminals
- Access corrupted databases. Maybe they'll help.

## 🔬 Research

### Efficient Extraction
- **Cost**: 30 metal, 20 energy
- **Effect**: +50% metal generation
- Sharper drills. Deeper cuts. The rock yields.

### Closed-Loop Bioreactor
- **Cost**: 40 metal, 25 energy, 10 biomass
- **Effect**: +50% biomass generation
- Less waste. More time. The cycle tightens.

### Fusion Ignition
- **Cost**: 50 metal, 40 energy
- **Effect**: +100% energy generation
- Brief hope. Exponential power. The reactor hums.

### Redundant Systems
- **Cost**: 35 metal, 30 energy
- **Effect**: -20% energy consumption
- Backup protocols. Failsafes upon failsafes.

## 💾 Save System

- Auto-save: Manual (press `s`)
- Save location: `colony/saves/colony_save.json`
- Load: Select option 2 from main menu
- Multiple saves: Rename save files

## 🎨 Theme

**Inspired by**: Mothership TTRPG, Rimworld, Caves of Qud, Dwarf Fortress

**Aesthetic**: Cold. Computational. Ominous.

This is not a power fantasy. You're managing entropy. Resources are scarce. Colonists are fragile. The void doesn't care.

## 🛠️ Technical Details

- **Engine**: Custom incremental game engine (reusable)
- **Architecture**: Data-oriented content definitions
- **UI**: ANSI terminal with color coding
- **Performance**: Tick-based at 60 FPS
- **Saves**: JSON format

## 📚 File Structure

```
colony/
├── content/        # Game content definitions
│   ├── resources.py
│   ├── structures.py
│   ├── research.py
│   └── loader.py
├── systems/        # Game-specific systems
│   └── event_log.py
├── ui/             # UI screens
│   ├── main_screen.py
│   ├── build_menu.py
│   ├── research_menu.py
│   └── help_screen.py
├── saves/          # Save files
├── config.py       # Game configuration
└── main.py         # Game loop integration
```

## 🐛 Troubleshooting

### Game won't start
- Check Python version: `python3 --version` (need 3.7+)
- Run from project root: `./colony.sh`

### Blank screen
- Terminal too small - resize to at least 80x24
- Colors not showing - terminal may not support ANSI

### Save failed
- Check `colony/saves/` directory exists
- Verify write permissions

## 📖 Learn More

- **MECHANICS.md** - Complete formulas, stats, and interactions
- **TUTORIAL.md** - How the game was built (dev guide)

## 🎯 Strategy Tips

1. **Energy is life** - Always maintain positive energy production
2. **Build Mining Rigs early** - Metal bottleneck is real
3. **Research multipliers** - Exponential growth beats linear
4. **Watch ratios** - Don't let any resource hit zero
5. **Save often** - Catastrophes happen

---

*Built with the incremental game engine*
*For more terminal games, see ../engine/*
