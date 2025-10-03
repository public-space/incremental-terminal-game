"""
Colony.sh Configuration
========================

Game settings and constants.
"""

import os

# Game info
GAME_NAME = "colony.sh"
GAME_VERSION = "1.0.0"
GAME_SUBTITLE = "Frontier Colony Survival Sim"

# Paths
SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")
DEFAULT_SAVE_FILE = os.path.join(SAVE_DIR, "colony_save.json")

# Timing
TICK_RATE = 1.0  # Game ticks per second
MAX_FPS = 30.0   # Frame rate cap
SOL_LENGTH = 60.0  # Seconds per Sol (day)

# UI
USE_COLORS = True
BORDER_STYLE = "double"  # UI border style

# Gameplay
STARTING_RESOURCES = {
    'energy': 20.0,
    'metal': 10.0,
    'biomass': 15.0,
    'colonists': 3.0,
}

# Debug
DEBUG_MODE = False
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR


def ensure_save_directory():
    """Create saves directory if it doesn't exist."""
    os.makedirs(SAVE_DIR, exist_ok=True)
