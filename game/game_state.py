"""
Game State Module
==================

Central game state management that coordinates all game systems.
Handles save/load, game progression, and system integration.

Classes:
    GameState: Main game state coordinator

Usage:
    game = GameState()
    game.initialize()
    game.update(delta_time=1.0)
    game.save_game('savegame.json')
    game.load_game('savegame.json')
"""

import logging
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from .resources import ResourceManager
from .buildings import BuildingManager
from .units import UnitManager
from .upgrades import UpgradeManager
from engine.state_manager import StateManager

logger = logging.getLogger(__name__)


class GameState:
    """
    Central game state coordinator that manages all game systems.

    Attributes:
        resources (ResourceManager): Resource management system
        buildings (BuildingManager): Building management system
        units (UnitManager): Unit management system
        upgrades (UpgradeManager): Upgrade management system
        state (StateManager): Generic state storage
        metadata (dict): Game metadata (version, playtime, etc.)
    """

    def __init__(self):
        """Initialize the game state and all subsystems."""
        # Core managers
        self.state = StateManager()
        self.resources = ResourceManager()
        self.buildings = BuildingManager(resource_manager=self.resources)
        self.units = UnitManager(resource_manager=self.resources)
        self.upgrades = UpgradeManager(resource_manager=self.resources)

        # Game metadata
        self.metadata: Dict[str, Any] = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'last_saved': None,
            'total_playtime': 0.0,
            'tick_count': 0
        }

        logger.info("GameState initialized")

    def initialize(self):
        """
        Initialize the game with starting state.
        This sets up the initial game configuration.
        """
        logger.info("Initializing new game...")

        # Set up initial metadata
        self.state.set('game.initialized', True)
        self.state.set('game.started_at', datetime.now().isoformat())

        # This method should be overridden or extended by specific game implementations
        # to set up their starting resources, buildings, etc.

        logger.info("Game initialization complete")

    def update(self, delta_time: float):
        """
        Update all game systems.

        Args:
            delta_time: Time elapsed since last update (seconds)
        """
        try:
            # Update playtime
            self.metadata['total_playtime'] += delta_time
            self.metadata['tick_count'] += 1

            # Update resource generation
            self.resources.generate(delta_time)

            # Update building production
            self.buildings.update_production(delta_time)

            # Update unit production and upkeep
            self.units.update_production(delta_time)

            logger.debug(f"Game updated (Δt={delta_time:.3f}s)")

        except Exception as e:
            logger.error(f"Error during game update: {e}", exc_info=True)
            raise

    def can_afford(self, costs: Dict[str, float]) -> bool:
        """
        Check if player can afford a cost.

        Args:
            costs: Dictionary of {resource: amount}

        Returns:
            bool: True if affordable
        """
        return self.resources.can_afford(costs)

    def get_resource_amount(self, resource: str) -> float:
        """
        Get amount of a resource.

        Args:
            resource: Resource name

        Returns:
            float: Resource amount
        """
        return self.resources.get_amount(resource)

    def save_game(self, filepath: str) -> bool:
        """
        Save game state to file.

        Args:
            filepath: Path to save file

        Returns:
            bool: True if successful
        """
        try:
            # Prepare save data
            save_data = {
                'metadata': {
                    **self.metadata,
                    'last_saved': datetime.now().isoformat()
                },
                'state': self.state.get_all(),
                'resources': self.resources.to_dict(),
                'buildings': self.buildings.to_dict(),
                'units': self.units.to_dict(),
                'upgrades': self.upgrades.to_dict()
            }

            # Ensure directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            # Write to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)

            self.metadata['last_saved'] = save_data['metadata']['last_saved']
            logger.info(f"Game saved to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save game: {e}", exc_info=True)
            return False

    def load_game(self, filepath: str) -> bool:
        """
        Load game state from file.

        Args:
            filepath: Path to save file

        Returns:
            bool: True if successful
        """
        try:
            if not os.path.exists(filepath):
                logger.error(f"Save file not found: {filepath}")
                return False

            # Read from file
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            # Validate save data
            if not self._validate_save_data(save_data):
                logger.error("Invalid save data format")
                return False

            # Load metadata
            if 'metadata' in save_data:
                self.metadata.update(save_data['metadata'])

            # Load state
            if 'state' in save_data:
                self.state.set_all(save_data['state'])

            # Load subsystems
            if 'resources' in save_data:
                self.resources.from_dict(save_data['resources'])

            if 'buildings' in save_data:
                self.buildings.from_dict(save_data['buildings'])

            if 'units' in save_data:
                self.units.from_dict(save_data['units'])

            if 'upgrades' in save_data:
                self.upgrades.from_dict(save_data['upgrades'])

            logger.info(f"Game loaded from {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to load game: {e}", exc_info=True)
            return False

    def _validate_save_data(self, data: dict) -> bool:
        """
        Validate save data structure.

        Args:
            data: Save data dictionary

        Returns:
            bool: True if valid
        """
        required_keys = ['metadata', 'resources', 'buildings', 'units', 'upgrades']
        return all(key in data for key in required_keys)

    def export_stats(self) -> Dict[str, Any]:
        """
        Export game statistics.

        Returns:
            dict: Game statistics
        """
        return {
            'metadata': self.metadata,
            'resources': {
                name: resource.amount
                for name, resource in self.resources.resources.items()
            },
            'buildings': {
                name: building.count
                for name, building in self.buildings.buildings.items()
            },
            'units': {
                name: unit.count
                for name, unit in self.units.units.items()
            },
            'upgrades_purchased': [
                upgrade.name
                for upgrade in self.upgrades.get_purchased_upgrades()
            ],
            'total_production': self.buildings.get_total_production(),
            'total_unit_production': self.units.get_total_production(),
            'total_upkeep': self.units.get_total_upkeep()
        }

    def reset(self):
        """Reset the entire game state."""
        self.resources.reset()
        self.buildings.reset()
        self.units.reset()
        self.upgrades.reset()
        self.state.clear()

        self.metadata = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'last_saved': None,
            'total_playtime': 0.0,
            'tick_count': 0
        }

        logger.info("Game state reset")

    def get_playtime_formatted(self) -> str:
        """
        Get formatted playtime string.

        Returns:
            str: Formatted playtime (e.g., "1h 23m 45s")
        """
        total_seconds = int(self.metadata['total_playtime'])
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def get_save_info(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a save file without loading it.

        Args:
            filepath: Path to save file

        Returns:
            dict or None: Save file metadata
        """
        try:
            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r') as f:
                save_data = json.load(f)

            return save_data.get('metadata', {})

        except Exception as e:
            logger.error(f"Failed to read save info: {e}", exc_info=True)
            return None

    def auto_save(self, save_dir: str = 'saves', filename: str = 'autosave.json') -> bool:
        """
        Perform an automatic save.

        Args:
            save_dir: Directory for save files
            filename: Name of autosave file

        Returns:
            bool: True if successful
        """
        filepath = os.path.join(save_dir, filename)
        return self.save_game(filepath)

    def __repr__(self) -> str:
        """String representation of game state."""
        return (
            f"GameState(playtime={self.get_playtime_formatted()}, "
            f"ticks={self.metadata['tick_count']}, "
            f"resources={len(self.resources.resources)}, "
            f"buildings={len(self.buildings.buildings)}, "
            f"units={len(self.units.units)})"
        )


# Example usage
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from game.resources import ResourceManager
    from game.buildings import BuildingManager
    from game.units import UnitManager
    from game.upgrades import UpgradeManager
    from engine.state_manager import StateManager

    # Create new game
    game = GameState()
    game.initialize()

    # Add some example resources
    game.resources.add_resource('gold', initial=100, generation_rate=1.0)
    game.resources.add_resource('wood', initial=50)

    # Add example building
    game.buildings.register_building(
        'farm',
        cost={'wood': 30},
        produces={'gold': 0.5},
        unlocked=True
    )

    # Build something
    game.buildings.build('farm')

    # Simulate game updates
    print("Initial state:", game)
    for _ in range(5):
        game.update(delta_time=1.0)

    print("After 5 ticks:", game)
    print("Gold:", game.get_resource_amount('gold'))

    # Save game
    game.save_game('test_save.json')

    # Create new game and load
    game2 = GameState()
    game2.load_game('test_save.json')
    print("Loaded game:", game2)
    print("Loaded gold:", game2.get_resource_amount('gold'))

    # Export stats
    print("\nStats:", json.dumps(game2.export_stats(), indent=2))

    # Cleanup
    import os
    os.remove('test_save.json')
