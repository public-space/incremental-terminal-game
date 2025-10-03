"""
Content Loader
==============

Loads game content definitions into engine systems.
Bridges data-oriented content with engine managers.
"""

import sys
import os

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from engine import ResourceManager, BuildingManager, UpgradeManager, GameState

# Handle imports for both module and direct execution
try:
    from .resources import get_resource_definitions, get_starting_resources
    from .structures import get_structure_definitions, get_starting_structures
    from .research import get_research_definitions
except ImportError:
    from resources import get_resource_definitions, get_starting_resources
    from structures import get_structure_definitions, get_starting_structures
    from research import get_research_definitions


def load_game_content() -> GameState:
    """
    Load all colony.sh content into a new GameState.

    Returns:
        GameState: Initialized game state with all content loaded
    """
    # Create game state
    game_state = GameState()

    # Load resources
    resource_defs = get_resource_definitions()
    for res_name, res_data in resource_defs.items():
        # Convert 'amount' to 'initial' for add_resource
        data = res_data.copy()
        if 'amount' in data:
            data['initial'] = data.pop('amount')
        game_state.resources.add_resource(**data)

    # Load buildings (structures)
    structure_defs = get_structure_definitions()
    for struct_name, struct_data in structure_defs.items():
        # Convert 'production' to 'produces' and 'consumption' to 'consumes'
        data = struct_data.copy()
        if 'production' in data:
            data['produces'] = data.pop('production')
        if 'consumption' in data:
            data['consumes'] = data.pop('consumption')
        # Remove 'count' as that's not a registration parameter
        data.pop('count', None)
        game_state.buildings.register_building(**data)

    # Load research (upgrades)
    research_defs = get_research_definitions()
    for research_name, research_data in research_defs.items():
        # Remove 'purchased' as that's state, not definition
        data = research_data.copy()
        data.pop('purchased', None)
        game_state.upgrades.register_upgrade(**data)

    return game_state


def load_new_game() -> GameState:
    """
    Load a new game with starting resources and structures.

    Returns:
        GameState: New game with starting conditions
    """
    game_state = load_game_content()

    # Set starting resources
    starting_resources = get_starting_resources()
    for resource, amount in starting_resources.items():
        game_state.resources.set_amount(resource, amount)

    # Set starting structures
    starting_structures = get_starting_structures()
    for structure, count in starting_structures.items():
        building = game_state.buildings.get_building(structure)
        if building:
            building.count = count

    # Initialize metadata
    game_state.metadata['game_name'] = 'colony.sh'
    game_state.metadata['sol'] = 0  # Day counter
    game_state.metadata['started'] = True

    return game_state


def load_save_game(save_file: str) -> GameState:
    """
    Load a game from save file.

    Args:
        save_file: Path to save file

    Returns:
        GameState: Loaded game state

    Raises:
        FileNotFoundError: If save file doesn't exist
        ValueError: If save file is corrupted
    """
    game_state = load_game_content()
    game_state.load_game(save_file)
    return game_state


# Example usage
if __name__ == "__main__":
    print("=== COLONY.SH CONTENT LOADER TEST ===\n")

    # Load new game
    game = load_new_game()

    print("Starting Resources:")
    for res_name, resource in game.resources.resources.items():
        print(f"  {resource.display_name}: {resource.amount:.1f}/{resource.max_storage}")

    print("\nStarting Structures:")
    for struct_name, building in game.buildings.buildings.items():
        if building.count > 0:
            print(f"  {building.display_name}: {building.count}")

    print("\nAvailable Research:")
    for research_name, upgrade in game.upgrades.upgrades.items():
        cost_str = ", ".join([f"{amt:.0f} {res}" for res, amt in upgrade.cost.items()])
        print(f"  {upgrade.display_name} - Cost: {cost_str}")

    print("\n✓ Content loaded successfully!")
