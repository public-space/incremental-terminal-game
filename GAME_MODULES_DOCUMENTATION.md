# Game Modules Documentation

> Comprehensive documentation for the Incremental Terminal Game engine and game systems

**Version:** 1.0.0
**Last Updated:** 2025-10-02

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Engine Modules](#engine-modules)
  - [TickSystem](#ticksystem)
  - [StateManager](#statemanager)
- [Game Modules](#game-modules)
  - [ResourceManager](#resourcemanager)
  - [BuildingManager](#buildingmanager)
  - [UnitManager](#unitmanager)
  - [UpgradeManager](#upgrademanager)
  - [GameState](#gamestate)
- [Integration Guide](#integration-guide)
- [Save/Load System](#saveload-system)
- [Examples](#examples)

---

## Architecture Overview

The game follows a modular architecture with clear separation between engine systems and game-specific logic:

```
┌─────────────────────────────────────┐
│          GameState (Central)        │
│   Coordinates all game systems      │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐        ┌─────▼──────┐
│ Engine │        │    Game    │
│ Layer  │        │   Layer    │
└───┬────┘        └─────┬──────┘
    │                   │
    ├─ TickSystem       ├─ ResourceManager
    └─ StateManager     ├─ BuildingManager
                        ├─ UnitManager
                        └─ UpgradeManager
```

**Design Principles:**
- **Modularity**: Each system is self-contained and reusable
- **Extensibility**: Easy to add new resources, buildings, units, and upgrades
- **Data-driven**: Game content separated from logic
- **Save/Load**: Full serialization support for all systems

---

## Engine Modules

### TickSystem

**Location:** `engine/tick_system.py`

Manages the game loop timing and provides a consistent update cycle for idle/incremental mechanics.

#### Key Features
- Configurable tick rate (updates per second)
- Callback registration for tick events
- Delta time tracking
- Performance statistics

#### Class: `TickSystem`

**Constructor:**
```python
TickSystem(tick_rate: float = 1.0)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `start()` | Start the tick system |
| `stop()` | Stop the tick system |
| `should_tick()` | Check if it's time for next tick |
| `tick()` | Execute a single tick update |
| `register_callback(callback)` | Register function to call each tick |
| `set_tick_rate(new_rate)` | Change tick rate |
| `get_stats()` | Get tick statistics |

**Example:**
```python
from engine.tick_system import TickSystem

tick_system = TickSystem(tick_rate=1.0)  # 1 tick per second
tick_system.register_callback(my_update_function)
tick_system.start()

while game_running:
    if tick_system.should_tick():
        tick_system.tick()
    time.sleep(0.01)
```

---

### StateManager

**Location:** `engine/state_manager.py`

Generic key-value state storage with nested dictionary support and observer pattern.

#### Key Features
- Dot notation for nested keys (`player.inventory.gold`)
- Observer pattern for state changes
- Increment/decrement helpers for numeric values
- Full serialization support

#### Class: `StateManager`

**Key Methods:**

| Method | Description |
|--------|-------------|
| `set(key, value)` | Set a state value |
| `get(key, default)` | Get a state value |
| `increment(key, amount)` | Increment numeric value |
| `decrement(key, amount)` | Decrement numeric value |
| `exists(key)` | Check if key exists |
| `observe(key, callback)` | Register observer for key changes |
| `get_all()` | Get entire state as dict |
| `set_all(data)` | Replace entire state |

**Example:**
```python
from engine.state_manager import StateManager

state = StateManager()
state.set('player.gold', 100)
state.increment('player.gold', 50)
print(state.get('player.gold'))  # 150

# Observer pattern
def on_gold_change(key, new_val, old_val):
    print(f"Gold: {old_val} → {new_val}")

state.observe('player.gold', on_gold_change)
```

---

## Game Modules

### ResourceManager

**Location:** `game/resources.py`

Manages all game resources including amounts, generation rates, and storage limits.

#### Key Features
- Unlimited or capped storage
- Automatic generation over time
- Transaction system (add/spend)
- Resource unlocking
- Full cost checking

#### Class: `Resource`

A dataclass representing a single resource type.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier |
| `amount` | float | Current amount |
| `max_storage` | float/None | Storage limit |
| `generation_rate` | float | Generation per second |
| `display_name` | str | UI display name |
| `unlocked` | bool | Visibility flag |

#### Class: `ResourceManager`

**Key Methods:**

| Method | Description |
|--------|-------------|
| `add_resource(name, initial, ...)` | Register new resource type |
| `get_amount(name)` | Get current resource amount |
| `add(name, amount)` | Add to resource |
| `spend(name, amount)` | Spend resource (atomic) |
| `can_afford(costs)` | Check multiple resource costs |
| `spend_multiple(costs)` | Spend multiple resources atomically |
| `generate(delta_time)` | Generate resources based on rates |
| `unlock_resource(name)` | Make resource visible |
| `set_generation_rate(name, rate)` | Update generation rate |

**Example:**
```python
from game.resources import ResourceManager

rm = ResourceManager()
rm.add_resource('gold', initial=100, generation_rate=1.0)
rm.add_resource('wood', initial=0, max_storage=500)

# Generate for 5 seconds
rm.generate(delta_time=5.0)
print(rm.get_amount('gold'))  # 105

# Spend resources
if rm.spend('gold', 50):
    print("Purchase successful!")

# Check costs
costs = {'gold': 30, 'wood': 20}
if rm.can_afford(costs):
    rm.spend_multiple(costs)
```

---

### BuildingManager

**Location:** `game/buildings.py`

Manages building construction, ownership, and resource production/consumption.

#### Key Features
- Cost system for construction
- Production and consumption rates
- Building unlocking
- Max count limits
- Category organization

#### Class: `Building`

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier |
| `cost` | dict | Build cost {resource: amount} |
| `count` | int | Number owned |
| `produces` | dict | Production {resource: rate/s} |
| `consumes` | dict | Consumption {resource: rate/s} |
| `unlocked` | bool | Availability flag |
| `max_count` | int/None | Maximum allowed |

#### Class: `BuildingManager`

**Constructor:**
```python
BuildingManager(resource_manager: ResourceManager)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `register_building(name, cost, ...)` | Add building type |
| `build(name, count)` | Construct buildings |
| `can_build(name, count)` | Check if can build |
| `demolish(name, count)` | Remove buildings |
| `unlock_building(name)` | Make building available |
| `get_total_production()` | Get all production rates |
| `update_production(delta_time)` | Apply production/consumption |

**Example:**
```python
from game.buildings import BuildingManager
from game.resources import ResourceManager

rm = ResourceManager()
rm.add_resource('wood', initial=100)
rm.add_resource('food', initial=0)

bm = BuildingManager(resource_manager=rm)

# Register building
bm.register_building(
    'farm',
    cost={'wood': 30},
    produces={'food': 1.0},
    description="Produces food",
    unlocked=True
)

# Build it
if bm.can_build('farm'):
    bm.build('farm', count=2)

# Update production
bm.update_production(delta_time=10.0)
print(rm.get_amount('food'))  # 20.0
```

---

### UnitManager

**Location:** `game/units.py`

Manages worker units, recruitment, production, and upkeep costs.

#### Key Features
- Recruitment system
- Production rates per unit
- Upkeep/maintenance costs
- Unit categorization
- Training time support

#### Class: `Unit`

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier |
| `cost` | dict | Recruitment cost |
| `count` | int | Number recruited |
| `produces` | dict | Production per unit |
| `upkeep` | dict | Upkeep per unit |
| `unlocked` | bool | Availability flag |
| `training_time` | float | Recruitment time (seconds) |

#### Class: `UnitManager`

**Constructor:**
```python
UnitManager(resource_manager: ResourceManager)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `register_unit(name, cost, ...)` | Add unit type |
| `recruit(name, count)` | Recruit units |
| `can_recruit(name, count)` | Check if can recruit |
| `dismiss(name, count)` | Remove units |
| `unlock_unit(name)` | Make unit available |
| `get_total_production()` | Get total unit production |
| `get_total_upkeep()` | Get total upkeep costs |
| `update_production(delta_time)` | Apply production and upkeep |

**Example:**
```python
from game.units import UnitManager
from game.resources import ResourceManager

rm = ResourceManager()
rm.add_resource('food', initial=100)
rm.add_resource('wood', initial=0)

um = UnitManager(resource_manager=rm)

# Register unit
um.register_unit(
    'worker',
    cost={'food': 10},
    produces={'wood': 0.5},
    upkeep={'food': 0.1},
    unlocked=True
)

# Recruit
um.recruit('worker', count=3)

# Update
um.update_production(delta_time=10.0)
print(rm.get_amount('wood'))  # 15.0 (3 workers × 0.5/s × 10s)
print(rm.get_amount('food'))  # 70.0 (started 100, spent 30 recruiting, spent 3 upkeep)
```

---

### UpgradeManager

**Location:** `game/upgrades.py`

Manages one-time purchases that provide permanent bonuses and unlock new features.

#### Key Features
- One-time and repeatable upgrades
- Tech tree with prerequisites
- Effect accumulation
- Unlock chaining
- Cost scaling for repeatable upgrades

#### Class: `Upgrade`

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier |
| `cost` | dict | Purchase cost |
| `purchased` | bool | Purchase status |
| `effects` | dict | Effects/bonuses provided |
| `prerequisites` | set | Required upgrades |
| `unlocks` | list | What this unlocks |
| `repeatable` | bool | Can purchase multiple times |
| `max_purchases` | int/None | Maximum purchases |

#### Class: `UpgradeManager`

**Constructor:**
```python
UpgradeManager(resource_manager: ResourceManager)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `register_upgrade(name, cost, ...)` | Add upgrade |
| `purchase(name)` | Buy upgrade |
| `can_purchase(name)` | Check prerequisites and cost |
| `is_purchased(name)` | Check purchase status |
| `unlock_upgrade(name)` | Make upgrade available |
| `get_effect_value(effect)` | Get cumulative effect value |
| `get_all_effects()` | Get all active effects |

**Example:**
```python
from game.upgrades import UpgradeManager
from game.resources import ResourceManager

rm = ResourceManager()
rm.add_resource('gold', initial=500)

um = UpgradeManager(resource_manager=rm)

# Create tech tree
um.register_upgrade(
    'basic_tools',
    cost={'gold': 50},
    effects={'wood_bonus': 0.25},
    unlocked=True
)

um.register_upgrade(
    'advanced_tools',
    cost={'gold': 200},
    effects={'wood_bonus': 0.5},
    prerequisites=['basic_tools'],
    unlocked=True
)

# Purchase
um.purchase('basic_tools')
um.purchase('advanced_tools')

# Get effects
total_bonus = um.get_effect_value('wood_bonus')  # 0.75
print(f"Wood gathering: +{total_bonus * 100}%")
```

---

### GameState

**Location:** `game/game_state.py`

Central coordinator that integrates all game systems and handles save/load.

#### Key Features
- Coordinates all managers
- Save/load to JSON
- Playtime tracking
- Statistics export
- Auto-save support

#### Class: `GameState`

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `resources` | ResourceManager | Resource system |
| `buildings` | BuildingManager | Building system |
| `units` | UnitManager | Unit system |
| `upgrades` | UpgradeManager | Upgrade system |
| `state` | StateManager | Generic state storage |
| `metadata` | dict | Game metadata |

**Key Methods:**

| Method | Description |
|--------|-------------|
| `initialize()` | Set up new game |
| `update(delta_time)` | Update all systems |
| `save_game(filepath)` | Save to file |
| `load_game(filepath)` | Load from file |
| `auto_save(save_dir, filename)` | Automatic save |
| `export_stats()` | Export statistics |
| `reset()` | Reset entire game |

**Example:**
```python
from game.game_state import GameState

# Create and initialize
game = GameState()
game.initialize()

# Set up resources
game.resources.add_resource('gold', initial=100, generation_rate=1.0)

# Update game
for _ in range(10):
    game.update(delta_time=1.0)

# Save
game.save_game('saves/mygame.json')

# Load
new_game = GameState()
new_game.load_game('saves/mygame.json')

# Get stats
stats = game.export_stats()
print(f"Playtime: {game.get_playtime_formatted()}")
```

---

## Integration Guide

### Basic Integration

Here's how to integrate all systems into a complete game:

```python
from game.game_state import GameState

# 1. Create game state
game = GameState()
game.initialize()

# 2. Set up resources
game.resources.add_resource('gold', initial=100, generation_rate=0.5)
game.resources.add_resource('wood', initial=50, max_storage=500)
game.resources.add_resource('food', initial=0)

# 3. Register buildings
game.buildings.register_building(
    'farm',
    cost={'wood': 30},
    produces={'food': 1.0},
    unlocked=True
)

game.buildings.register_building(
    'lumber_mill',
    cost={'wood': 50, 'gold': 25},
    produces={'wood': 0.5},
    unlocked=True
)

# 4. Register units
game.units.register_unit(
    'worker',
    cost={'food': 10},
    produces={'gold': 0.3},
    upkeep={'food': 0.1},
    unlocked=True
)

# 5. Register upgrades
game.upgrades.register_upgrade(
    'better_tools',
    cost={'gold': 100},
    effects={'production_bonus': 0.2},
    unlocked=True
)

# 6. Game loop
while running:
    if tick_system.should_tick():
        game.update(delta_time=tick_system.tick())

    # Auto-save every 100 ticks
    if game.metadata['tick_count'] % 100 == 0:
        game.auto_save()
```

### Tick System Integration

```python
from engine.tick_system import TickSystem
from game.game_state import GameState

tick_system = TickSystem(tick_rate=1.0)
game = GameState()
game.initialize()

# Register game update as tick callback
def on_tick(delta_time):
    game.update(delta_time)

tick_system.register_callback(on_tick)
tick_system.start()

# Main loop
while running:
    if tick_system.should_tick():
        tick_system.tick()
    time.sleep(0.01)  # Prevent CPU spinning
```

---

## Save/Load System

### Save File Format

Save files are JSON with the following structure:

```json
{
  "metadata": {
    "version": "1.0.0",
    "created_at": "2025-10-02T12:00:00",
    "last_saved": "2025-10-02T12:30:00",
    "total_playtime": 1800.0,
    "tick_count": 1800
  },
  "state": {
    "game": {
      "initialized": true
    }
  },
  "resources": {
    "gold": {
      "name": "gold",
      "amount": 250.5,
      "generation_rate": 1.0,
      ...
    }
  },
  "buildings": {
    "farm": {
      "name": "farm",
      "count": 3,
      ...
    }
  },
  "units": { ... },
  "upgrades": { ... }
}
```

### Save/Load Example

```python
# Save
game.save_game('saves/slot1.json')

# Load
game2 = GameState()
if game2.load_game('saves/slot1.json'):
    print("Loaded successfully!")
    print(f"Playtime: {game2.get_playtime_formatted()}")

# Get save info without loading
info = game.get_save_info('saves/slot1.json')
print(f"Last saved: {info['last_saved']}")
```

---

## Examples

### Example 1: Medieval Kingdom Setup

```python
game = GameState()
game.initialize()

# Resources
game.resources.add_resource('gold', initial=50, generation_rate=0.1)
game.resources.add_resource('wood', initial=100)
game.resources.add_resource('stone', initial=50)
game.resources.add_resource('food', initial=0)

# Buildings
game.buildings.register_building(
    'farm', cost={'wood': 30}, produces={'food': 1.0}, unlocked=True
)
game.buildings.register_building(
    'quarry', cost={'wood': 40, 'gold': 20},
    produces={'stone': 0.5}, unlocked=True
)
game.buildings.register_building(
    'castle', cost={'wood': 500, 'stone': 300},
    effects={'prestige': 100}, unlocked=False
)

# Units
game.units.register_unit(
    'peasant', cost={'food': 5}, produces={'gold': 0.2},
    upkeep={'food': 0.05}, unlocked=True
)
game.units.register_unit(
    'knight', cost={'gold': 100, 'food': 50},
    effects={'military': 10}, upkeep={'gold': 0.5}, unlocked=False
)

# Upgrades
game.upgrades.register_upgrade(
    'bronze_tools', cost={'gold': 50},
    effects={'production_bonus': 0.1}, unlocked=True
)
game.upgrades.register_upgrade(
    'iron_tools', cost={'gold': 200, 'stone': 100},
    effects={'production_bonus': 0.25},
    prerequisites=['bronze_tools'], unlocked=True
)
```

### Example 2: Applying Upgrade Bonuses

```python
# Get production bonus from upgrades
production_bonus = game.upgrades.get_effect_value('production_bonus')

# Apply to building production
base_production = game.buildings.get_total_production()
for resource, rate in base_production.items():
    boosted_rate = rate * (1 + production_bonus)
    print(f"{resource}: {rate}/s → {boosted_rate}/s")
```

### Example 3: Resource Generation with Effects

```python
def update_with_bonuses(game, delta_time):
    # Get all active bonuses
    effects = game.upgrades.get_all_effects()

    # Apply production bonus to resources
    production_mult = 1.0 + effects.get('production_bonus', 0)

    # Normal update
    game.update(delta_time)

    # Apply bonus to building production
    bonus_production = game.buildings.get_total_production()
    for resource, rate in bonus_production.items():
        bonus_amount = rate * production_mult * delta_time
        game.resources.add(resource, bonus_amount)
```

---

## Best Practices

1. **Always use ResourceManager for costs**: Don't manipulate resource amounts directly
2. **Check affordability before actions**: Use `can_afford()` before allowing purchases
3. **Use callbacks for UI updates**: Register callbacks to react to state changes
4. **Save regularly**: Implement auto-save every N ticks
5. **Validate save data**: Check save file compatibility before loading
6. **Log extensively**: All managers have built-in logging for debugging
7. **Use metadata for categorization**: Store categories in building/unit metadata for UI organization

---

## Logging

All modules use Python's standard logging. Configure it in your main game:

```python
import logging

logging.basicConfig(
    filename='game.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Log levels:
- **DEBUG**: Detailed state changes
- **INFO**: Important events (purchases, unlocks)
- **WARNING**: Potential issues (insufficient resources)
- **ERROR**: Failures and exceptions

---

## Contributing

When extending these modules:

1. Maintain comprehensive docstrings
2. Add logging for important events
3. Implement `to_dict()` and `from_dict()` for serialization
4. Write example usage in `if __name__ == "__main__"` blocks
5. Update this documentation

---

**End of Documentation**
