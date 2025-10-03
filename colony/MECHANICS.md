# Colony.sh - Game Mechanics

**Complete reference for all game systems, formulas, and interactions**

## Core Systems

### Tick System

```
TICK_RATE = 1.0 second
MAX_FPS = 60
RENDER_RATE = 5 FPS (updates every 0.2s)
```

- Game updates 60 times per second for smooth resource flow
- Display refreshes 5 times per second to reduce flicker
- All production/consumption calculated per tick then scaled to per-second

### Sol (Day) Counter

```
SOL_LENGTH = 60.0 seconds
Sol increments every 60 real-time seconds
```

Event log timestamps: `[Sol XXX HH:MM:SS]`

## Resources

### Resource Properties

| Resource | Initial | Max Storage | Generation | Metadata |
|----------|---------|-------------|------------|----------|
| Energy | 20.0 | 100.0 | 0.0 | critical_threshold: 10.0 |
| Metal | 10.0 | 50.0 | 0.0 | - |
| Biomass | 15.0 | 75.0 | 0.0 | - |
| Colonists | 3.0 | 10.0 | 0.0 | integer_only: true, precious: true |

### Resource Update Formula

```python
for each tick (delta_time):
    resource.amount += resource.generation_rate * delta_time
    resource.amount = clamp(resource.amount, 0, resource.max_storage)
```

### Color Coding

```python
if resource.amount >= resource.max_storage * 0.5:
    color = GREEN
elif resource.amount >= resource.max_storage * 0.25:
    color = YELLOW
else:
    color = RED
```

Critical threshold (energy): If amount < 10.0, display warning

## Structures

### Building Cost Formulas

All buildings have **flat costs** (no scaling with count):

```python
cost_to_build = building.cost  # Fixed cost dictionary
can_afford = all(resources[r] >= amount for r, amount in cost.items())
```

### Production Calculation

```python
total_production = {}
for building in buildings:
    for resource, rate in building.produces.items():
        total_production[resource] += rate * building.count

total_consumption = {}
for building in buildings:
    for resource, rate in building.consumes.items():
        total_consumption[resource] += rate * building.count

net_rate = total_production[resource] - total_consumption[resource]
```

### Structure Details

#### Solar Array
```yaml
Cost:
  metal: 5.0
Production:
  energy: 3.0/s per building
Max Count: unlimited
Unlocked: true (always available)
```

**Formula**:
```
Energy generated = 3.0 * solar_array_count * energy_multiplier
```

#### Mining Rig
```yaml
Cost:
  metal: 8.0
  energy: 5.0
Production:
  metal: 2.0/s per building
Max Count: unlimited
Unlocked: true
```

**Net effect**:
- Costs 5 energy to build (one-time)
- Generates 2 metal/s
- No ongoing consumption

#### Reclamation Bay
```yaml
Cost:
  metal: 10.0
  energy: 8.0
Production:
  biomass: 1.5/s per building
Max Count: unlimited
Unlocked: true
```

#### Hab Module
```yaml
Cost:
  metal: 15.0
  biomass: 10.0
Production:
  colonists: 1 (one-time, not per second)
Max Count: unlimited
Unlocked: true
```

**Special behavior**:
- Adds 1 colonist when built
- Does NOT generate colonists over time
- Colonists are precious - no decay

#### Research Terminal
```yaml
Cost:
  metal: 20.0
  energy: 15.0
  biomass: 10.0
Production: none
Max Count: 1
Unlocked: true
Effect: Unlocks advanced research options
```

## Research (Upgrades)

### Research Properties

Research is **permanent** and **one-time purchase**:

```python
upgrade.purchased = false  # Initially
upgrade.purchased = true   # After purchase (permanent)
```

### Research Details

#### Efficient Extraction
```yaml
Cost:
  metal: 30.0
  energy: 20.0
Effects:
  metal_production_multiplier: 1.5
Prerequisites: none
```

**Formula**:
```
metal_production = base_production * 1.5
```

#### Solar Efficiency
```yaml
Cost:
  metal: 25.0
  biomass: 15.0
Effects:
  energy_production_multiplier: 1.5
Prerequisites: none
```

#### Fusion Ignition
```yaml
Cost:
  metal: 50.0
  energy: 40.0
Effects:
  energy_production_multiplier: 2.0
Prerequisites:
  - Research Terminal (built)
  - Solar Efficiency (researched)
Unlocked: false (locked until prerequisites met)
```

**Stacking behavior**:
```
If Solar Efficiency AND Fusion Ignition both purchased:
  energy_production = base * 1.5 * 2.0 = base * 3.0
```

Multipliers are **multiplicative**, not additive.

#### Bioreactor Upgrade
```yaml
Cost:
  metal: 40.0
  energy: 30.0
  biomass: 20.0
Effects:
  biomass_production_multiplier: 1.75
Prerequisites:
  - Research Terminal (built)
Unlocked: false
```

### Upgrade Application

```python
def apply_upgrades(base_production):
    for upgrade in purchased_upgrades:
        for effect_key, multiplier in upgrade.effects.items():
            if 'multiplier' in effect_key:
                resource = effect_key.replace('_production_multiplier', '')
                base_production[resource] *= multiplier
    return base_production
```

## Balancing

### Early Game (Sol 0-10)

**Starting resources**:
- Energy: 20 (enough for 4 seconds at base consumption)
- Metal: 10 (enough for 2 Solar Arrays)
- Biomass: 15
- Colonists: 3

**Initial production** (with starter Solar Array at count=1):
- Energy: +2.5/s (from 1 Solar Array with starting game boost)

**First build path**:
1. Build Mining Rig (8 metal) → +2 metal/s
2. Build Solar Array (5 metal) → +3 energy/s
3. Build Reclamation Bay (10 metal, 8 energy) → +1.5 biomass/s

