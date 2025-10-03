"""
Medieval Kingdom Game Package
==============================

Game-specific implementation for the Medieval Kingdom idle game.

Modules:
    - resources: Resource types and generation logic
    - buildings: Building definitions and production mechanics
    - units: Worker and unit types
    - upgrades: Upgrade system and tech tree
    - events: Random events and special occurrences
    - game_state: Game-specific state management
"""

__version__ = "1.0.0"
__game_name__ = "Medieval Kingdom"

from .resources import ResourceManager
from .buildings import BuildingManager
from .units import UnitManager
from .upgrades import UpgradeManager
from .game_state import GameState

__all__ = [
    'ResourceManager',
    'BuildingManager',
    'UnitManager',
    'UpgradeManager',
    'GameState'
]
