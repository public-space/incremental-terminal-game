"""
Research Menu
=============

Technology tree interface for colony.sh.
"""

import sys
import os

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from engine import UIFramework, Color, GameState
from typing import Tuple


class ResearchMenu:
    """
    Research/upgrade menu.

    Displays available research with costs and effects.
    """

    def __init__(self, ui: UIFramework):
        """
        Initialize research menu.

        Args:
            ui: UI framework instance
        """
        self.ui = ui

    def render(self, game_state: GameState):
        """
        Render research menu.

        Args:
            game_state: Current game state
        """
        self.ui.clear_screen()

        # Header
        self.ui.print_colored(
            "╔═══ RESEARCH TERMINAL ══════════════════════════════════════════════════╗",
            Color.BRIGHT_CYAN
        )
        self.ui.print_colored(
            "║ Access corrupted databases. Unlock ancient knowledge.                 ║",
            Color.CYAN
        )
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )

        # Get research
        upgrades = game_state.upgrades.upgrades
        unlocked = [(name, upg) for name, upg in upgrades.items() if upg.unlocked]

        # Separate purchased and available
        available = [(name, upg) for name, upg in unlocked if not upg.purchased]
        completed = [(name, upg) for name, upg in unlocked if upg.purchased]

        # Display available research
        if available:
            self.ui.print_colored("║ AVAILABLE RESEARCH" + " " * 51 + " ║", Color.BRIGHT_WHITE)
            self.ui.print_colored(
                "║ " + "─" * 69 + " ║",
                Color.WHITE
            )

            for idx, (name, upgrade) in enumerate(available, 1):
                self._render_research(game_state, idx, upgrade, purchased=False)

        # Display completed research
        if completed:
            self.ui.print_colored("║ COMPLETED RESEARCH" + " " * 51 + " ║", Color.BRIGHT_GREEN)
            self.ui.print_colored(
                "║ " + "─" * 69 + " ║",
                Color.GREEN
            )

            for name, upgrade in completed:
                self._render_research(game_state, None, upgrade, purchased=True)

        # No research available
        if not available and not completed:
            self.ui.print_colored(
                "║   (No research available)".ljust(70) + " ║",
                Color.DIM
            )

        # Footer
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )
        self.ui.print_colored(
            "║ Enter number to research, or [ESC] to return                         ║",
            Color.CYAN
        )
        self.ui.print_colored(
            "╚════════════════════════════════════════════════════════════════════════╝",
            Color.BRIGHT_CYAN
        )

        print("> ", end='', flush=True)

    def _render_research(self, game_state: GameState, idx, upgrade, purchased: bool):
        """Render a single research option."""
        icon = upgrade.metadata.get('icon', '🔬')

        if purchased:
            # Completed research (no index)
            self.ui.print_colored(
                f"║ ✓ {icon} {upgrade.display_name}".ljust(70) + " ║",
                Color.GREEN
            )
            self.ui.print_colored(
                f"║     {upgrade.description:<62} ║",
                Color.DIM
            )
        else:
            # Available research
            affordable = game_state.resources.can_afford(upgrade.cost)
            color = Color.GREEN if affordable else Color.RED

            self.ui.print_colored(
                f"║ [{idx}] {icon} {upgrade.display_name}",
                Color.BRIGHT_WHITE
            )

            # Description
            self.ui.print_colored(
                f"║     {upgrade.description:<62} ║",
                Color.WHITE
            )

            # Cost
            cost_str = ", ".join([f"{amt:.0f} {res}" for res, amt in upgrade.cost.items()])
            self.ui.print_colored(
                f"║     Cost: {cost_str:<60} ║",
                color
            )

            # Effects
            if upgrade.effects:
                effects_str = ", ".join([
                    f"{key}: {val}x" if 'multiplier' in key else f"{key}: +{val}"
                    for key, val in upgrade.effects.items()
                ])
                self.ui.print_colored(
                    f"║     Effects: {effects_str:<57} ║",
                    Color.CYAN
                )

            # Flavor text
            flavor = upgrade.metadata.get('flavor', '')
            if flavor:
                self.ui.print_colored(
                    f"║     \"{flavor}\"".ljust(70) + " ║",
                    Color.DIM
                )

        # Separator
        self.ui.print_colored(
            "║ ────────────────────────────────────────────────────────────────── ║",
            Color.WHITE
        )

    def get_choice(self, game_state: GameState) -> Tuple[bool, str]:
        """
        Get user's research choice.

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
                available_list = [
                    (name, upg) for name, upg in game_state.upgrades.upgrades.items()
                    if upg.unlocked and not upg.purchased
                ]

                if 1 <= idx <= len(available_list):
                    upgrade_name, upgrade = available_list[idx - 1]

                    # Try to purchase
                    success = game_state.upgrades.purchase(upgrade_name)

                    if success:
                        return (True, f"Research complete: {upgrade.display_name}")
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

    # Give player some resources
    game.resources.add('energy', 100)
    game.resources.add('metal', 80)
    game.resources.add('biomass', 50)

    # Purchase one upgrade to show completed section
    game.upgrades.purchase('efficient_extraction')

    # Render menu
    ui = UIFramework(use_colors=True)
    menu = ResearchMenu(ui)
    menu.render(game)

    print("\n✓ Research menu test complete!")
