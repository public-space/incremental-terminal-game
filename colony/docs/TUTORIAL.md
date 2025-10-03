# Colony.sh - Development Tutorial

**How this game was built, and how to build your own**

## Overview

This tutorial explains the architecture of colony.sh and shows you how to create your own terminal incremental game using the engine.

## Philosophy

### Separation of Concerns

```
engine/          → Reusable game systems (tick, UI, state)
colony/          → Game-specific implementation
  content/       → Data definitions (resources, buildings)
  systems/       → Game-specific logic (event log)
  ui/            → Game screens
  main.py        → Integration layer
```

**Key insight**: The engine knows nothing about "energy" or "colonists". It only knows about generic "resources" and "buildings". Game content is injected via data files.

### Data-Oriented Design

Instead of:
```python
class SolarArray(Building):
    def __init__(self):
        self.cost = {'metal': 5}
        self.produces = {'energy': 3.0}
```

We use:
```python
STRUCTURES = {
    'solar_array': {
        'cost': {'metal': 5},
        'produces': {'energy': 3.0}
    }
}
```

**Benefits**:
- No code changes to add content
- Easy to balance (edit numbers in one file)
- Can load from JSON/YAML later
- Designers can modify without touching code

## Architecture Deep Dive

### 1. Engine Layer

Located in `../engine/`

**Core systems**:

```python
TickSystem          # Fixed timestep game loop
StateManager        # Central game state
UIFramework         # Terminal rendering
InputHandler        # Command processing
Animator            # Visual effects
GameLoop            # Ties everything together
```

**Game modules**:

```python
ResourceManager     # Generic resource tracking
BuildingManager     # Generic building construction
UpgradeManager      # Generic research/upgrades
GameState           # Combines all managers
```

### 2. Content Layer

Located in `colony/content/`

**Purpose**: Define what the game is about

```python
# resources.py
RESOURCES = {
    'energy': {
        'name': 'energy',
        'display_name': '⚡ Energy',
        'amount': 20.0,
        'max_storage': 100.0
    }
}

# structures.py
STRUCTURES = {
    'solar_array': {
        'name': 'solar_array',
        'display_name': 'Solar Array',
        'cost': {'metal': 5},
        'production': {'energy': 3.0}
    }
}

# research.py
RESEARCH = {
    'efficient_extraction': {
        'name': 'efficient_extraction',
        'cost': {'metal': 30, 'energy': 20},
        'effects': {'metal_production_multiplier': 1.5}
    }
}
```

**loader.py**: Bridges data → engine

```python
def load_new_game() -> GameState:
    game_state = GameState()

    # Load resources
    for name, data in RESOURCES.items():
        game_state.resources.add_resource(**data)

    # Load buildings
    for name, data in STRUCTURES.items():
        # Convert data format to engine format
        converted = convert_structure_data(data)
        game_state.buildings.register_building(**converted)

    return game_state
```

### 3. Systems Layer

Located in `colony/systems/`

**Purpose**: Game-specific logic not in the engine

**Example: Event Log**

```python
@dataclass
class LogEntry:
    sol: int
    timestamp: str
    message: str
    category: str  # info, warning, critical, success

class EventLog:
    def __init__(self):
        self.entries: List[LogEntry] = []
        self.current_sol = 0

    def info(self, message: str):
        self.entries.append(LogEntry(
            sol=self.current_sol,
            timestamp=self._get_timestamp(),
            message=message,
            category='info'
        ))
```

### 4. UI Layer

Located in `colony/ui/`

**Purpose**: Visual presentation of game state

Each screen is a class:

```python
class MainScreen:
    def __init__(self, ui: UIFramework):
        self.ui = ui

    def render(self, game_state: GameState, event_log: EventLog):
        self.ui.clear_screen()
        self._render_header(game_state)
        self._render_resources(game_state)
        self._render_structures(game_state)
        self._render_event_log(event_log)
        self._render_footer()
```

**Separation of data and display**: UI never modifies game state, only reads it.

### 5. Integration Layer

Located in `colony/main.py`

**Purpose**: Wire engine + content + systems together

