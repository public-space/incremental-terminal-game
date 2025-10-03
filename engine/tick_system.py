"""
Tick System Module
==================

Manages the game loop timing and tick-based updates.
Provides a consistent update cycle for idle/incremental games.

Classes:
    TickSystem: Main tick management class

Usage:
    tick_system = TickSystem(tick_rate=1.0)
    tick_system.start()

    while game_running:
        if tick_system.should_tick():
            # Update game state
            tick_system.tick()
"""

import time
import logging
from typing import Callable, List

# Setup logging
logging.basicConfig(
    filename='game_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TickSystem:
    """
    Manages game loop timing with configurable tick rate.

    Attributes:
        tick_rate (float): Target time between ticks in seconds
        tick_count (int): Total number of ticks since start
        last_tick_time (float): Timestamp of last tick
        delta_time (float): Time elapsed since last tick
        is_running (bool): Whether the tick system is active
        tick_callbacks (List[Callable]): Functions to call on each tick
    """

    def __init__(self, tick_rate: float = 1.0):
        """
        Initialize the tick system.

        Args:
            tick_rate: Target time between ticks in seconds (default: 1.0)
        """
        self.tick_rate = tick_rate
        self.tick_count = 0
        self.last_tick_time = 0
        self.delta_time = 0
        self.is_running = False
        self.tick_callbacks: List[Callable] = []

        logger.info(f"TickSystem initialized with tick_rate={tick_rate}s")

    def start(self):
        """Start the tick system."""
        self.is_running = True
        self.last_tick_time = time.time()
        logger.info("TickSystem started")

    def stop(self):
        """Stop the tick system."""
        self.is_running = False
        logger.info(f"TickSystem stopped after {self.tick_count} ticks")

    def should_tick(self) -> bool:
        """
        Check if enough time has passed for the next tick.

        Returns:
            bool: True if it's time for the next tick
        """
        if not self.is_running:
            return False

        current_time = time.time()
        elapsed = current_time - self.last_tick_time
        return elapsed >= self.tick_rate

    def tick(self):
        """
        Execute a single tick update.
        Updates tick count, delta time, and calls all registered callbacks.
        """
        try:
            current_time = time.time()
            self.delta_time = current_time - self.last_tick_time
            self.last_tick_time = current_time
            self.tick_count += 1

            # Call all registered callbacks
            for callback in self.tick_callbacks:
                try:
                    callback(self.delta_time)
                except Exception as e:
                    logger.error(f"Error in tick callback {callback.__name__}: {e}", exc_info=True)

            logger.debug(f"Tick #{self.tick_count} executed (Δt={self.delta_time:.3f}s)")

        except Exception as e:
            logger.error(f"Critical error in tick(): {e}", exc_info=True)
            raise

    def register_callback(self, callback: Callable):
        """
        Register a function to be called on each tick.

        Args:
            callback: Function that takes delta_time as parameter
        """
        if callback not in self.tick_callbacks:
            self.tick_callbacks.append(callback)
            logger.info(f"Registered tick callback: {callback.__name__}")

    def unregister_callback(self, callback: Callable):
        """
        Remove a callback function.

        Args:
            callback: Function to remove
        """
        if callback in self.tick_callbacks:
            self.tick_callbacks.remove(callback)
            logger.info(f"Unregistered tick callback: {callback.__name__}")

    def set_tick_rate(self, new_rate: float):
        """
        Change the tick rate.

        Args:
            new_rate: New tick rate in seconds
        """
        old_rate = self.tick_rate
        self.tick_rate = max(0.1, new_rate)  # Minimum 0.1s to prevent crazy fast ticks
        logger.info(f"Tick rate changed from {old_rate}s to {self.tick_rate}s")

    def get_stats(self) -> dict:
        """
        Get tick system statistics.

        Returns:
            dict: Statistics including tick count, rate, and uptime
        """
        uptime = self.tick_count * self.tick_rate
        return {
            'tick_count': self.tick_count,
            'tick_rate': self.tick_rate,
            'uptime': uptime,
            'delta_time': self.delta_time,
            'is_running': self.is_running
        }

    def reset(self):
        """Reset tick count and timing."""
        self.tick_count = 0
        self.last_tick_time = time.time()
        self.delta_time = 0
        logger.info("TickSystem reset")


# Example usage
if __name__ == "__main__":
    def example_callback(delta_time):
        print(f"Tick! (Δt={delta_time:.3f}s)")

    tick_system = TickSystem(tick_rate=1.0)
    tick_system.register_callback(example_callback)
    tick_system.start()

    print("Running tick system for 5 seconds...")
    start_time = time.time()
    while time.time() - start_time < 5:
        if tick_system.should_tick():
            tick_system.tick()
        time.sleep(0.01)  # Small sleep to prevent CPU spinning

    tick_system.stop()
    print(f"Stats: {tick_system.get_stats()}")
