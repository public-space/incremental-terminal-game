"""
Game Engine Package
===================

A modular, reusable game engine for terminal-based incremental/idle games.

Core Systems:
    - tick_system: Handles game loop timing and tick-based updates
    - state_manager: Manages game state and data structures
    - ui_framework: Terminal rendering, colors, and layout management
    - input_handler: User input processing and command routing
    - animator: ASCII animation utilities
    - game_loop: Main game loop controller

Game Systems (Generic, Reusable):
    - resources: Resource management system
    - buildings: Building construction and production
    - units: Worker/unit management
    - upgrades: Technology tree and upgrades
    - game_state: Complete game state coordinator
"""

__version__ = "1.0.0"
__author__ = "Donovan & Claude"

# Core engine systems
from .tick_system import TickSystem
from .state_manager import StateManager
from .ui_framework import UIFramework, Color, Panel, BorderStyle
from .input_handler import InputHandler, Command
from .animator import Animator, Animation, AnimationType
from .game_loop import GameLoop, GameState as GameLoopState

# Generic game systems
from .resources import ResourceManager
from .buildings import BuildingManager
from .units import UnitManager
from .upgrades import UpgradeManager
from .game_state import GameState

__all__ = [
    # Core engine
    'TickSystem',
    'StateManager',
    'UIFramework',
    'Color',
    'Panel',
    'BorderStyle',
    'InputHandler',
    'Command',
    'Animator',
    'Animation',
    'AnimationType',
    'GameLoop',
    'GameLoopState',
    # Game systems
    'ResourceManager',
    'BuildingManager',
    'UnitManager',
    'UpgradeManager',
    'GameState',
]