```python
class ColonyGame:
    def __init__(self):
        # Engine systems
        self.game_loop = GameLoop(tick_rate=1.0)

        # Game state
        self.game_state = load_new_game()

        # Game systems
        self.event_log = EventLog()

        # UI screens
        self.main_screen = MainScreen(self.game_loop.ui)

        # Hook up callbacks
        self.game_loop.register_update_callback(self._on_update)
        self.game_loop.register_render_callback(self._on_render)

    def _on_update(self, delta_time: float):
        # Update game state every tick
        self.game_state.update(delta_time)

        # Update Sol counter
        self.sol_timer += delta_time
        if self.sol_timer >= SOL_LENGTH:
            self.sol_timer = 0
            self.game_state.metadata['sol'] += 1

    def _on_render(self, ui, animator):
        # Render main screen
        self.main_screen.render(self.game_state, self.event_log)
```

## Step-by-Step: Building Your Own Game

### Step 1: Plan Your Theme

Questions to answer:
- What resources exist in your world?
- What buildings produce them?
- What research/upgrades make sense?
- What's the progression arc?

**Example for colony.sh**:

Theme: Dark sci-fi colony survival
- Resources: Energy (power), Metal (construction), Biomass (food), Colonists (workers)
- Buildings: Solar arrays, mining rigs, recycling bays
- Research: Efficiency multipliers
- Arc: Survive → Expand → Thrive

### Step 2: Define Content Files

Create `your_game/content/`:

```python
# resources.py
def get_resource_definitions():
    return {
        'wood': {
            'name': 'wood',
            'display_name': '🌲 Wood',
            'amount': 10.0,
            'max_storage': 100.0
        },
        'stone': {
            'name': 'stone',
            'display_name': '🪨 Stone',
            'amount': 5.0,
            'max_storage': 50.0
        }
    }

# structures.py
def get_structure_definitions():
    return {
        'sawmill': {
            'name': 'sawmill',
            'display_name': 'Sawmill',
            'cost': {'stone': 10},
            'production': {'wood': 1.0}
        }
    }
```

### Step 3: Create Content Loader

```python
# loader.py
def load_new_game() -> GameState:
    from engine import GameState

    game = GameState()

    # Load resources
    resources = get_resource_definitions()
    for name, data in resources.items():
        # Convert format
        converted = {
            'name': data['name'],
            'display_name': data['display_name'],
            'initial': data.get('amount', 0),
            'max_storage': data.get('max_storage', 1000),
            'metadata': data.get('metadata', {})
        }
        game.resources.add_resource(**converted)

    # Load buildings
    structures = get_structure_definitions()
    for name, data in structures.items():
        converted = {
            'name': data['name'],
            'display_name': data['display_name'],
            'cost': data.get('cost', {}),
            'produces': data.get('production', {}),
            'consumes': data.get('consumption', {}),
            'unlocked': data.get('unlocked', True)
        }
        game.buildings.register_building(**converted)

    return game
```

**Critical**: The loader converts YOUR data format → engine format. This is where compatibility happens.

### Step 4: Create UI Screens

```python
# ui/main_screen.py
from engine import UIFramework, Color

class MainScreen:
    def __init__(self, ui: UIFramework):
        self.ui = ui

    def render(self, game_state):
        self.ui.clear_screen()

        # Header
        self.ui.print_colored("=== YOUR GAME ===", Color.BRIGHT_CYAN)

        # Resources
        self.ui.print_colored("\nRESOURCES:", Color.BRIGHT_WHITE)
        for name, resource in game_state.resources.resources.items():
            display = f"{resource.display_name}: {resource.amount:.1f}/{resource.max_storage}"
            color = Color.GREEN if resource.amount > 0 else Color.RED
            self.ui.print_colored(f"  {display}", color)
```

### Step 5: Wire Game Loop

