"""
Main Game Screen
================

Primary UI for colony.sh.
Displays resources, structures, production, and event log.
"""

import sys
import os

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from engine import UIFramework, Color, Panel, BorderStyle, GameState
from typing import Optional

# Handle imports
try:
    from ..systems.event_log import EventLog
except ImportError:
    from systems.event_log import EventLog


class MainScreen:
    """
    Main game screen renderer.

    Displays:
        - Header (title, Sol counter)
        - Resources (current, max, generation rates)
        - Structures (count, production/consumption)
        - Event log (recent messages)
        - Command prompt
    """

    def __init__(self, ui: UIFramework):
        """
        Initialize main screen.

        Args:
            ui: UI framework instance
        """
        self.ui = ui

    def render(
        self,
        game_state: GameState,
        event_log: EventLog,
        show_production: bool = True
    ):
        """
        Render the main game screen.

        Args:
            game_state: Current game state
            event_log: Event log instance
            show_production: Whether to show production rates
        """
        self.ui.clear_screen()

        # Header
        self._render_header(game_state)

        # Resources
        self._render_resources(game_state, show_production)

        # Structures
        self._render_structures(game_state)

        # Event Log
        self._render_event_log(event_log)

        # Commands
        self._render_commands()

    def _render_header(self, game_state: GameState):
        """Render header with title and Sol counter."""
        sol = game_state.metadata.get('sol', 0)
        playtime = game_state.metadata.get('total_playtime', 0)

        # Title bar
        title = "COLONY.SH"
        subtitle = f"Sol {sol:03d} | Uptime: {int(playtime)}s"

        self.ui.print_colored(
            f"╔═══ {title} ════════════════════════════════════════════════════════╗",
            Color.BRIGHT_CYAN
        )
        self.ui.print_colored(
            f"║ {subtitle:<69} ║",
            Color.CYAN
        )
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )

    def _render_resources(self, game_state: GameState, show_production: bool):
        """Render resource display."""
        resources = game_state.resources

        # Resource header
        self.ui.print_colored("║ RESOURCES" + " " * 60 + " ║", Color.BRIGHT_WHITE)
        self.ui.print_colored(
            "║ " + "─" * 69 + " ║",
            Color.WHITE
        )

        # Each resource
        for res_name, resource in resources.resources.items():
            if not resource.unlocked:
                continue

            # Format amount (integers for colonists, floats for others)
            if resource.metadata.get('integer_only'):
                amount_str = f"{int(resource.amount)}"
                max_str = f"{int(resource.max_storage)}" if resource.max_storage else "∞"
            else:
                amount_str = f"{resource.amount:.1f}"
                max_str = f"{resource.max_storage:.1f}" if resource.max_storage else "∞"

            # Color based on status
            percent = resource.amount / resource.max_storage if resource.max_storage else 0
            if percent < 0.2:
                color = Color.RED
            elif percent < 0.5:
                color = Color.YELLOW
            else:
                color = Color.GREEN

            # Production rate
            rate_str = ""
            if show_production and resource.generation_rate != 0:
                sign = "+" if resource.generation_rate > 0 else ""
                rate_str = f" ({sign}{resource.generation_rate:.1f}/s)"

            # Display
            icon = resource.metadata.get('icon', '')
            display_text = f"║ {icon} {resource.display_name:<15} {amount_str:>6}/{max_str:<6}{rate_str:<15}"

            self.ui.print_colored(display_text.ljust(70) + " ║", color)

        print()

    def _render_structures(self, game_state: GameState):
        """Render structure display."""
        buildings = game_state.buildings

        # Structure header
        self.ui.print_colored("║ STRUCTURES" + " " * 59 + " ║", Color.BRIGHT_WHITE)
        self.ui.print_colored(
            "║ " + "─" * 69 + " ║",
            Color.WHITE
        )

        # Show structures with count > 0
        active_structures = [
            (name, building) for name, building in buildings.buildings.items()
            if building.count > 0
        ]

        if not active_structures:
            self.ui.print_colored("║   (No structures built yet)".ljust(70) + " ║", Color.DIM)
        else:
            for struct_name, building in active_structures:
                # Production/consumption summary
                status_parts = []

                # Production
                for res, rate in building.produces.items():
                    total_rate = rate * building.count
                    status_parts.append(f"+{total_rate:.1f} {res}/s")

                # Consumption
                for res, rate in building.consumes.items():
                    total_rate = rate * building.count
                    status_parts.append(f"-{total_rate:.1f} {res}/s")

                status_str = " ".join(status_parts) if status_parts else "No production"

                # Display
                icon = building.metadata.get('icon', '▪')
                display_text = f"║ {icon} {building.display_name:<20} x{building.count:<3} {status_str}"

                self.ui.print_colored(display_text.ljust(70) + " ║", Color.WHITE)

        print()

    def _render_event_log(self, event_log: EventLog):
        """Render event log."""
        self.ui.print_colored("║ EVENT LOG" + " " * 60 + " ║", Color.BRIGHT_WHITE)
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )

        # Get recent entries
        recent = event_log.get_recent(5)

        if not recent:
            self.ui.print_colored("║   (No events yet)".ljust(70) + " ║", Color.DIM)
        else:
            for entry in recent:
                # Color based on category
                color = {
                    'info': Color.WHITE,
                    'warning': Color.YELLOW,
                    'critical': Color.RED,
                    'success': Color.GREEN,
                }.get(entry.category, Color.WHITE)

                # Format entry
                entry_str = str(entry)
                self.ui.print_colored(f"║ {entry_str:<69} ║", color)

        print()

    def _render_commands(self):
        """Render command bar."""
        self.ui.print_colored(
            "╠════════════════════════════════════════════════════════════════════════╣",
            Color.BRIGHT_CYAN
        )

        commands = "[B]uild  [R]esearch  [I]nfo  [H]elp  [S]ave  [Q]uit"
        self.ui.print_colored(f"║ {commands:<69} ║", Color.CYAN)

        self.ui.print_colored(
            "╚════════════════════════════════════════════════════════════════════════╝",
            Color.BRIGHT_CYAN
        )

        print("> ", end='', flush=True)


# Example usage
if __name__ == "__main__":
    from ..content.loader import load_new_game
    from ..systems.event_log import EventLog

    # Create game state
    game = load_new_game()
    event_log = EventLog()
    event_log.set_sol(5)

    # Add some test events
    event_log.info("Colony initialization complete")
    event_log.success("Solar Array online")
    event_log.warning("Energy reserves low")
    event_log.info("Mining Rig constructed")

    # Build some structures for display
    game.buildings.get_building('mining_rig').count = 2
    game.buildings.get_building('reclamation_bay').count = 1

    # Set some resource generation
    game.resources.get_resource('energy').generation_rate = 3.0
    game.resources.get_resource('metal').generation_rate = 1.5

    # Render
    ui = UIFramework(use_colors=True)
    screen = MainScreen(ui)
    screen.render(game, event_log)

    print("\n✓ Main screen test complete!")
