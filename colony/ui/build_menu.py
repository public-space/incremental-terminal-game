"""
Build Menu
==========

Structure construction interface for colony.sh.
"""

import sys
import os

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from engine import UIFramework, Color, GameState
from typing import List, Tuple


class BuildMenu:
    """
    Building construction menu.

    Displays available structures with costs and allows construction.
    """

    def __init__(self, ui: UIFramework):
        """
        Initialize build menu.

        Args:
            ui: UI framework instance
        """
        self.ui = ui

    def render(self, game_state: GameState):
        """
        Render build menu.

        Args:
            game_state: Current game state
        """
        self.ui.clear_screen()

        # Header
        self.ui.print_colored(
            "╔═══ BUILD MENU ═════════════════════════════════════════════════════════╗",
            Color.BRIGHT_CYAN
        )
        self.ui.print_colored(
            "║ Construct structures to expand the colony                            ║",
            Color.CYAN
        )
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )

        # Get unlocked buildings
        buildings = game_state.buildings.buildings
        unlocked = [(name, bld) for name, bld in buildings.items() if bld.unlocked]

        # Display each building
        for idx, (name, building) in enumerate(unlocked, 1):
            self._render_building(game_state, idx, building)

        # Footer
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )
        self.ui.print_colored(
            "║ Enter number to build, or [ESC] to return                            ║",
            Color.CYAN
        )
        self.ui.print_colored(
            "╚════════════════════════════════════════════════════════════════════════╝",
            Color.BRIGHT_CYAN
        )

        print("> ", end='', flush=True)

    def _render_building(self, game_state: GameState, idx: int, building):
        """Render a single building option."""
        # Check if affordable
        affordable = game_state.resources.can_afford(building.cost)
        color = Color.GREEN if affordable else Color.RED

        # Building name and count
        icon = building.metadata.get('icon', '▪')
        current_count = building.count
        max_count_str = f"/{building.max_count}" if building.max_count else ""

        self.ui.print_colored(
            f"║ [{idx}] {icon} {building.display_name:<25} (Current: {current_count}{max_count_str})",
            Color.BRIGHT_WHITE
        )

        # Description
        self.ui.print_colored(
            f"║     {building.description:<66} ║",
            Color.WHITE
        )

        # Cost
        cost_str = ", ".join([f"{amt:.0f} {res}" for res, amt in building.cost.items()])
        self.ui.print_colored(
            f"║     Cost: {cost_str:<60} ║",
            color
        )

        # Production
        if building.produces:
            prod_str = ", ".join([f"+{rate:.1f} {res}/s" for res, rate in building.produces.items()])
            self.ui.print_colored(
                f"║     Production: {prod_str:<56} ║",
                Color.GREEN
            )

        # Consumption
        if building.consumes:
            cons_str = ", ".join([f"-{rate:.1f} {res}/s" for res, rate in building.consumes.items()])
            self.ui.print_colored(
                f"║     Consumption: {cons_str:<55} ║",
                Color.YELLOW
            )

        # Flavor text
        flavor = building.metadata.get('flavor', '')
        if flavor:
            self.ui.print_colored(
                f"║     \"{flavor}\"".ljust(70) + " ║",
                Color.DIM
            )

        # Separator
        self.ui.print_colored(
            "║ " + "─" * 69 + " ║",
            Color.WHITE
        )

    def get_choice(self, game_state: GameState) -> Tuple[bool, str]:
        """
        Get user's build choice.

        Args:
            game_state: Current game state

        Returns:
            tuple: (success, message)
        """
        try:
            choice = input().strip().lower()

            if choice in ['esc', 'exit', 'back', '']:
                return (True, "Cancelled")

            # Try to parse as number
            try:
                idx = int(choice)
                buildings_list = [
                    (name, bld) for name, bld in game_state.buildings.buildings.items()
                    if bld.unlocked
                ]

                if 1 <= idx <= len(buildings_list):
                    building_name, building = buildings_list[idx - 1]

                    # Check max count
                    if building.max_count and building.count >= building.max_count:
                        return (False, f"Maximum {building.display_name} count reached")

                    # Try to build
                    success = game_state.buildings.build(building_name)

                    if success:
                        return (True, f"{building.display_name} constructed")
                    else:
                        return (False, "Insufficient resources")
                else:
                    return (False, "Invalid choice")

            except ValueError:
                return (False, "Invalid input")

        except Exception as e:
            return (False, f"Error: {e}")


# Example usage
if __name__ == "__main__":
    from ..content.loader import load_new_game

    # Create game state
    game = load_new_game()

    # Give player some resources to test affordability
    game.resources.add('energy', 50)
    game.resources.add('metal', 30)

    # Render menu
    ui = UIFramework(use_colors=True)
    menu = BuildMenu(ui)
    menu.render(game)

    print("\n✓ Build menu test complete!")
