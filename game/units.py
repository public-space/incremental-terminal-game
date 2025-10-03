"""
Unit Management Module
======================

Manages workers, soldiers, and other unit types.
Handles recruitment, assignment, and unit-based bonuses.

Classes:
    Unit: Individual unit type definition
    UnitManager: Central unit management system

Usage:
    unit_mgr = UnitManager(resource_mgr)
    unit_mgr.register_unit('worker', cost={'food': 10}, produces={'wood': 0.5})
    unit_mgr.recruit('worker', count=5)
    unit_mgr.update_production(delta_time=1.0)
"""

import logging
from typing import Dict, Optional, Callable, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Unit:
    """
    Represents a unit type in the game.

    Attributes:
        name (str): Unique identifier for the unit
        display_name (str): Human-readable name
        description (str): Unit description
        cost (Dict[str, float]): Resources required to recruit {resource: amount}
        count (int): Number of this unit owned
        upkeep (Dict[str, float]): Resources consumed per second {resource: rate}
        produces (Dict[str, float]): Resources produced per second {resource: rate}
        unlocked (bool): Whether unit is available
        max_count (int): Maximum allowed (None = unlimited)
        training_time (float): Time to recruit in seconds (0 = instant)
        effects (Dict[str, float]): Special effects/bonuses
        metadata (dict): Additional custom data
    """
    name: str
    display_name: str = ""
    description: str = ""
    cost: Dict[str, float] = field(default_factory=dict)
    count: int = 0
    upkeep: Dict[str, float] = field(default_factory=dict)
    produces: Dict[str, float] = field(default_factory=dict)
    unlocked: bool = False
    max_count: Optional[int] = None
    training_time: float = 0.0
    effects: Dict[str, float] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set display_name to name if not provided."""
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()

    def can_recruit_more(self) -> bool:
        """
        Check if more units can be recruited.

        Returns:
            bool: True if not at max count
        """
        if self.max_count is None:
            return True
        return self.count < self.max_count

    def get_cost(self, count: int = 1) -> Dict[str, float]:
        """
        Get cost to recruit a number of units.

        Args:
            count: Number of units to recruit

        Returns:
            dict: Total cost
        """
        return {resource: amount * count for resource, amount in self.cost.items()}

    def get_total_production(self) -> Dict[str, float]:
        """
        Get total production from all units.

        Returns:
            dict: Total production rates {resource: rate/s}
        """
        if self.count == 0:
            return {}
        return {resource: rate * self.count for resource, rate in self.produces.items()}

    def get_total_upkeep(self) -> Dict[str, float]:
        """
        Get total upkeep from all units.

        Returns:
            dict: Total upkeep rates {resource: rate/s}
        """
        if self.count == 0:
            return {}
        return {resource: rate * self.count for resource, rate in self.upkeep.items()}

    def to_dict(self) -> dict:
        """
        Serialize unit to dictionary.

        Returns:
            dict: Unit data
        """
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'cost': self.cost,
            'count': self.count,
            'upkeep': self.upkeep,
            'produces': self.produces,
            'unlocked': self.unlocked,
            'max_count': self.max_count,
            'training_time': self.training_time,
            'effects': self.effects,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Unit':
        """
        Deserialize unit from dictionary.

        Args:
            data: Dictionary containing unit data

        Returns:
            Unit: New unit instance
        """
        return cls(**data)


class UnitManager:
    """
    Manages all units, recruitment, and production.

    Attributes:
        units (Dict[str, Unit]): All registered unit types
        resource_manager: Reference to ResourceManager for costs/production
        recruit_callbacks (List[Callable]): Callbacks when units are recruited
    """

    def __init__(self, resource_manager=None):
        """
        Initialize the unit manager.

        Args:
            resource_manager: ResourceManager instance for handling costs/production
        """
        self.units: Dict[str, Unit] = {}
        self.resource_manager = resource_manager
        self.recruit_callbacks: List[Callable] = []
        logger.info("UnitManager initialized")

    def register_unit(
        self,
        name: str,
        cost: Dict[str, float],
        display_name: str = "",
        description: str = "",
        produces: Optional[Dict[str, float]] = None,
        upkeep: Optional[Dict[str, float]] = None,
        unlocked: bool = False,
        max_count: Optional[int] = None,
        training_time: float = 0.0,
        **effects
    ) -> Unit:
        """
        Register a new unit type.

        Args:
            name: Unique unit identifier
            cost: Recruitment cost {resource: amount}
            display_name: Display name for UI
            description: Unit description
            produces: Production rates {resource: rate/s}
            upkeep: Upkeep costs {resource: rate/s}
            unlocked: Whether available initially
            max_count: Maximum number allowed
            training_time: Recruitment time in seconds
            **effects: Additional effects/bonuses

        Returns:
            Unit: The created unit

        Raises:
            ValueError: If unit already exists
        """
        if name in self.units:
            raise ValueError(f"Unit '{name}' already exists")

        unit = Unit(
            name=name,
            display_name=display_name,
            description=description,
            cost=cost,
            produces=produces or {},
            upkeep=upkeep or {},
            unlocked=unlocked,
            max_count=max_count,
            training_time=training_time,
            effects=effects
        )

        self.units[name] = unit
        logger.info(f"Unit registered: {name} (cost={cost})")
        return unit

    def get_unit(self, name: str) -> Optional[Unit]:
        """
        Get a unit by name.

        Args:
            name: Unit identifier

        Returns:
            Unit or None: The unit if found
        """
        return self.units.get(name)

    def has_unit(self, name: str) -> bool:
        """
        Check if a unit type exists.

        Args:
            name: Unit identifier

        Returns:
            bool: True if unit exists
        """
        return name in self.units

    def get_count(self, name: str) -> int:
        """
        Get number of units owned.

        Args:
            name: Unit identifier

        Returns:
            int: Count of units
        """
        unit = self.get_unit(name)
        return unit.count if unit else 0

    def get_total_count(self) -> int:
        """
        Get total count of all units.

        Returns:
            int: Total unit count
        """
        return sum(unit.count for unit in self.units.values())

    def can_recruit(self, name: str, count: int = 1) -> bool:
        """
        Check if unit(s) can be recruited.

        Args:
            name: Unit identifier
            count: Number to recruit

        Returns:
            bool: True if can afford and not at max
        """
        unit = self.get_unit(name)
        if not unit or not unit.unlocked:
            return False

        # Check max count
        if unit.max_count is not None:
            if unit.count + count > unit.max_count:
                return False

        # Check cost
        if self.resource_manager:
            total_cost = unit.get_cost(count)
            return self.resource_manager.can_afford(total_cost)

        return True

    def recruit(self, name: str, count: int = 1) -> bool:
        """
        Recruit one or more units.

        Args:
            name: Unit identifier
            count: Number to recruit

        Returns:
            bool: True if successful
        """
        if not self.can_recruit(name, count):
            logger.debug(f"Cannot recruit {count}x {name}")
            return False

        unit = self.get_unit(name)
        if not unit:
            return False

        # Spend resources
        total_cost = unit.get_cost(count)
        if self.resource_manager:
            if not self.resource_manager.spend_multiple(total_cost):
                return False

        # Add units
        unit.count += count
        logger.info(f"Recruited {count}x {name} (total: {unit.count})")

        # Notify callbacks
        self._notify_recruit(name, count)

        # Update production rates
        self._update_production_rates()

        return True

    def dismiss(self, name: str, count: int = 1) -> bool:
        """
        Dismiss units (no refund).

        Args:
            name: Unit identifier
            count: Number to dismiss

        Returns:
            bool: True if successful
        """
        unit = self.get_unit(name)
        if not unit or unit.count < count:
            return False

        unit.count -= count
        logger.info(f"Dismissed {count}x {name} (remaining: {unit.count})")

        # Update production rates
        self._update_production_rates()

        return True

    def unlock_unit(self, name: str):
        """
        Unlock a unit type.

        Args:
            name: Unit identifier
        """
        unit = self.get_unit(name)
        if unit:
            unit.unlocked = True
            logger.info(f"Unit unlocked: {name}")

    def get_unlocked_units(self) -> List[Unit]:
        """
        Get all unlocked unit types.

        Returns:
            List[Unit]: List of unlocked units
        """
        return [u for u in self.units.values() if u.unlocked]

    def get_recruited_units(self) -> List[Unit]:
        """
        Get all units the player has (count > 0).

        Returns:
            List[Unit]: List of recruited units
        """
        return [u for u in self.units.values() if u.count > 0]

    def get_total_production(self) -> Dict[str, float]:
        """
        Get total production from all units.

        Returns:
            dict: Total production rates {resource: rate/s}
        """
        total_production: Dict[str, float] = {}

        for unit in self.units.values():
            production = unit.get_total_production()
            for resource, rate in production.items():
                total_production[resource] = total_production.get(resource, 0) + rate

        return total_production

    def get_total_upkeep(self) -> Dict[str, float]:
        """
        Get total upkeep from all units.

        Returns:
            dict: Total upkeep rates {resource: rate/s}
        """
        total_upkeep: Dict[str, float] = {}

        for unit in self.units.values():
            upkeep = unit.get_total_upkeep()
            for resource, rate in upkeep.items():
                total_upkeep[resource] = total_upkeep.get(resource, 0) + rate

        return total_upkeep

    def update_production(self, delta_time: float):
        """
        Update resource production and upkeep from all units.

        Args:
            delta_time: Time elapsed since last update (seconds)
        """
        if not self.resource_manager:
            logger.warning("No ResourceManager assigned, cannot update production")
            return

        # Apply production
        total_production = self.get_total_production()
        for resource, rate in total_production.items():
            amount = rate * delta_time
            self.resource_manager.add(resource, amount)

        # Apply upkeep
        total_upkeep = self.get_total_upkeep()
        for resource, rate in total_upkeep.items():
            amount = rate * delta_time
            current = self.resource_manager.get_amount(resource)

            if current < amount:
                # Not enough resources for upkeep
                logger.warning(f"Insufficient {resource} for unit upkeep!")
                # Could implement penalties here (units flee, efficiency drops, etc.)

            self.resource_manager.spend(resource, min(amount, current))

    def _update_production_rates(self):
        """Update resource generation rates based on unit production."""
        if not self.resource_manager:
            return

        # Calculate total production per resource
        total_production = self.get_total_production()

        # Modify resource generation rates
        for resource_name, rate in total_production.items():
            if self.resource_manager.has_resource(resource_name):
                self.resource_manager.modify_generation_rate(resource_name, rate)

    def register_recruit_callback(self, callback: Callable):
        """
        Register callback for when units are recruited.

        Args:
            callback: Function(unit_name, count)
        """
        self.recruit_callbacks.append(callback)

    def _notify_recruit(self, name: str, count: int):
        """
        Notify callbacks of unit recruitment.

        Args:
            name: Unit name
            count: Number recruited
        """
        for callback in self.recruit_callbacks:
            try:
                callback(name, count)
            except Exception as e:
                logger.error(f"Error in recruit callback: {e}", exc_info=True)

    def get_unit_by_category(self, category: str) -> List[Unit]:
        """
        Get units by metadata category.

        Args:
            category: Category name

        Returns:
            List[Unit]: Units in that category
        """
        return [
            u for u in self.units.values()
            if u.metadata.get('category') == category
        ]

    def to_dict(self) -> dict:
        """
        Serialize all units to dictionary.

        Returns:
            dict: All unit data
        """
        return {
            name: unit.to_dict()
            for name, unit in self.units.items()
        }

    def from_dict(self, data: dict):
        """
        Load units from dictionary.

        Args:
            data: Dictionary of unit data
        """
        self.units.clear()
        for name, unit_data in data.items():
            self.units[name] = Unit.from_dict(unit_data)
        logger.info(f"Loaded {len(self.units)} units from data")

        # Update production rates
        self._update_production_rates()

    def reset(self):
        """Clear all units."""
        self.units.clear()
        logger.info("UnitManager reset")


# Example usage
if __name__ == "__main__":
    from resources import ResourceManager

    # Create managers
    rm = ResourceManager()
    rm.add_resource('food', initial=100)
    rm.add_resource('wood', initial=0)
    rm.add_resource('gold', initial=50)

    um = UnitManager(resource_manager=rm)

    # Register units
    um.register_unit(
        'worker',
        cost={'food': 10},
        produces={'wood': 0.5},
        upkeep={'food': 0.1},
        description="Gathers wood",
        unlocked=True
    )

    um.register_unit(
        'miner',
        cost={'food': 15, 'gold': 5},
        produces={'gold': 0.3},
        upkeep={'food': 0.15},
        description="Mines gold",
        unlocked=True
    )

    # Recruit
    print("Can recruit worker:", um.can_recruit('worker'))
    um.recruit('worker', count=3)
    print("Workers owned:", um.get_count('worker'))

    # Check production
    print("Total production:", um.get_total_production())
    print("Total upkeep:", um.get_total_upkeep())

    # Simulate production
    um.update_production(delta_time=10.0)
    print("Wood after 10s:", rm.get_amount('wood'))
    print("Food after 10s (with upkeep):", rm.get_amount('food'))
