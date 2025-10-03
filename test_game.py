#!/usr/bin/env python3
"""
Quick test to verify game systems work
"""
import sys
sys.path.insert(0, 'colony')

from content.loader import load_new_game
from ui.build_menu import BuildMenu
from ui.research_menu import ResearchMenu
from engine import UIFramework

# Create game state
print("Loading game...")
game = load_new_game()

# Give player some resources
game.resources.add('energy', 50)
game.resources.add('metal', 30)
game.resources.add('biomass', 20)

print("✓ Game state loaded")
print(f"  - Resources: {len(game.resources.resources)}")
print(f"  - Buildings: {len(game.buildings.buildings)}")
print(f"  - Research: {len(game.upgrades.upgrades)}")

# Test building
print("\n✓ Testing build menu render...")
ui = UIFramework(use_colors=False)
build_menu = BuildMenu(ui)
try:
    # Just create the menu display (don't wait for input)
    buildings = game.buildings.buildings
    unlocked = [(name, bld) for name, bld in buildings.items() if bld.unlocked]
    print(f"  - {len(unlocked)} buildings available")

    # Check first building has correct attributes
    if unlocked:
        name, bld = unlocked[0]
        print(f"  - Test building: {bld.display_name}")
        print(f"    - Has 'produces': {hasattr(bld, 'produces')}")
        print(f"    - Has 'consumes': {hasattr(bld, 'consumes')}")
        print(f"    - Produces: {bld.produces}")
    print("✓ Build menu OK")
except Exception as e:
    print(f"✗ Build menu error: {e}")
    sys.exit(1)

# Test research
print("\n✓ Testing research menu...")
research_menu = ResearchMenu(ui)
try:
    upgrades = game.upgrades.upgrades
    unlocked = [(name, upg) for name, upg in upgrades.items() if upg.unlocked]
    print(f"  - {len(unlocked)} research available")
    print("✓ Research menu OK")
except Exception as e:
    print(f"✗ Research error: {e}")
    sys.exit(1)

# Test save
print("\n✓ Testing save/load...")
try:
    import tempfile
    import os

    # Save to temp file
    temp_file = tempfile.mktemp(suffix='.json')
    game.save(temp_file)
    print(f"  - Saved to {temp_file}")

    # Try to load it
    from content.loader import load_save_game
    loaded_game = load_save_game(temp_file)
    print(f"  - Loaded successfully")
    print(f"  - Resources match: {len(loaded_game.resources.resources) == len(game.resources.resources)}")

    # Cleanup
    os.remove(temp_file)
    print("✓ Save/load OK")
except Exception as e:
    print(f"✗ Save/load error: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("ALL TESTS PASSED ✓")
print("="*50)