```python
# main.py
from engine import GameLoop
from content.loader import load_new_game
from ui.main_screen import MainScreen

class YourGame:
    def __init__(self):
        self.game_loop = GameLoop(tick_rate=1.0)
        self.game_state = load_new_game()
        self.main_screen = MainScreen(self.game_loop.ui)

        self.game_loop.register_update_callback(self._update)
        self.game_loop.register_render_callback(self._render)

    def _update(self, dt):
        self.game_state.update(dt)

    def _render(self, ui, animator):
        self.main_screen.render(self.game_state)

    def run(self):
        self.game_loop.run()

if __name__ == "__main__":
    game = YourGame()
    game.run()
```

### Step 6: Add Commands

```python
def _setup_commands(self):
    handler = self.game_loop.input_handler

    def cmd_build(args):
        # Show build menu, handle construction
        pass

    def cmd_save(args):
        self.game_state.save_game('saves/game.json')
        print("Game saved!")

    handler.register_command('build', cmd_build, 'Build structures', aliases=['b'])
    handler.register_command('save', cmd_save, 'Save game', aliases=['s'])
```

## Advanced Patterns

### Custom Game Systems

Sometimes you need logic that's game-specific:

```python
# systems/weather.py
class WeatherSystem:
    def __init__(self):
        self.current_weather = 'sunny'
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer > 60:  # Change every minute
            self.current_weather = random.choice(['sunny', 'rain', 'snow'])
            self.timer = 0

    def get_production_modifier(self):
        return {
            'sunny': 1.2,
            'rain': 1.0,
            'snow': 0.8
        }[self.current_weather]
```

Then in your game:

```python
class YourGame:
    def __init__(self):
        # ...
        self.weather = WeatherSystem()

    def _update(self, dt):
        self.weather.update(dt)

        # Apply weather modifier to production
        base_prod = self.game_state.buildings.get_total_production()
        modifier = self.weather.get_production_modifier()
        for resource, amount in base_prod.items():
            base_prod[resource] *= modifier
```

### Event System

Trigger events based on game state:

```python
class EventSystem:
    def __init__(self):
        self.events = []

    def check_events(self, game_state):
        # Low energy warning
        if game_state.resources.get_amount('energy') < 10:
            self.trigger_event('low_energy', 'WARNING: Energy critical!')

        # Milestone events
        if game_state.buildings.get_count('sawmill') >= 10:
            self.trigger_event('milestone', 'Achievement: Lumber Baron!')

    def trigger_event(self, category, message):
        self.events.append({'category': category, 'message': message})
```

### Unlock System

Gate content behind conditions:

```python
def update_unlocks(self, game_state):
    # Unlock advanced research if player has 5 of each building
    if all(b.count >= 5 for b in game_state.buildings.buildings.values()):
        game_state.upgrades.unlock('advanced_tech')

    # Unlock special building if research complete
    if game_state.upgrades.is_purchased('fusion_power'):
        game_state.buildings.unlock('fusion_reactor')
```

## Common Patterns

### Building Menus

Pattern for any selection menu:

```python
def show_menu(self, items, game_state):
    # Display items with numbers
    for idx, (name, item) in enumerate(items, 1):
        affordable = can_afford(item.cost, game_state)
        color = GREEN if affordable else RED
        print(f"[{idx}] {item.display_name} - Cost: {item.cost}")

    # Get choice
    choice = input("> ")

    # Validate and execute
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            name, item = items[idx]
            return self.execute_choice(name, item, game_state)
    except ValueError:
        return False, "Invalid input"
```

### Production Display

Show rates per second:

```python
def display_production(self, game_state):
    production = game_state.buildings.get_total_production()
    consumption = game_state.buildings.get_total_consumption()

    for resource in game_state.resources.resources.keys():
        prod = production.get(resource, 0)
        cons = consumption.get(resource, 0)
        net = prod - cons

        print(f"{resource}: {net:+.2f}/s (↑{prod:.1f} ↓{cons:.1f})")
```

### Save/Load Integration

```python
def save_game(self, filepath):
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save using engine method
        success = self.game_state.save_game(filepath)

        if success:
            self.event_log.success("Colony data archived")
        else:
            self.event_log.critical("Archive failed")
    except Exception as e:
        self.event_log.critical(f"Error: {e}")
```

