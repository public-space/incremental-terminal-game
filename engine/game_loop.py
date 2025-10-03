"""
Game Loop Module
=================

Generic game loop for terminal-based games.
Integrates tick system, UI, input, and animation systems.

Classes:
    GameLoop: Main game loop controller

Usage:
    loop = GameLoop(game_state, tick_rate=1.0)
    loop.register_render_callback(render_ui)
    loop.register_update_callback(update_game)
    loop.run()
"""

import logging
import time
import sys
import select
from typing import Callable, Optional, List
from enum import Enum

from .tick_system import TickSystem
from .ui_framework import UIFramework, Color
from .input_handler import InputHandler
from .animator import Animator

logger = logging.getLogger(__name__)


class GameState(Enum):
    """Game loop states."""
    MENU = 'menu'
    RUNNING = 'running'
    PAUSED = 'paused'
    QUITTING = 'quitting'


class GameLoop:
    """
    Generic game loop that integrates all engine systems.

    Attributes:
        tick_system (TickSystem): Game timing system
        ui (UIFramework): UI rendering system
        input_handler (InputHandler): Command processing
        animator (Animator): Animation system
        state (GameState): Current game state
        running (bool): Whether loop is active
    """

    def __init__(
        self,
        tick_rate: float = 1.0,
        use_colors: bool = True,
        max_fps: float = 60.0
    ):
        """
        Initialize the game loop.

        Args:
            tick_rate: Game ticks per second
            use_colors: Enable terminal colors
            max_fps: Maximum frames per second
        """
        self.tick_system = TickSystem(tick_rate=tick_rate)
        self.ui = UIFramework(use_colors=use_colors)
        self.input_handler = InputHandler()
        self.animator = Animator()

        self.state = GameState.MENU
        self.running = False

        self.max_fps = max_fps
        self.frame_time = 1.0 / max_fps

        # Callbacks
        self.render_callbacks: List[Callable] = []
        self.update_callbacks: List[Callable] = []
        self.input_callbacks: List[Callable] = []

        # Timing
        self.last_frame_time = 0.0
        self.frame_count = 0
        self.elapsed_time = 0.0

        logger.info(f"GameLoop initialized (tick_rate={tick_rate}, max_fps={max_fps})")

    def register_render_callback(self, callback: Callable):
        """
        Register a render callback.

        Args:
            callback: Function to call for rendering (receives ui, animator)
        """
        self.render_callbacks.append(callback)

    def register_update_callback(self, callback: Callable):
        """
        Register an update callback.

        Args:
            callback: Function to call for updates (receives delta_time)
        """
        self.update_callbacks.append(callback)
        # Also register with tick system
        self.tick_system.register_callback(callback)

    def register_input_callback(self, callback: Callable):
        """
        Register an input processing callback.

        Args:
            callback: Function to call for custom input handling
        """
        self.input_callbacks.append(callback)

    def setup_default_commands(self):
        """Set up default system commands."""

        def cmd_help(args):
            """Show help."""
            command = args[0] if args else None
            print(self.input_handler.generate_help(command))

        def cmd_quit(args):
            """Quit the game."""
            self.state = GameState.QUITTING
            print("Quitting game...")

        def cmd_pause(args):
            """Pause the game."""
            if self.state == GameState.RUNNING:
                self.state = GameState.PAUSED
                self.tick_system.stop()
                print("Game paused.")
            elif self.state == GameState.PAUSED:
                self.state = GameState.RUNNING
                self.tick_system.start()
                print("Game resumed.")

        def cmd_stats(args):
            """Show game statistics."""
            tick_stats = self.tick_system.get_stats()
            print(f"\n=== Game Statistics ===")
            print(f"  Ticks: {tick_stats['tick_count']}")
            print(f"  Tick Rate: {tick_stats['tick_rate']}/s")
            print(f"  Uptime: {tick_stats['uptime']:.1f}s")
            print(f"  Frames: {self.frame_count}")
            print(f"  FPS Target: {self.max_fps}")
            print(f"  Animations: {len(self.animator.animations)}\n")

        def cmd_clear(args):
            """Clear the screen."""
            self.ui.clear_screen()

        # Register default commands
        self.input_handler.register_command(
            'help', cmd_help, 'Show available commands',
            aliases=['h', '?'], args_help='[command]', category='System'
        )

        self.input_handler.register_command(
            'quit', cmd_quit, 'Exit the game',
            aliases=['q', 'exit'], category='System'
        )

        self.input_handler.register_command(
            'pause', cmd_pause, 'Pause/resume the game',
            aliases=['p'], category='System'
        )

        self.input_handler.register_command(
            'stats', cmd_stats, 'Show game statistics',
            category='System'
        )

        self.input_handler.register_command(
            'clear', cmd_clear, 'Clear the screen',
            aliases=['cls'], category='System'
        )

    def start(self):
        """Start the game loop."""
        self.running = True
        self.state = GameState.RUNNING
        self.tick_system.start()
        self.last_frame_time = time.time()
        logger.info("Game loop started")

    def stop(self):
        """Stop the game loop."""
        self.running = False
        self.tick_system.stop()
        logger.info("Game loop stopped")

    def update(self, delta_time: float):
        """
        Update game state.

        Args:
            delta_time: Time since last update
        """
        # Update animations
        self.animator.update(delta_time)

        # Update tick system
        if self.tick_system.should_tick():
            self.tick_system.tick()

        # Call custom update callbacks (non-tick based, every frame)
        for callback in self.update_callbacks:
            if callback not in self.tick_system.tick_callbacks:
                try:
                    callback(delta_time)
                except Exception as e:
                    logger.error(f"Error in update callback: {e}", exc_info=True)

    def render(self):
        """Render the game."""
        try:
            for callback in self.render_callbacks:
                callback(self.ui, self.animator)

        except Exception as e:
            logger.error(f"Error in render callback: {e}", exc_info=True)

    def process_input(self):
        """Process user input (non-blocking)."""
        # Check if input is available (Unix-like systems)
        if sys.platform != 'win32':
            # Non-blocking input check
            ready, _, _ = select.select([sys.stdin], [], [], 0)

            if ready:
                try:
                    user_input = sys.stdin.readline().strip()
                    if user_input:
                        # Process through input handler
                        result = self.input_handler.process_input(user_input)

                        # Call custom input callbacks
                        for callback in self.input_callbacks:
                            try:
                                callback(user_input, result)
                            except Exception as e:
                                logger.error(f"Error in input callback: {e}", exc_info=True)

                except Exception as e:
                    logger.error(f"Error processing input: {e}", exc_info=True)

    def run_frame(self):
        """Execute a single frame."""
        current_time = time.time()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        self.elapsed_time += delta_time
        self.frame_count += 1

        # Update
        if self.state == GameState.RUNNING:
            self.update(delta_time)

        # Render
        self.render()

        # Process input
        self.process_input()

        # Frame limiting
        frame_end_time = time.time()
        frame_duration = frame_end_time - current_time

        if frame_duration < self.frame_time:
            time.sleep(self.frame_time - frame_duration)

    def run(self):
        """
        Run the main game loop.

        This is the primary entry point for starting the game.
        """
        logger.info("Entering main game loop")

        try:
            self.start()

            while self.running and self.state != GameState.QUITTING:
                self.run_frame()

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            print("\n\nGame interrupted by user.")

        except Exception as e:
            logger.error(f"Fatal error in game loop: {e}", exc_info=True)
            print(f"\n\nFatal error: {e}")

        finally:
            self.stop()
            self.ui.show_cursor()
            logger.info("Game loop exited")

    def run_menu_loop(self, menu_render: Callable, menu_options: dict):
        """
        Run a simple menu loop.

        Args:
            menu_render: Function to render menu (receives ui)
            menu_options: Dict of {input: callback} for menu choices
        """
        self.state = GameState.MENU

        while self.state == GameState.MENU:
            self.ui.clear_screen()
            menu_render(self.ui)

            try:
                user_input = self.ui.input_prompt("\nChoice: ").strip().lower()

                if user_input in menu_options:
                    result = menu_options[user_input]()

                    if result == "START":
                        self.state = GameState.RUNNING
                        break
                    elif result == "QUIT":
                        self.state = GameState.QUITTING
                        break
                else:
                    print(f"Invalid choice: {user_input}")
                    time.sleep(1)

            except KeyboardInterrupt:
                self.state = GameState.QUITTING
                break

    def get_fps(self) -> float:
        """
        Get current FPS.

        Returns:
            float: Frames per second
        """
        if self.elapsed_time > 0:
            return self.frame_count / self.elapsed_time
        return 0.0


# Example usage
if __name__ == "__main__":
    # Create game loop
    game_loop = GameLoop(tick_rate=1.0, max_fps=30)

    # Set up default commands
    game_loop.setup_default_commands()

    # Example game state
    counter = [0]  # Use list for mutability in closures

    # Render callback
    def render_game(ui: UIFramework, animator: Animator):
        ui.move_cursor(0, 0)
        ui.print_colored("=== GAME LOOP TEST ===", Color.BRIGHT_CYAN, style=Color.BOLD)
        print(f"\nCounter: {counter[0]}")
        print(f"FPS: {game_loop.get_fps():.1f}")
        print(f"\nCommands: help, pause, stats, quit")
        print("\n> ", end='', flush=True)

    # Update callback (tick-based)
    def update_game(delta_time):
        counter[0] += 1

    # Register callbacks
    game_loop.register_render_callback(render_game)
    game_loop.register_update_callback(update_game)

    # Run
    print("Starting game loop demo...")
    print("Type 'help' for commands, 'quit' to exit\n")
    time.sleep(2)

    game_loop.run()

    print("\nGame loop demo ended.")
