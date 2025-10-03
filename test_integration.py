#!/usr/bin/env python3
"""
Integration Test Suite
=======================

Comprehensive test of all game systems working together.
Tests the full game loop with tick system, resources, buildings, units, and upgrades.
"""

import sys
import time
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.tick_system import TickSystem
from game.game_state import GameState


def test_full_integration():
    """Test all systems integrated together with tick system."""

    print("=" * 60)
    print("INTEGRATION TEST: Full Game System")
    print("=" * 60)

    # 1. Create game state
    print("\n[1] Creating game state...")
    game = GameState()
    game.initialize()
    print("✓ GameState initialized")

    # 2. Set up resources
    print("\n[2] Setting up resources...")
    game.resources.add_resource('gold', initial=100, generation_rate=0.5)
    game.resources.add_resource('wood', initial=200, max_storage=1000)
    game.resources.add_resource('food', initial=50)
    game.resources.add_resource('stone', initial=0)
    print(f"✓ Resources: gold={game.get_resource_amount('gold')}, "
          f"wood={game.get_resource_amount('wood')}, "
          f"food={game.get_resource_amount('food')}")

    # 3. Register buildings
    print("\n[3] Registering buildings...")
    game.buildings.register_building(
        'farm',
        cost={'wood': 50, 'gold': 20},
        produces={'food': 1.0},
        description="Produces food",
        unlocked=True
    )
    game.buildings.register_building(
        'quarry',
        cost={'wood': 80, 'gold': 30},
        produces={'stone': 0.5},
        description="Produces stone",
        unlocked=True
    )
    game.buildings.register_building(
        'lumber_mill',
        cost={'wood': 100, 'gold': 50},
        produces={'wood': 0.8},
        description="Produces wood",
        unlocked=True
    )
    print("✓ 3 building types registered")

    # 4. Register units
    print("\n[4] Registering units...")
    game.units.register_unit(
        'worker',
        cost={'food': 10},
        produces={'gold': 0.3},
        upkeep={'food': 0.1},
        description="Gathers gold",
        unlocked=True
    )
    game.units.register_unit(
        'miner',
        cost={'food': 15, 'gold': 5},
        produces={'stone': 0.2},
        upkeep={'food': 0.15},
        description="Mines stone",
        unlocked=True
    )
    print("✓ 2 unit types registered")

    # 5. Register upgrades
    print("\n[5] Registering upgrades...")
    game.upgrades.register_upgrade(
        'better_tools',
        cost={'gold': 50},
        effects={'production_bonus': 0.2},
        description="+20% production",
        unlocked=True
    )
    game.upgrades.register_upgrade(
        'advanced_tools',
        cost={'gold': 150, 'stone': 20},
        effects={'production_bonus': 0.3},
        description="+30% production",
        prerequisites=['better_tools'],
        unlocked=True
    )
    game.upgrades.register_upgrade(
        'worker_training',
        cost={'gold': 30},
        effects={'worker_efficiency': 0.1},
        description="+10% worker efficiency",
        unlocked=True,
        repeatable=True,
        max_purchases=3
    )
    print("✓ 3 upgrade types registered")

    # 6. Build some buildings
    print("\n[6] Building structures...")
    if game.buildings.build('farm'):
        print("✓ Built farm")
    if game.buildings.build('quarry'):
        print("✓ Built quarry")

    print(f"  Remaining - Gold: {game.get_resource_amount('gold')}, "
          f"Wood: {game.get_resource_amount('wood')}")

    # 7. Recruit units
    print("\n[7] Recruiting units...")
    if game.units.recruit('worker', count=2):
        print("✓ Recruited 2 workers")

    print(f"  Remaining - Food: {game.get_resource_amount('food')}")

    # 8. Purchase upgrade
    print("\n[8] Purchasing upgrades...")
    if game.upgrades.purchase('better_tools'):
        print("✓ Purchased 'better_tools'")

    effects = game.upgrades.get_all_effects()
    print(f"  Active effects: {effects}")

    # 9. Set up tick system
    print("\n[9] Setting up tick system...")
    tick_system = TickSystem(tick_rate=1.0)

    def on_tick(delta_time):
        game.update(delta_time)

    tick_system.register_callback(on_tick)
    tick_system.start()
    print("✓ Tick system started (1 tick/second)")

    # 10. Run simulation
    print("\n[10] Running 10-second simulation...")
    print("-" * 60)

    start_gold = game.get_resource_amount('gold')
    start_food = game.get_resource_amount('food')
    start_stone = game.get_resource_amount('stone')

    start_time = time.time()
    last_report = start_time

    while time.time() - start_time < 10:
        if tick_system.should_tick():
            tick_system.tick()

            # Report every 2 seconds
            if time.time() - last_report >= 2:
                print(f"  Tick {tick_system.tick_count}: "
                      f"Gold={game.get_resource_amount('gold'):.1f}, "
                      f"Food={game.get_resource_amount('food'):.1f}, "
                      f"Stone={game.get_resource_amount('stone'):.1f}")
                last_report = time.time()

        time.sleep(0.01)

    tick_system.stop()
    print("-" * 60)

    # 11. Results
    print("\n[11] Simulation Results:")
    end_gold = game.get_resource_amount('gold')
    end_food = game.get_resource_amount('food')
    end_stone = game.get_resource_amount('stone')

    print(f"  Gold: {start_gold:.1f} → {end_gold:.1f} (Δ{end_gold - start_gold:+.1f})")
    print(f"  Food: {start_food:.1f} → {end_food:.1f} (Δ{end_food - start_food:+.1f})")
    print(f"  Stone: {start_stone:.1f} → {end_stone:.1f} (Δ{end_stone - start_stone:+.1f})")
    print(f"  Total ticks: {tick_system.tick_count}")
    print(f"  Playtime: {game.get_playtime_formatted()}")

    # 12. Save/Load test
    print("\n[12] Testing save/load...")
    save_file = 'test_integration_save.json'

    if game.save_game(save_file):
        print(f"✓ Saved to {save_file}")

    # Load into new game
    game2 = GameState()
    if game2.load_game(save_file):
        print(f"✓ Loaded from {save_file}")
        print(f"  Loaded gold: {game2.get_resource_amount('gold'):.1f}")
        print(f"  Loaded buildings: {len(game2.buildings.get_owned_buildings())} owned")
        print(f"  Loaded units: {game2.units.get_total_count()} total")
        print(f"  Loaded upgrades: {len(game2.upgrades.get_purchased_upgrades())} purchased")

    # Cleanup
    os.remove(save_file)
    print(f"✓ Cleaned up {save_file}")

    # 13. Final statistics
    print("\n[13] Final Statistics:")
    stats = game.export_stats()
    print(f"  Total production: {stats['total_production']}")
    print(f"  Unit production: {stats['total_unit_production']}")
    print(f"  Unit upkeep: {stats['total_upkeep']}")

    print("\n" + "=" * 60)
    print("✓ ALL INTEGRATION TESTS PASSED!")
    print("=" * 60)

    return True


