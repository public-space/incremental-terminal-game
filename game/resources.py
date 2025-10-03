"""
Resource Management Module
===========================

Manages game resources including generation, storage, and transactions.
Provides a flexible system for adding, spending, and tracking resources.

Classes:
    Resource: Individual resource definition
    ResourceManager: Central resource management system

Usage:
    resource_mgr = ResourceManager()
    resource_mgr.add_resource('gold', initial=100, max_storage=1000)
    resource_mgr.spend('gold', 50)
    resource_mgr.generate('gold', 10, delta_time=1.0)
"""

import logging
from typing import Dict, Optional, Callable, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Resource:
    """
    Represents a single resource type in the game.

    Attributes:
        name (str): Unique identifier for the resource
        amount (float): Current amount of the resource
        max_storage (float): Maximum storage capacity (None = unlimited)
        generation_rate (float): Base generation per second
        display_name (str): Human-readable name for UI
        description (str): Description of the resource
        unlocked (bool): Whether the resource is visible to the player
        metadata (dict): Additional custom data
    """
    name: str
    amount: float = 0.0
    max_storage: Optional[float] = None
    generation_rate: float = 0.0
    display_name: str = ""
    description: str = ""
    unlocked: bool = True
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set display_name to name if not provided."""
        if not self.display_name:
            self.display_name = self.name.title()

    def is_full(self) -> bool:
        """
        Check if resource storage is at maximum.

        Returns:
            bool: True if at max storage, False otherwise
        """
        if self.max_storage is None:
            return False
        return self.amount >= self.max_storage

    def space_remaining(self) -> Optional[float]:
        """
        Get remaining storage space.

        Returns:
            float or None: Space remaining, or None if unlimited
        """
        if self.max_storage is None:
            return None
        return max(0, self.max_storage - self.amount)

    def to_dict(self) -> dict:
        """
        Serialize resource to dictionary.

        Returns:
            dict: Resource data
        """
        return {
            'name': self.name,
            'amount': self.amount,
            'max_storage': self.max_storage,
            'generation_rate': self.generation_rate,
            'display_name': self.display_name,
            'description': self.description,
            'unlocked': self.unlocked,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Resource':
        """
        Deserialize resource from dictionary.

        Args:
            data: Dictionary containing resource data

        Returns:
            Resource: New resource instance
        """
        return cls(**data)


class ResourceManager:
    """
    Manages all game resources with generation, storage, and transaction capabilities.

    Attributes:
        resources (Dict[str, Resource]): All registered resources
        transaction_callbacks (List[Callable]): Callbacks for resource transactions
    """

    def __init__(self):
        """Initialize the resource manager."""
        self.resources: Dict[str, Resource] = {}
        self.transaction_callbacks: List[Callable] = []
        logger.info("ResourceManager initialized")

    def add_resource(
        self,
        name: str,
        initial: float = 0.0,
        max_storage: Optional[float] = None,
        generation_rate: float = 0.0,
        display_name: str = "",
        description: str = "",
        unlocked: bool = True,
        **metadata
    ) -> Resource:
        """
        Register a new resource type.

        Args:
            name: Unique resource identifier
            initial: Starting amount
            max_storage: Maximum storage (None = unlimited)
            generation_rate: Base generation per second
            display_name: Display name for UI
            description: Resource description
            unlocked: Whether visible to player
            **metadata: Additional custom data

        Returns:
            Resource: The created resource

        Raises:
            ValueError: If resource already exists
        """
        if name in self.resources:
            raise ValueError(f"Resource '{name}' already exists")

        resource = Resource(
            name=name,
            amount=initial,
            max_storage=max_storage,
            generation_rate=generation_rate,
            display_name=display_name,
            description=description,
            unlocked=unlocked,
            metadata=metadata
        )

        self.resources[name] = resource
        logger.info(f"Resource added: {name} (initial={initial}, rate={generation_rate}/s)")
        return resource

    def get_resource(self, name: str) -> Optional[Resource]:
        """
        Get a resource by name.

        Args:
            name: Resource identifier

        Returns:
            Resource or None: The resource if found
        """
        return self.resources.get(name)

    def has_resource(self, name: str) -> bool:
        """
        Check if a resource exists.

        Args:
            name: Resource identifier

        Returns:
            bool: True if resource exists
        """
        return name in self.resources

    def get_amount(self, name: str) -> float:
        """
        Get current amount of a resource.

        Args:
            name: Resource identifier

        Returns:
            float: Amount of resource, or 0 if not found
        """
        resource = self.get_resource(name)
        return resource.amount if resource else 0.0

    def set_amount(self, name: str, amount: float, clamp: bool = True) -> bool:
        """
        Set resource amount directly.

        Args:
            name: Resource identifier
            amount: New amount
            clamp: Whether to clamp to max_storage

        Returns:
            bool: True if successful
        """
        resource = self.get_resource(name)
        if not resource:
            logger.warning(f"Attempted to set amount for non-existent resource: {name}")
            return False

        old_amount = resource.amount
        resource.amount = amount

        if clamp and resource.max_storage is not None:
            resource.amount = min(resource.amount, resource.max_storage)

        resource.amount = max(0, resource.amount)  # Never negative

        logger.debug(f"Resource '{name}' amount changed: {old_amount} → {resource.amount}")
        self._notify_transaction(name, resource.amount - old_amount, 'set')
        return True

    def add(self, name: str, amount: float) -> float:
        """
        Add to a resource amount.

        Args:
            name: Resource identifier
            amount: Amount to add

        Returns:
            float: Actual amount added (may be less due to storage limits)
        """
        resource = self.get_resource(name)
        if not resource:
            logger.warning(f"Attempted to add to non-existent resource: {name}")
            return 0.0

        old_amount = resource.amount
        resource.amount += amount

        # Clamp to max storage
        if resource.max_storage is not None:
            resource.amount = min(resource.amount, resource.max_storage)

        actual_added = resource.amount - old_amount

        logger.debug(f"Added {actual_added} {name} (requested {amount})")
        self._notify_transaction(name, actual_added, 'add')
        return actual_added

    def spend(self, name: str, amount: float) -> bool:
        """
        Spend/remove resource amount.

        Args:
            name: Resource identifier
            amount: Amount to spend

        Returns:
            bool: True if successful (enough resources available)
        """
        resource = self.get_resource(name)
        if not resource:
            logger.warning(f"Attempted to spend non-existent resource: {name}")
            return False

        if resource.amount < amount:
            logger.debug(f"Insufficient {name}: have {resource.amount}, need {amount}")
            return False

        resource.amount -= amount
        logger.debug(f"Spent {amount} {name} (remaining: {resource.amount})")
        self._notify_transaction(name, -amount, 'spend')
        return True

    def can_afford(self, costs: Dict[str, float]) -> bool:
        """
        Check if player can afford a cost.

        Args:
            costs: Dictionary of {resource_name: amount}

        Returns:
            bool: True if all costs can be paid
        """
        for resource_name, cost in costs.items():
            if self.get_amount(resource_name) < cost:
                return False
        return True

    def spend_multiple(self, costs: Dict[str, float]) -> bool:
        """
        Spend multiple resources at once (atomic transaction).

        Args:
            costs: Dictionary of {resource_name: amount}

        Returns:
            bool: True if successful (all or nothing)
        """
        # Check affordability first
        if not self.can_afford(costs):
            return False

        # Spend all
        for resource_name, cost in costs.items():
            self.spend(resource_name, cost)

        return True

    def generate(self, delta_time: float):
        """
        Generate resources based on generation rates.

        Args:
            delta_time: Time elapsed since last generation (seconds)
        """
        for resource in self.resources.values():
            if resource.generation_rate > 0:
                generated = resource.generation_rate * delta_time
                actual = self.add(resource.name, generated)

                if actual < generated:
                    logger.debug(f"{resource.name} storage full, wasted {generated - actual}")

    def unlock_resource(self, name: str):
        """
        Unlock a resource (make it visible).

        Args:
            name: Resource identifier
        """
        resource = self.get_resource(name)
        if resource:
            resource.unlocked = True
            logger.info(f"Resource unlocked: {name}")

    def get_unlocked_resources(self) -> List[Resource]:
        """
        Get all unlocked resources.

        Returns:
            List[Resource]: List of unlocked resources
        """
        return [r for r in self.resources.values() if r.unlocked]

    def set_generation_rate(self, name: str, rate: float):
        """
        Set resource generation rate.

        Args:
            name: Resource identifier
            rate: New generation rate per second
        """
        resource = self.get_resource(name)
        if resource:
            old_rate = resource.generation_rate
            resource.generation_rate = max(0, rate)
            logger.debug(f"{name} generation rate: {old_rate}/s → {rate}/s")

    def modify_generation_rate(self, name: str, modifier: float):
        """
        Modify generation rate by adding to it.

        Args:
            name: Resource identifier
            modifier: Amount to add to generation rate
        """
        resource = self.get_resource(name)
        if resource:
            self.set_generation_rate(name, resource.generation_rate + modifier)

    def register_transaction_callback(self, callback: Callable):
        """
        Register callback for resource transactions.

        Args:
            callback: Function(resource_name, amount, transaction_type)
        """
        self.transaction_callbacks.append(callback)

    def _notify_transaction(self, name: str, amount: float, transaction_type: str):
        """
        Notify callbacks of a transaction.

        Args:
            name: Resource name
            amount: Amount changed
            transaction_type: Type of transaction ('add', 'spend', 'set')
        """
        for callback in self.transaction_callbacks:
            try:
                callback(name, amount, transaction_type)
            except Exception as e:
                logger.error(f"Error in transaction callback: {e}", exc_info=True)

    def to_dict(self) -> dict:
        """
        Serialize all resources to dictionary.

        Returns:
            dict: All resource data
        """
        return {
            name: resource.to_dict()
            for name, resource in self.resources.items()
        }

    def from_dict(self, data: dict):
        """
        Load resources from dictionary.

        Args:
            data: Dictionary of resource data
        """
        self.resources.clear()
        for name, resource_data in data.items():
            self.resources[name] = Resource.from_dict(resource_data)
        logger.info(f"Loaded {len(self.resources)} resources from data")

    def reset(self):
        """Clear all resources."""
        self.resources.clear()
        logger.info("ResourceManager reset")


# Example usage
if __name__ == "__main__":
    # Create resource manager
    rm = ResourceManager()

    # Add resources
    rm.add_resource('gold', initial=100, generation_rate=1.0, description="Shiny currency")
    rm.add_resource('wood', initial=50, max_storage=500, description="Building material")
    rm.add_resource('stone', initial=0, description="Sturdy material")

    # Simulate generation
    print("Initial gold:", rm.get_amount('gold'))
    rm.generate(delta_time=5.0)  # 5 seconds
    print("After 5s gold:", rm.get_amount('gold'))

    # Spend resources
    if rm.spend('gold', 50):
        print("Spent 50 gold successfully")

    # Check costs
    costs = {'wood': 30, 'stone': 10}
    print("Can afford:", rm.can_afford(costs))

    # Serialize
    print("\nSerialized:", rm.to_dict())