## Debugging Tips

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game_debug.log'),
        logging.StreamHandler()
    ]
)
```

### Add Debug Commands

```python
def cmd_debug(args):
    if args and args[0] == 'resources':
        # Give player tons of resources for testing
        for resource in self.game_state.resources.resources.values():
            resource.amount = resource.max_storage
        print("DEBUG: Resources maxed")

    elif args and args[0] == 'unlock':
        # Unlock everything
        for building in self.game_state.buildings.buildings.values():
            building.unlocked = True
        for upgrade in self.game_state.upgrades.upgrades.values():
            upgrade.unlocked = True
        print("DEBUG: Everything unlocked")

handler.register_command('debug', cmd_debug, 'Debug commands')
```

### Test Each Layer

```python
# Test content loading
if __name__ == "__main__":
    game = load_new_game()
    print(f"Loaded {len(game.resources.resources)} resources")
    print(f"Loaded {len(game.buildings.buildings)} buildings")
```

## Performance Considerations

### Tick Rate vs Render Rate

```python
TICK_RATE = 60  # Physics update (fast)
RENDER_RATE = 5  # Display update (slow)

# In game loop:
def _on_render(self, ui, animator):
    self.render_timer += 1/60
    if self.render_timer < 1/5:  # Only render at 5 FPS
        return

    self.render_timer = 0
    # Actual rendering here
```

**Why?** Updating the game 60 times/second keeps resources flowing smoothly. But clearing/redrawing the screen that often causes flicker.

### Cache Production Calculations

```python
def update(self, dt):
    # Calculate once per tick
    if not hasattr(self, '_cached_production'):
        self._cached_production = self.calculate_production()

    # Use cached value
    for resource, rate in self._cached_production.items():
        self.resources.add(resource, rate * dt)

# Invalidate cache when buildings change
def on_building_built(self):
    self._cached_production = None  # Force recalculation
```

## Extending Colony.sh

Want to add features to colony.sh? Here's how:

### Add New Resource

```python
# In content/resources.py
RESOURCES['data'] = {
    'name': 'data',
    'display_name': '💾 Data',
    'description': 'Corrupted archives. Fragments of knowledge.',
    'amount': 0.0,
    'max_storage': 200.0,
    'metadata': {'icon': '💾', 'color': 'blue'}
}
```

That's it! Engine handles the rest.

### Add New Building

```python
# In content/structures.py
STRUCTURES['data_center'] = {
    'name': 'data_center',
    'display_name': 'Data Center',
    'description': 'Processes ancient signals. Something listens.',
    'cost': {'metal': 25, 'energy': 20},
    'production': {'data': 0.5},
    'consumption': {'energy': 5.0},
    'unlocked': True,
    'metadata': {
        'icon': '💾',
        'flavor': 'The servers hum. The patterns... they repeat.'
    }
}
```

### Add Random Events

```python
# In systems/ create events.py
class RandomEvents:
    def __init__(self):
        self.timer = 0
        self.events = [
            {'name': 'solar_flare', 'chance': 0.1, 'effect': 'lose_energy'},
            {'name': 'mineral_vein', 'chance': 0.15, 'effect': 'gain_metal'}
        ]

    def update(self, dt, game_state, event_log):
        self.timer += dt
        if self.timer > 120:  # Check every 2 minutes
            self.timer = 0
            self.check_random_event(game_state, event_log)

    def check_random_event(self, game_state, event_log):
        for event in self.events:
            if random.random() < event['chance']:
                self.trigger_event(event, game_state, event_log)
```

## Final Tips

1. **Start with data** - Define your content first, implement systems later
2. **Test incrementally** - Test content loading, then UI, then integration
3. **Use the engine** - Don't reinvent resource tracking, use ResourceManager
4. **Keep it modular** - Each system should work independently
5. **Document as you go** - Update MECHANICS.md when you add content
6. **Balance through iteration** - Playtest and adjust numbers
7. **Theme consistency** - Make sure flavor text matches your world

## Resources

- **Engine source**: `../engine/` - Read the docstrings
- **This game**: `colony/` - Working example
- **Engine README**: `../engine/README.md` - API reference

---

*Now go build something amazing. The void awaits.*
