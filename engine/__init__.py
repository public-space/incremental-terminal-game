"""
Game Engine Package
===================

A modular, reusable game engine for terminal-based incremental/idle games.

Modules:
    - tick_system: Handles game loop timing and tick-based updates
    - state_manager: Manages game state and data structures
    - ui_framework: Terminal rendering, colors, and layout management
    - input_handler: User input processing and command routing
    - animator: ASCII animation utilities
    - game_loop: Main game loop controller
"""

__version__ = "1.0.0"
__author__ = "Donovan & Claude"

from .tick_system import TickSystem
from .state_manager import StateManager
from .ui_framework import UIFramework, Color, Panel, BorderStyle
from .input_handler import InputHandler, Command
from .animator import Animator, Animation, AnimationType
from .game_loop import GameLoop, GameState

__all__ = [
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
    'GameState'
]
