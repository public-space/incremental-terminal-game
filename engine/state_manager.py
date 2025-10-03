"""
State Manager Module
====================

Generic game state management system.
Handles state storage, retrieval, and observation patterns.

Classes:
    StateManager: Main state management class

Usage:
    state = StateManager()
    state.set('player.gold', 100)
    gold = state.get('player.gold', default=0)
"""

import logging
from typing import Any, Callable, Dict, List, Optional
from collections import defaultdict
from copy import deepcopy

logger = logging.getLogger(__name__)


class StateManager:
    """
    Manages game state with nested dictionary support and observation pattern.

    Attributes:
        data (Dict): Main state storage
        observers (Dict[str, List[Callable]]): Registered state change observers
    """

    def __init__(self):
        """Initialize the state manager."""
        self.data: Dict[str, Any] = {}
        self.observers: Dict[str, List[Callable]] = defaultdict(list)
        logger.info("StateManager initialized")

    def set(self, key: str, value: Any, notify: bool = True):
        """
        Set a state value with optional dot notation for nested access.

        Args:
            key: State key (supports dot notation: 'player.inventory.gold')
            value: Value to set
            notify: Whether to notify observers (default: True)

        Examples:
            state.set('gold', 100)
            state.set('player.resources.wood', 50)
        """
        try:
            keys = key.split('.')
            current = self.data

            # Navigate to the nested location
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            # Set the value
            old_value = current.get(keys[-1])
            current[keys[-1]] = value

            logger.debug(f"State set: {key} = {value} (was {old_value})")

            # Notify observers
            if notify:
                self._notify_observers(key, value, old_value)

        except Exception as e:
            logger.error(f"Error setting state '{key}': {e}", exc_info=True)
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a state value with optional dot notation.

        Args:
            key: State key (supports dot notation)
            default: Default value if key doesn't exist

        Returns:
            The value at the key, or default if not found
        """
        try:
            keys = key.split('.')
            current = self.data

            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    logger.debug(f"State get: {key} not found, returning default={default}")
                    return default

            return current

        except Exception as e:
            logger.error(f"Error getting state '{key}': {e}", exc_info=True)
            return default

    def increment(self, key: str, amount: float = 1, notify: bool = True):
        """
        Increment a numeric state value.

        Args:
            key: State key
            amount: Amount to increment by (default: 1)
            notify: Whether to notify observers
        """
        current = self.get(key, default=0)
        if not isinstance(current, (int, float)):
            logger.warning(f"Attempted to increment non-numeric value at '{key}'")
            return

        self.set(key, current + amount, notify=notify)

    def decrement(self, key: str, amount: float = 1, notify: bool = True):
        """
        Decrement a numeric state value.

        Args:
            key: State key
            amount: Amount to decrement by (default: 1)
            notify: Whether to notify observers
        """
        self.increment(key, -amount, notify=notify)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in state.

        Args:
            key: State key to check

        Returns:
            bool: True if key exists
        """
        return self.get(key) is not None

    def delete(self, key: str):
        """
        Delete a key from state.

        Args:
            key: State key to delete
        """
        try:
            keys = key.split('.')
            current = self.data

            # Navigate to parent
            for k in keys[:-1]:
                if k in current:
                    current = current[k]
                else:
                    return  # Key doesn't exist, nothing to delete

            # Delete the key
            if keys[-1] in current:
                del current[keys[-1]]
                logger.debug(f"State deleted: {key}")

        except Exception as e:
            logger.error(f"Error deleting state '{key}': {e}", exc_info=True)

    def observe(self, key: str, callback: Callable):
        """
        Register an observer for state changes.

        Args:
            key: State key to observe
            callback: Function(key, new_value, old_value) to call on change
        """
        self.observers[key].append(callback)
        logger.debug(f"Observer registered for '{key}': {callback.__name__}")

    def unobserve(self, key: str, callback: Callable):
        """
        Remove an observer.

        Args:
            key: State key
            callback: Callback to remove
        """
        if key in self.observers and callback in self.observers[key]:
            self.observers[key].remove(callback)
            logger.debug(f"Observer removed for '{key}': {callback.__name__}")

    def _notify_observers(self, key: str, new_value: Any, old_value: Any):
        """
        Notify all observers of a state change.

        Args:
            key: State key that changed
            new_value: New value
            old_value: Previous value
        """
        if key in self.observers:
            for callback in self.observers[key]:
                try:
                    callback(key, new_value, old_value)
                except Exception as e:
                    logger.error(f"Error in observer callback for '{key}': {e}", exc_info=True)

    def get_all(self) -> Dict[str, Any]:
        """
        Get entire state as a dictionary.

        Returns:
            dict: Deep copy of all state data
        """
        return deepcopy(self.data)

    def set_all(self, data: Dict[str, Any]):
        """
        Replace entire state with new data.

        Args:
            data: New state data
        """
        self.data = deepcopy(data)
        logger.info("State replaced with new data")

    def clear(self):
        """Clear all state data."""
        self.data = {}
        logger.info("State cleared")

    def merge(self, data: Dict[str, Any]):
        """
        Merge new data into existing state.

        Args:
            data: Data to merge in
        """
        self._deep_merge(self.data, data)
        logger.info("State merged with new data")

    def _deep_merge(self, target: dict, source: dict):
        """
        Recursively merge source dict into target dict.

        Args:
            target: Target dictionary
            source: Source dictionary
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value


# Example usage
if __name__ == "__main__":
    def on_gold_change(key, new_val, old_val):
        print(f"Gold changed from {old_val} to {new_val}!")

    state = StateManager()
    state.observe('player.gold', on_gold_change)

    state.set('player.gold', 100)
    state.increment('player.gold', 50)
    print(f"Gold: {state.get('player.gold')}")

    state.set('player.resources.wood', 25)
    print(f"Wood: {state.get('player.resources.wood', default=0)}")
    print(f"All state: {state.get_all()}")
