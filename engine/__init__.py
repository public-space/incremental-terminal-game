"""
Game Engine Package
===================

A modular, reusable game engine for terminal-based incremental/idle games.

Modules:
    - tick_system: Handles game loop timing and tick-based updates
    - state_manager: Manages game state and data structures
    - save_load: Serialization and persistence system
    - ui_framework: Terminal rendering, colors, and layout management
    - input_handler: User input processing and command routing
    - animator: ASCII animation utilities
"""

__version__ = "1.0.0"
__author__ = "Donovan & Claude"

from .tick_system import TickSystem
from .state_manager import StateManager
from .save_load import SaveLoadManager
from .ui_framework import UIFramework
from .input_handler import InputHandler
from .animator import Animator

__all__ = [
    'TickSystem',
    'StateManager',
    'SaveLoadManager',
    'UIFramework',
    'InputHandler',
    'Animator'
]