### Mid Game (Sol 10-50)

**Focus**: Multiply production through research

**Recommended progression**:
1. Research Efficient Extraction → 1.5x metal
2. Research Solar Efficiency → 1.5x energy
3. Build Research Terminal
4. Research Fusion Ignition → 2.0x energy (total 3.0x with Solar Efficiency)

### Late Game (Sol 50+)

**Max theoretical production** (with all upgrades, 10 of each building):

```yaml
Energy:
  Base: 3.0/s per Solar Array * 10 = 30/s
  With Solar Efficiency (1.5x): 45/s
  With Fusion Ignition (2.0x): 90/s
  Total: 90/s

Metal:
  Base: 2.0/s per Mining Rig * 10 = 20/s
  With Efficient Extraction (1.5x): 30/s
  Total: 30/s

Biomass:
  Base: 1.5/s per Reclamation Bay * 10 = 15/s
  With Bioreactor Upgrade (1.75x): 26.25/s
  Total: 26.25/s
```

## Progression Gates

### Resource Gates

**To afford first Mining Rig**: Need 8 metal
- Start with 10 metal → Can build immediately
- But should build Solar Array first for energy

**To afford Research Terminal**: Need 20 metal + 15 energy + 10 biomass
- Requires balanced production of all three
- Typical time: Sol 20-30

**To afford Fusion Ignition**: Need 50 metal + 40 energy
- Requires sustained production
- Typical time: Sol 40-60

### Unlock Gates

Some research is locked behind prerequisites:

```python
Fusion Ignition.unlocked = (
    Research_Terminal.count > 0 AND
    Solar_Efficiency.purchased
)

Bioreactor_Upgrade.unlocked = (
    Research_Terminal.count > 0
)
```

## Save System

### Save Format

```json
{
  "version": "1.0",
  "metadata": {
    "sol": 42,
    "total_playtime": 2520.5,
    "tick_count": 151230
  },
  "resources": {
    "energy": {"amount": 87.5, "max_storage": 100.0},
    "metal": {"amount": 34.2, "max_storage": 50.0}
  },
  "buildings": {
    "solar_array": {"count": 5},
    "mining_rig": {"count": 3}
  },
  "upgrades": {
    "efficient_extraction": {"purchased": true},
    "solar_efficiency": {"purchased": false}
  }
}
```

### Save Integrity

- Validates JSON structure on load
- Falls back to new game if corrupted
- Preserves metadata (playtime, sol, ticks)
- Restores exact resource amounts

## Event Log

### Log Categories

```python
categories = {
    'info': '  ',      # Normal events
    'warning': '⚠',    # Resource low, issues
    'critical': '✖',   # Severe problems
    'success': '✓'     # Achievements, builds
}
```

### Timestamp Format

```
[Sol 042 12:34:56] ✓ Mining Rig constructed
```

### Sol Time Calculation

```python
sols_elapsed = floor(total_playtime / SOL_LENGTH)
time_in_current_sol = total_playtime % SOL_LENGTH
hours = floor(time_in_current_sol / 3600)
minutes = floor((time_in_current_sol % 3600) / 60)
seconds = floor(time_in_current_sol % 60)
timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
```

## UI Systems

### Main Screen Layout

```
╔═══ COLONY.SH ═══════════════════════════╗
║ Sol XXX | Uptime: XXXs                   ║
╠═══════════════════════════════════════════╣
║ RESOURCES                                ║
║ ──────────────────────────────────────── ║
║  ⚡ Energy     XX.X/XXX.X  (+X.X/s)      ║
║  ⛏ Metal      XX.X/XXX.X  (+X.X/s)      ║
║  🧬 Biomass    XX.X/XXX.X  (+X.X/s)      ║
║  👤 Colonists   X.X/XXX.X                ║
║                                          ║
║ STRUCTURES                               ║
║ ──────────────────────────────────────── ║
║  [icon] Name x Count                     ║
║                                          ║
║ EVENT LOG                                ║
║ ──────────────────────────────────────── ║
║  [Sol XXX HH:MM:SS] ✓ Message           ║
║                                          ║
╠═══════════════════════════════════════════╣
║ Commands: [B]uild [R]esearch [I]nfo ... ║
╚═══════════════════════════════════════════╝
```

### Color System

```python
BORDERS = BRIGHT_CYAN
HEADERS = BRIGHT_WHITE
TEXT = WHITE
DIM_TEXT = DIM
SUCCESS = GREEN
WARNING = YELLOW
CRITICAL = RED
```

## Performance

### Optimization Strategies

1. **Tick-based updates**: Fixed timestep physics
2. **Render throttling**: 5 FPS display, 60 FPS logic
3. **Production caching**: Calculate once per tick
4. **Event log pruning**: Keep last 100 entries

### Typical Performance

```
CPU: <1% on modern systems
Memory: ~10MB
Startup: <0.5s
Save/Load: <0.1s
```

## Expansion Points

### Easy to add:

1. **New resources**: Add to `content/resources.py`
2. **New buildings**: Add to `content/structures.py`
3. **New research**: Add to `content/research.py`
4. **New events**: Extend `EventLog` class
5. **Random events**: Hook into tick system

### Data-Oriented Design

All content is defined as dictionaries, making expansion trivial:

```python
# Add new building:
STRUCTURES['new_building'] = {
    'name': 'new_building',
    'display_name': 'New Building',
    'cost': {'metal': 15.0},
    'production': {'energy': 5.0},
    'unlocked': True
}
```

No engine code changes required!

---

*For implementation details, see TUTORIAL.md*
*For gameplay guide, see README.md*