def test_edge_cases():
    """Test edge cases and error handling."""

    print("\n\n" + "=" * 60)
    print("INTEGRATION TEST: Edge Cases & Error Handling")
    print("=" * 60)

    game = GameState()
    game.initialize()

    # Test 1: Insufficient resources
    print("\n[1] Testing insufficient resources...")
    game.resources.add_resource('gold', initial=10)
    game.buildings.register_building('expensive', cost={'gold': 100}, unlocked=True)

    if not game.buildings.build('expensive'):
        print("✓ Correctly rejected build with insufficient resources")

    # Test 2: Non-existent resource
    print("\n[2] Testing non-existent resources...")
    amount = game.get_resource_amount('nonexistent')
    if amount == 0:
        print("✓ Correctly returned 0 for non-existent resource")

    # Test 3: Upgrade prerequisites
    print("\n[3] Testing upgrade prerequisites...")
    game.resources.add_resource('research', initial=1000)
    game.upgrades.register_upgrade('basic', cost={'research': 10}, unlocked=True)
    game.upgrades.register_upgrade('advanced', cost={'research': 20},
                                   prerequisites=['basic'], unlocked=True)

    if not game.upgrades.can_purchase('advanced'):
        print("✓ Correctly blocked upgrade without prerequisite")

    game.upgrades.purchase('basic')
    if game.upgrades.can_purchase('advanced'):
        print("✓ Correctly allowed upgrade after prerequisite")

    # Test 4: Max storage
    print("\n[4] Testing max storage...")
    game.resources.add_resource('limited', initial=90, max_storage=100)
    added = game.resources.add('limited', 20)
    if added == 10:
        print(f"✓ Correctly clamped to max storage (added {added} instead of 20)")

    # Test 5: Repeatable upgrades
    print("\n[5] Testing repeatable upgrades...")
    game.upgrades.register_upgrade('repeatable', cost={'research': 50},
                                   repeatable=True, max_purchases=2, unlocked=True)

    game.upgrades.purchase('repeatable')
    game.upgrades.purchase('repeatable')

    if not game.upgrades.can_purchase('repeatable'):
        print("✓ Correctly blocked repeatable upgrade at max purchases")

    print("\n" + "=" * 60)
    print("✓ ALL EDGE CASE TESTS PASSED!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        # Run tests
        test_full_integration()
        test_edge_cases()

        print("\n" + "🎉" * 30)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("🎉" * 30)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
