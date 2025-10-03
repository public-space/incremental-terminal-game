"""
Upgrade Management Module
==========================

Manages upgrades, tech tree, and one-time purchases.
Provides a system for permanent improvements and progression unlocks.

Classes:
    Upgrade: Individual upgrade definition
    UpgradeManager: Central upgrade management system

Usage:
    upgrade_mgr = UpgradeManager(resource_mgr)
    upgrade_mgr.register_upgrade('better_tools', cost={'gold': 100}, effects={'wood_bonus': 0.5})
    upgrade_mgr.purchase('better_tools')
"""

import logging
from typing import Dict, Optional, Callable, List, Set
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Upgrade:
    """
    Represents a one-time upgrade in the game.

    Attributes:
        name (str): Unique identifier for the upgrade
        display_name (str): Human-readable name
        description (str): Upgrade description
        cost (Dict[str, float]): Resources required to purchase {resource: amount}
        purchased (bool): Whether this upgrade has been bought
        effects (Dict[str, float]): Effects/bonuses provided {effect: value}
        unlocked (bool): Whether upgrade is visible/available
        prerequisites (Set[str]): Upgrade names required before this can be purchased
        unlocks (List[str]): What this upgrade unlocks (buildings, units, etc.)
        repeatable (bool): Whether this can be purchased multiple times
        times_purchased (int): Number of times purchased (for repeatable upgrades)
        max_purchases (int): Maximum purchases (None = unlimited for repeatable)
        metadata (dict): Additional custom data
    """
    name: str
    display_name: str = ""
    description: str = ""
    cost: Dict[str, float] = field(default_factory=dict)
    purchased: bool = False
    effects: Dict[str, float] = field(default_factory=dict)
    unlocked: bool = False
    prerequisites: Set[str] = field(default_factory=set)
    unlocks: List[str] = field(default_factory=list)
    repeatable: bool = False
    times_purchased: int = 0
    max_purchases: Optional[int] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set display_name to name if not provided."""
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()

    def can_purchase_more(self) -> bool:
        """
        Check if upgrade can be purchased (again).

        Returns:
            bool: True if purchase is possible
        """
        if not self.repeatable:
            return not self.purchased

        if self.max_purchases is None:
            return True

        return self.times_purchased < self.max_purchases

    def get_cost(self) -> Dict[str, float]:
        """
        Get current cost to purchase (may scale with times_purchased).

        Returns:
            dict: Current cost
        """
        # For repeatable upgrades, could implement scaling costs here
        if self.repeatable and self.times_purchased > 0:
            # Simple exponential scaling example
            scale = 1.5 ** self.times_purchased
            return {resource: amount * scale for resource, amount in self.cost.items()}

        return self.cost.copy()

    def to_dict(self) -> dict:
        """
        Serialize upgrade to dictionary.

        Returns:
            dict: Upgrade data
        """
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'cost': self.cost,
            'purchased': self.purchased,
            'effects': self.effects,
            'unlocked': self.unlocked,
            'prerequisites': list(self.prerequisites),
            'unlocks': self.unlocks,
            'repeatable': self.repeatable,
            'times_purchased': self.times_purchased,
            'max_purchases': self.max_purchases,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Upgrade':
        """
        Deserialize upgrade from dictionary.

        Args:
            data: Dictionary containing upgrade data

        Returns:
            Upgrade: New upgrade instance
        """
        # Convert prerequisites list back to set
        if 'prerequisites' in data:
            data['prerequisites'] = set(data['prerequisites'])
        return cls(**data)


class UpgradeManager:
    """
    Manages all upgrades and tech tree progression.

    Attributes:
        upgrades (Dict[str, Upgrade]): All registered upgrades
        resource_manager: Reference to ResourceManager for costs
        purchase_callbacks (List[Callable]): Callbacks when upgrades are purchased
    """

    def __init__(self, resource_manager=None):
        """
        Initialize the upgrade manager.

        Args:
            resource_manager: ResourceManager instance for handling costs
        """
        self.upgrades: Dict[str, Upgrade] = {}
        self.resource_manager = resource_manager
        self.purchase_callbacks: List[Callable] = []
        logger.info("UpgradeManager initialized")

    def register_upgrade(
        self,
        name: str,
        cost: Dict[str, float],
        display_name: str = "",
        description: str = "",
        effects: Optional[Dict[str, float]] = None,
        unlocked: bool = False,
        prerequisites: Optional[List[str]] = None,
        unlocks: Optional[List[str]] = None,
        repeatable: bool = False,
        max_purchases: Optional[int] = None,
        **metadata
    ) -> Upgrade:
        """
        Register a new upgrade.

        Args:
            name: Unique upgrade identifier
            cost: Purchase cost {resource: amount}
            display_name: Display name for UI
            description: Upgrade description
            effects: Effects/bonuses {effect: value}
            unlocked: Whether visible initially
            prerequisites: Required upgrades (by name)
            unlocks: What this unlocks (building/unit names)
            repeatable: Whether can be purchased multiple times
            max_purchases: Maximum purchases for repeatable upgrades
            **metadata: Additional custom data

        Returns:
            Upgrade: The created upgrade

        Raises:
            ValueError: If upgrade already exists
        """
        if name in self.upgrades:
            raise ValueError(f"Upgrade '{name}' already exists")

        upgrade = Upgrade(
            name=name,
            display_name=display_name,
            description=description,
            cost=cost,
            effects=effects or {},
            unlocked=unlocked,
            prerequisites=set(prerequisites or []),
            unlocks=unlocks or [],
            repeatable=repeatable,
            max_purchases=max_purchases,
            metadata=metadata
        )

        self.upgrades[name] = upgrade
        logger.info(f"Upgrade registered: {name} (cost={cost})")
        return upgrade

    def get_upgrade(self, name: str) -> Optional[Upgrade]:
        """
        Get an upgrade by name.

        Args:
            name: Upgrade identifier

        Returns:
            Upgrade or None: The upgrade if found
        """
        return self.upgrades.get(name)

    def has_upgrade(self, name: str) -> bool:
        """
        Check if an upgrade exists.

        Args:
            name: Upgrade identifier

        Returns:
            bool: True if upgrade exists
        """
        return name in self.upgrades

    def is_purchased(self, name: str) -> bool:
        """
        Check if an upgrade has been purchased.

        Args:
            name: Upgrade identifier

        Returns:
            bool: True if purchased
        """
        upgrade = self.get_upgrade(name)
        return upgrade.purchased if upgrade else False

    def can_purchase(self, name: str) -> bool:
        """
        Check if an upgrade can be purchased.

        Args:
            name: Upgrade identifier

        Returns:
            bool: True if all requirements met
        """
        upgrade = self.get_upgrade(name)
        if not upgrade or not upgrade.unlocked:
            return False

        # Check if already purchased (for non-repeatable)
        if not upgrade.can_purchase_more():
            return False

        # Check prerequisites
        for prereq in upgrade.prerequisites:
            if not self.is_purchased(prereq):
                logger.debug(f"Upgrade '{name}' requires '{prereq}'")
                return False

        # Check cost
        if self.resource_manager:
            current_cost = upgrade.get_cost()
            return self.resource_manager.can_afford(current_cost)

        return True

    def purchase(self, name: str) -> bool:
        """
        Purchase an upgrade.

        Args:
            name: Upgrade identifier

        Returns:
            bool: True if successful
        """
        if not self.can_purchase(name):
            logger.debug(f"Cannot purchase upgrade: {name}")
            return False

        upgrade = self.get_upgrade(name)
        if not upgrade:
            return False

        # Spend resources
        current_cost = upgrade.get_cost()
        if self.resource_manager:
            if not self.resource_manager.spend_multiple(current_cost):
                return False

        # Mark as purchased
        if upgrade.repeatable:
            upgrade.times_purchased += 1
        else:
            upgrade.purchased = True

        logger.info(f"Purchased upgrade: {name}")

        # Process unlocks
        self._process_unlocks(upgrade)

        # Notify callbacks
        self._notify_purchase(name, upgrade)

        return True

    def _process_unlocks(self, upgrade: Upgrade):
        """
        Process what this upgrade unlocks.

        Args:
            upgrade: The upgrade that was purchased
        """
        for unlock_name in upgrade.unlocks:
            # Check if it's another upgrade
            if self.has_upgrade(unlock_name):
                self.unlock_upgrade(unlock_name)
                logger.info(f"Upgrade '{upgrade.name}' unlocked upgrade '{unlock_name}'")

    def unlock_upgrade(self, name: str):
        """
        Unlock an upgrade (make it visible).

        Args:
            name: Upgrade identifier
        """
        upgrade = self.get_upgrade(name)
        if upgrade:
            upgrade.unlocked = True
            logger.info(f"Upgrade unlocked: {name}")

    def get_unlocked_upgrades(self) -> List[Upgrade]:
        """
        Get all unlocked upgrades.

        Returns:
            List[Upgrade]: List of unlocked upgrades
        """
        return [u for u in self.upgrades.values() if u.unlocked]

    def get_available_upgrades(self) -> List[Upgrade]:
        """
        Get upgrades that are unlocked and not yet purchased.

        Returns:
            List[Upgrade]: List of available upgrades
        """
        return [
            u for u in self.upgrades.values()
            if u.unlocked and u.can_purchase_more()
        ]

    def get_purchased_upgrades(self) -> List[Upgrade]:
        """
        Get all purchased upgrades.

        Returns:
            List[Upgrade]: List of purchased upgrades
        """
        return [u for u in self.upgrades.values() if u.purchased or u.times_purchased > 0]

    def get_effect_value(self, effect_name: str) -> float:
        """
        Get cumulative value of an effect from all purchased upgrades.

        Args:
            effect_name: Name of the effect

        Returns:
            float: Total effect value
        """
        total = 0.0
        for upgrade in self.get_purchased_upgrades():
            if effect_name in upgrade.effects:
                effect_value = upgrade.effects[effect_name]

                # For repeatable upgrades, multiply by times purchased
                if upgrade.repeatable:
                    effect_value *= upgrade.times_purchased

                total += effect_value

        return total

    def has_effect(self, effect_name: str) -> bool:
        """
        Check if player has any upgrades providing this effect.

        Args:
            effect_name: Name of the effect

        Returns:
            bool: True if effect is active
        """
        return self.get_effect_value(effect_name) > 0

    def get_all_effects(self) -> Dict[str, float]:
        """
        Get all cumulative effects from purchased upgrades.

        Returns:
            dict: All effects {effect_name: total_value}
        """
        all_effects: Dict[str, float] = {}

        for upgrade in self.get_purchased_upgrades():
            for effect_name, effect_value in upgrade.effects.items():
                # For repeatable upgrades, multiply by times purchased
                if upgrade.repeatable:
                    effect_value *= upgrade.times_purchased

                all_effects[effect_name] = all_effects.get(effect_name, 0) + effect_value

        return all_effects

    def register_purchase_callback(self, callback: Callable):
        """
        Register callback for when upgrades are purchased.

        Args:
            callback: Function(upgrade_name, upgrade)
        """
        self.purchase_callbacks.append(callback)

    def _notify_purchase(self, name: str, upgrade: Upgrade):
        """
        Notify callbacks of upgrade purchase.

        Args:
            name: Upgrade name
            upgrade: The upgrade that was purchased
        """
        for callback in self.purchase_callbacks:
            try:
                callback(name, upgrade)
            except Exception as e:
                logger.error(f"Error in purchase callback: {e}", exc_info=True)

    def get_upgrade_tree_tier(self, name: str, visited: Optional[Set[str]] = None) -> int:
        """
        Get the tier/depth of an upgrade in the tech tree.

        Args:
            name: Upgrade identifier
            visited: Set of already visited upgrades (for cycle detection)

        Returns:
            int: Tier level (0 = no prerequisites)
        """
        if visited is None:
            visited = set()

        upgrade = self.get_upgrade(name)
        if not upgrade or name in visited:
            return 0

        visited.add(name)

        if not upgrade.prerequisites:
            return 0

        # Tier is 1 + max tier of prerequisites
        max_prereq_tier = max(
            (self.get_upgrade_tree_tier(prereq, visited) for prereq in upgrade.prerequisites),
            default=-1
        )

        return max_prereq_tier + 1

    def to_dict(self) -> dict:
        """
        Serialize all upgrades to dictionary.

        Returns:
            dict: All upgrade data
        """
        return {
            name: upgrade.to_dict()
            for name, upgrade in self.upgrades.items()
        }

    def from_dict(self, data: dict):
        """
        Load upgrades from dictionary.

        Args:
            data: Dictionary of upgrade data
        """
        self.upgrades.clear()
        for name, upgrade_data in data.items():
            self.upgrades[name] = Upgrade.from_dict(upgrade_data)
        logger.info(f"Loaded {len(self.upgrades)} upgrades from data")

    def reset(self):
        """Clear all upgrades."""
        self.upgrades.clear()
        logger.info("UpgradeManager reset")


# Example usage
if __name__ == "__main__":
    from resources import ResourceManager

    # Create managers
    rm = ResourceManager()
    rm.add_resource('gold', initial=500)
    rm.add_resource('research', initial=100)

    um = UpgradeManager(resource_manager=rm)

    # Register upgrades with tech tree
    um.register_upgrade(
        'basic_tools',
        cost={'gold': 50},
        effects={'wood_bonus': 0.25},
        description="Improve wood gathering by 25%",
        unlocked=True
    )

    um.register_upgrade(
        'advanced_tools',
        cost={'gold': 200, 'research': 50},
        effects={'wood_bonus': 0.5},
        description="Further improve wood gathering by 50%",
        prerequisites=['basic_tools'],
        unlocked=True
    )

    um.register_upgrade(
        'worker_training',
        cost={'gold': 100},
        effects={'worker_efficiency': 0.1},
        description="Workers are 10% more efficient",
        unlocked=True,
        repeatable=True,
        max_purchases=5
    )

    # Purchase upgrades
    print("Can buy basic_tools:", um.can_purchase('basic_tools'))
    um.purchase('basic_tools')
    print("Basic tools purchased:", um.is_purchased('basic_tools'))

    print("\nCan buy advanced_tools:", um.can_purchase('advanced_tools'))
    um.purchase('advanced_tools')

    # Get cumulative effects
    print("\nTotal wood bonus:", um.get_effect_value('wood_bonus'))

    # Try repeatable upgrade
    um.purchase('worker_training')
    um.purchase('worker_training')
    print("Worker training efficiency:", um.get_effect_value('worker_efficiency'))

    print("\nAll effects:", um.get_all_effects())
