"""
Colony.sh - Main Game
=====================

Dark sci-fi frontier colony survival sim.
Built on the incremental game engine.
"""

import sys
import os
import logging
import time

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine import GameLoop, GameLoopState, UIFramework, InputHandler, Color
from content.loader import load_new_game, load_save_game
from systems.event_log import EventLog
from ui.main_screen import MainScreen
from ui.build_menu import BuildMenu
from ui.research_menu import ResearchMenu
from ui.help_screen import HelpScreen
import config

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('colony.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ColonyGame:
    """
    Main game controller for colony.sh.

    Integrates engine systems with game-specific logic.
    """

    def __init__(self):
        """Initialize the game."""
        # Engine systems
        self.game_loop = GameLoop(
            tick_rate=config.TICK_RATE,
            max_fps=config.MAX_FPS,
            use_colors=config.USE_COLORS
        )

        # Game state
        self.game_state = None
        self.event_log = EventLog()

        # UI screens
        self.main_screen = MainScreen(self.game_loop.ui)
        self.build_menu = BuildMenu(self.game_loop.ui)
        self.research_menu = ResearchMenu(self.game_loop.ui)
        self.help_screen = HelpScreen(self.game_loop.ui)

        # Timing
        self.sol_timer = 0.0
        self.render_timer = 0.0
        self.render_interval = 1.0 / 30.0  # Render at 30 FPS

        # Setup
        self._setup_callbacks()
        self._setup_commands()

        logger.info("Colony.sh initialized")

    def _setup_callbacks(self):
        """Register engine callbacks."""
        # Update callback (tick-based)
        self.game_loop.register_update_callback(self._on_update)

        # Render callback
        self.game_loop.register_render_callback(self._on_render)

    def _setup_commands(self):
        """Register game commands."""
        handler = self.game_loop.input_handler

        # Build command
        def cmd_build(args):
            self._handle_build_menu()

        # Research command
        def cmd_research(args):
            self._handle_research_menu()

        # Info command
        def cmd_info(args):
            self._show_info()

        # Help command
        def cmd_help(args):
            self.help_screen.render()

        # Save command
        def cmd_save(args):
            self._save_game()

        # Quit command
        def cmd_quit(args):
            self.game_loop.state = GameLoopState.QUITTING
            self.event_log.info("Shutting down colony systems...")

        # Register commands
        handler.register_command('build', cmd_build, 'Construct structures', aliases=['b'], category='Game')
        handler.register_command('research', cmd_research, 'Unlock technologies', aliases=['r'], category='Game')
        handler.register_command('info', cmd_info, 'Show detailed stats', aliases=['i'], category='Game')
        handler.register_command('help', cmd_help, 'Show help', aliases=['h', '?'], category='System')
        handler.register_command('save', cmd_save, 'Save progress', aliases=['s'], category='System')
        handler.register_command('quit', cmd_quit, 'Exit game', aliases=['q', 'exit'], category='System')

    def _on_update(self, delta_time: float):
        """
        Update callback (called on each tick).

        Args:
            delta_time: Time since last tick
        """
        if not self.game_state:
            return

        # Update game state
        self.game_state.update(delta_time)

        # Update Sol counter
        self.sol_timer += delta_time
        if self.sol_timer >= config.SOL_LENGTH:
            self.sol_timer = 0.0
            self.game_state.metadata['sol'] += 1
            self.event_log.set_sol(self.game_state.metadata['sol'])
            self.event_log.info(f"Sol {self.game_state.metadata['sol']} begins")

        # Update production rates (display only)
        self._calculate_production_rates()

    def _calculate_production_rates(self):
        """Calculate and update resource generation rates for display."""
        # Get base production from buildings
        total_production = self.game_state.buildings.get_total_production()
        total_consumption = self.game_state.buildings.get_total_consumption()

        # Apply to resource generation rates
        for res_name, resource in self.game_state.resources.resources.items():
            production = total_production.get(res_name, 0)
            consumption = total_consumption.get(res_name, 0)
            resource.generation_rate = production - consumption

    def _on_render(self, ui: UIFramework, animator):
        """
        Render callback.

        Args:
            ui: UI framework
            animator: Animator instance
        """
        # Throttle rendering
        self.render_timer += 1.0 / config.MAX_FPS
        if self.render_timer < self.render_interval:
            return

        self.render_timer = 0.0

        # Render main screen
        if self.game_state:
            self.main_screen.render(self.game_state, self.event_log)

    def _handle_build_menu(self):
        """Handle build menu interaction."""
        self.build_menu.render(self.game_state)
        success, message = self.build_menu.get_choice(self.game_state)

        if success and message != "Cancelled":
            self.event_log.success(message)
        elif not success:
            self.event_log.warning(message)

    def _handle_research_menu(self):
        """Handle research menu interaction."""
        self.research_menu.render(self.game_state)
        success, message = self.research_menu.get_choice(self.game_state)

        if success and message != "Cancelled":
            self.event_log.success(message)
        elif not success:
            self.event_log.warning(message)

    def _show_info(self):
        """Show detailed game statistics."""
        ui = self.game_loop.ui
        ui.clear_screen()

        ui.print_colored("=== COLONY STATISTICS ===\n", Color.BRIGHT_CYAN)

        # Production summary
        ui.print_colored("PRODUCTION SUMMARY:", Color.BRIGHT_WHITE)
        total_prod = self.game_state.buildings.get_total_production()
        total_cons = self.game_state.buildings.get_total_consumption()

        for res in ['energy', 'metal', 'biomass']:
            prod = total_prod.get(res, 0)
            cons = total_cons.get(res, 0)
            net = prod - cons
            print(f"  {res.capitalize()}: +{prod:.2f}/s  -{cons:.2f}/s  = {net:+.2f}/s")

        # Game stats
        ui.print_colored("\nGAME STATISTICS:", Color.BRIGHT_WHITE)
        print(f"  Sol: {self.game_state.metadata.get('sol', 0)}")
        print(f"  Playtime: {self.game_state.metadata.get('total_playtime', 0):.1f}s")
        print(f"  Ticks: {self.game_state.metadata.get('tick_count', 0)}")

        # Structure count
        total_structures = sum(b.count for b in self.game_state.buildings.buildings.values())
        print(f"  Structures: {total_structures}")

        # Research completed
        completed_research = sum(
            1 for u in self.game_state.upgrades.upgrades.values() if u.purchased
        )
        print(f"  Research Completed: {completed_research}")

        print("\nPress [ENTER] to continue...")
        input()

    def _save_game(self):
        """Save the game."""
        try:
            config.ensure_save_directory()
            self.game_state.save_game(config.DEFAULT_SAVE_FILE)

            # Get save file name for display
            save_name = os.path.basename(config.DEFAULT_SAVE_FILE)
            sol = self.game_state.metadata.get('sol', 0)

            self.event_log.success(f"Colony saved to {save_name} (Sol {sol})")
            logger.info(f"Game saved to {config.DEFAULT_SAVE_FILE}")
        except Exception as e:
            self.event_log.critical(f"Save failed: {e}")
            logger.error(f"Save failed: {e}", exc_info=True)

    def start_new_game(self):
        """Start a new game."""
        self.game_state = load_new_game()
        self.event_log.clear()
        self.event_log.set_sol(0)
        self.event_log.info("Colony initialization sequence started")
        self.event_log.success("Solar Array online")
        self.event_log.success("Hab Module pressurized")
        self.event_log.info("3 colonists awake from cryo-sleep")

        logger.info("New game started")

    def load_game(self):
        """Load a saved game."""
        try:
            self.game_state = load_save_game(config.DEFAULT_SAVE_FILE)
            self.event_log.set_sol(self.game_state.metadata.get('sol', 0))
            self.event_log.success("Colony systems restored from archive")

            logger.info("Game loaded successfully")
        except FileNotFoundError:
            self.event_log.warning("No save file found. Starting new colony.")
            self.start_new_game()
        except Exception as e:
            self.event_log.critical(f"Load failed: {e}")
            logger.error(f"Load failed: {e}", exc_info=True)
            self.start_new_game()

    def run_main_menu(self):
        """Run the main menu."""
        ui = self.game_loop.ui
        ui.clear_screen()

        # Title
        ui.print_colored("╔════════════════════════════════════════════════════════════════════════╗", Color.BRIGHT_CYAN)
        ui.print_colored("║                                                                        ║", Color.CYAN)
        ui.print_colored("║                          COLONY.SH                                     ║", Color.BRIGHT_WHITE, style=Color.BOLD)
        ui.print_colored("║                                                                        ║", Color.CYAN)
        ui.print_colored("║                  Frontier Colony Survival Sim                          ║", Color.CYAN)
        ui.print_colored("║                                                                        ║", Color.CYAN)
        ui.print_colored("╠════════════════════════════════════════════════════════════════════════╣", Color.BRIGHT_CYAN)
        ui.print_colored("║                                                                        ║", Color.WHITE)
        ui.print_colored("║   [1] New Colony                                                       ║", Color.WHITE)
        ui.print_colored("║   [2] Load Colony                                                      ║", Color.WHITE)
        ui.print_colored("║   [3] Quit                                                             ║", Color.WHITE)
        ui.print_colored("║                                                                        ║", Color.WHITE)
        ui.print_colored("╚════════════════════════════════════════════════════════════════════════╝", Color.BRIGHT_CYAN)

        print("\n> ", end='', flush=True)

        choice = input().strip()

        if choice == '1':
            self.start_new_game()
            return True
        elif choice == '2':
            self.load_game()
            return True
        elif choice == '3':
            return False
        else:
            return True

    def run(self):
        """Run the game."""
        logger.info("=== COLONY.SH STARTED ===")

        try:
            # Main menu
            if not self.run_main_menu():
                return

            # Start game loop
            self.game_loop.run()

        except KeyboardInterrupt:
            logger.info("Game interrupted by user")
            print("\n\nColony systems shutting down...")

        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            print(f"\n\nCRITICAL SYSTEM FAILURE: {e}")

        finally:
            logger.info("=== COLONY.SH SHUTDOWN ===")


def main():
    """Entry point."""
    game = ColonyGame()
    game.run()


if __name__ == "__main__":
    main()
