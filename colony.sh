#!/usr/bin/env python3
"""
colony.sh launcher
==================

Launches the colony.sh frontier survival game.
"""

import sys
import os

# Add colony directory to path
game_dir = os.path.join(os.path.dirname(__file__), 'colony')
sys.path.insert(0, game_dir)

# Run the game
if __name__ == "__main__":
    from main import main
    main()
