"""
Building Management Module
===========================

Manages buildings, their construction, production, and upgrades.
Provides a flexible system for defining building types and their effects.

Classes:
    Building: Individual building definition
    BuildingManager: Central building management system

Usage:
    building_mgr = BuildingManager(resource_mgr)
    building_mgr.register_building('farm', cost={'wood': 50}, produces={'food': 1.0})
    building_mgr.build('farm')
    building_mgr.update_production(delta_time=1.0)
"""

import logging
from typing import Dict, Optional, Callable, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Building:
    """
    Represents a building type in the game.

    Attributes:
        name (str): Unique identifier for the building
        display_name (str): Human-readable name
        description (str): Building description
        cost (Dict[str, float]): Resources required to build {resource: amount}
        count (int): Number of this building owned
        produces (Dict[str, float]): Resources produced per second {resource: rate}
        consumes (Dict[str, float]): Resources consumed per second {resource: rate}
        unlocked (bool): Whether building is available
        max_count (int): Maximum allowed (None = unlimited)
        build_time (float): Time to construct in seconds (0 = instant)
        effects (Dict[str, float]): Special effects/bonuses
        metadata (dict): Additional custom data
    """
    name: str
    display_name: str = ""
    description: str = ""
    cost: Dict[str, float] = field(default_factory=dict)
    count: int = 0
    produces: Dict[str, float] = field(default_factory=dict)
    consumes: Dict[str, float] = field(default_factory=dict)
    unlocked: bool = False
    max_count: Optional[int] = None
    build_time: float = 0.0
    effects: Dict[str, float] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set display_name to name if not provided."""
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()

    def can_build_more(self) -> bool:
        """
        Check if more of this building can be built.

        Returns:
            bool: True if not at max count
        """
        if self.max_count is None:
            return True
        return self.count < self.max_count

    def get_cost(self, count: int = 1) -> Dict[str, float]:
        """
        Get cost to build a number of buildings.

        Args:
            count: Number of buildings to build

        Returns:
            dict: Total cost
        """
        return {resource: amount * count for resource, amount in self.cost.items()}

    def get_total_production(self) -> Dict[str, float]:
        """
        Get total production from all owned buildings.

        Returns:
            dict: Total production rates {resource: rate/s}
        """
        if self.count == 0:
            return {}
        return {resource: rate * self.count for resource, rate in self.produces.items()}

    def get_total_consumption(self) -> Dict[str, float]:
        """
        Get total consumption from all owned buildings.

        Returns:
            dict: Total consumption rates {resource: rate/s}
        """
        if self.count == 0:
            return {}
        return {resource: rate * self.count for resource, rate in self.consumes.items()}

    def to_dict(self) -> dict:
        """
        Serialize building to dictionary.

        Returns:
            dict: Building data
        """
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'cost': self.cost,
            'count': self.count,
            'produces': self.produces,
            'consumes': self.consumes,
            'unlocked': self.unlocked,
            'max_count': self.max_count,
            'build_time': self.build_time,
            'effects': self.effects,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Building':
        """
        Deserialize building from dictionary.

        Args:
            data: Dictionary containing building data

        Returns:
            Building: New building instance
        """
        return cls(**data)


class BuildingManager:
    """
    Manages all buildings, construction, and production.

    Attributes:
        buildings (Dict[str, Building]): All registered building types
        resource_manager: Reference to ResourceManager for costs/production
        build_callbacks (List[Callable]): Callbacks when buildings are built
    """

    def __init__(self, resource_manager=None):
        """
        Initialize the building manager.

        Args:
            resource_manager: ResourceManager instance for handling costs/production
        """
        self.buildings: Dict[str, Building] = {}
        self.resource_manager = resource_manager
        self.build_callbacks: List[Callable] = []
        logger.info("BuildingManager initialized")

    def register_building(
        self,
        name: str,
        cost: Dict[str, float],
        display_name: str = "",
        description: str = "",
        produces: Optional[Dict[str, float]] = None,
        consumes: Optional[Dict[str, float]] = None,
        unlocked: bool = False,
        max_count: Optional[int] = None,
        build_time: float = 0.0,
        **effects
    ) -> Building:
        """
        Register a new building type.

        Args:
            name: Unique building identifier
            cost: Build cost {resource: amount}
            display_name: Display name for UI
            description: Building description
            produces: Production rates {resource: rate/s}
            consumes: Consumption rates {resource: rate/s}
            unlocked: Whether available initially
            max_count: Maximum number allowed
            build_time: Construction time in seconds
            **effects: Additional effects/bonuses

        Returns:
            Building: The created building

        Raises:
            ValueError: If building already exists
        """
        if name in self.buildings:
            raise ValueError(f"Building '{name}' already exists")

        building = Building(
            name=name,
            display_name=display_name,
            description=description,
            cost=cost,
            produces=produces or {},
            consumes=consumes or {},
            unlocked=unlocked,
            max_count=max_count,
            build_time=build_time,
            effects=effects
        )

        self.buildings[name] = building
        logger.info(f"Building registered: {name} (cost={cost})")
        return building

    def get_building(self, name: str) -> Optional[Building]:
        """
        Get a building by name.

        Args:
            name: Building identifier

        Returns:
            Building or None: The building if found
        """
        return self.buildings.get(name)

    def has_building(self, name: str) -> bool:
        """
        Check if a building type exists.

        Args:
            name: Building identifier

        Returns:
            bool: True if building exists
        """
        return name in self.buildings

    def get_count(self, name: str) -> int:
        """
        Get number of buildings owned.

        Args:
            name: Building identifier

        Returns:
            int: Count of buildings
        """
        building = self.get_building(name)
        return building.count if building else 0

    def can_build(self, name: str, count: int = 1) -> bool:
        """
        Check if building(s) can be built.

        Args:
            name: Building identifier
            count: Number to build

        Returns:
            bool: True if can afford and not at max
        """
        building = self.get_building(name)
        if not building or not building.unlocked:
            return False

        # Check max count
        if building.max_count is not None:
            if building.count + count > building.max_count:
                return False

        # Check cost
        if self.resource_manager:
            total_cost = building.get_cost(count)
            return self.resource_manager.can_afford(total_cost)

        return True

    def build(self, name: str, count: int = 1) -> bool:
        """
        Build one or more buildings.

        Args:
            name: Building identifier
            count: Number to build

        Returns:
            bool: True if successful
        """
        if not self.can_build(name, count):
            logger.debug(f"Cannot build {count}x {name}")
            return False

        building = self.get_building(name)
        if not building:
            return False

        # Spend resources
        total_cost = building.get_cost(count)
        if self.resource_manager:
            if not self.resource_manager.spend_multiple(total_cost):
                return False

        # Add buildings
        building.count += count
        logger.info(f"Built {count}x {name} (total: {building.count})")

        # Notify callbacks
        self._notify_build(name, count)

        # Update production rates
        self._update_production_rates()

        return True

    def demolish(self, name: str, count: int = 1) -> bool:
        """
        Demolish buildings (no refund).

        Args:
            name: Building identifier
            count: Number to demolish

        Returns:
            bool: True if successful
        """
        building = self.get_building(name)
        if not building or building.count < count:
            return False

        building.count -= count
        logger.info(f"Demolished {count}x {name} (remaining: {building.count})")

        # Update production rates
        self._update_production_rates()

        return True

    def unlock_building(self, name: str):
        """
        Unlock a building type.

        Args:
            name: Building identifier
        """
        building = self.get_building(name)
        if building:
            building.unlocked = True
            logger.info(f"Building unlocked: {name}")

    def get_unlocked_buildings(self) -> List[Building]:
        """
        Get all unlocked building types.

        Returns:
            List[Building]: List of unlocked buildings
        """
        return [b for b in self.buildings.values() if b.unlocked]

    def get_owned_buildings(self) -> List[Building]:
        """
        Get all buildings the player owns (count > 0).

        Returns:
            List[Building]: List of owned buildings
        """
        return [b for b in self.buildings.values() if b.count > 0]

    def get_total_production(self) -> Dict[str, float]:
        """
        Get total production from all buildings.

        Returns:
            dict: Total production rates {resource: rate/s}
        """
        total_production: Dict[str, float] = {}

        for building in self.buildings.values():
            production = building.get_total_production()
            for resource, rate in production.items():
                total_production[resource] = total_production.get(resource, 0) + rate

        return total_production

    def get_total_consumption(self) -> Dict[str, float]:
        """
        Get total consumption from all buildings.

        Returns:
            dict: Total consumption rates {resource: rate/s}
        """
        total_consumption: Dict[str, float] = {}

        for building in self.buildings.values():
            consumption = building.get_total_consumption()
            for resource, rate in consumption.items():
                total_consumption[resource] = total_consumption.get(resource, 0) + rate

        return total_consumption

    def update_production(self, delta_time: float):
        """
        Update resource production from all buildings.

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

        # Apply consumption
        total_consumption = self.get_total_consumption()
        for resource, rate in total_consumption.items():
            amount = rate * delta_time
            self.resource_manager.spend(resource, amount)

    def _update_production_rates(self):
        """Update resource generation rates based on building production."""
        if not self.resource_manager:
            return

        # Calculate total production and consumption per resource
        total_production = self.get_total_production()
        total_consumption = self.get_total_consumption()

        # Update resource generation rates (net production - consumption)
        all_resources = set(total_production.keys()) | set(total_consumption.keys())
        for resource_name in all_resources:
            production = total_production.get(resource_name, 0)
            consumption = total_consumption.get(resource_name, 0)
            net_rate = production - consumption

            if self.resource_manager.has_resource(resource_name):
                self.resource_manager.set_generation_rate(resource_name, net_rate)

    def register_build_callback(self, callback: Callable):
        """
        Register callback for when buildings are built.

        Args:
            callback: Function(building_name, count)
        """
        self.build_callbacks.append(callback)

    def _notify_build(self, name: str, count: int):
        """
        Notify callbacks of building construction.

        Args:
            name: Building name
            count: Number built
        """
        for callback in self.build_callbacks:
            try:
                callback(name, count)
            except Exception as e:
                logger.error(f"Error in build callback: {e}", exc_info=True)

    def get_building_by_category(self, category: str) -> List[Building]:
        """
        Get buildings by metadata category.

        Args:
            category: Category name

        Returns:
            List[Building]: Buildings in that category
        """
        return [
            b for b in self.buildings.values()
            if b.metadata.get('category') == category
        ]

    def to_dict(self) -> dict:
        """
        Serialize all buildings to dictionary.

        Returns:
            dict: All building data
        """
        return {
            name: building.to_dict()
            for name, building in self.buildings.items()
        }

    def from_dict(self, data: dict):
        """
        Load buildings from dictionary.

        Args:
            data: Dictionary of building data
        """
        self.buildings.clear()
        for name, building_data in data.items():
            self.buildings[name] = Building.from_dict(building_data)
        logger.info(f"Loaded {len(self.buildings)} buildings from data")

        # Update production rates
        self._update_production_rates()

    def reset(self):
        """Clear all buildings."""
        self.buildings.clear()
        logger.info("BuildingManager reset")


# Example usage
if __name__ == "__main__":
    from resources import ResourceManager

    # Create managers
    rm = ResourceManager()
    rm.add_resource('wood', initial=100)
    rm.add_resource('food', initial=0)
    rm.add_resource('stone', initial=50)

    bm = BuildingManager(resource_manager=rm)

    # Register buildings
    bm.register_building(
        'farm',
        cost={'wood': 30},
        produces={'food': 1.0},
        description="Produces food",
        unlocked=True
    )

    bm.register_building(
        'lumber_mill',
        cost={'wood': 50, 'stone': 20},
        produces={'wood': 0.5},
        description="Produces wood",
        unlocked=True
    )

    # Build
    print("Can build farm:", bm.can_build('farm'))
    bm.build('farm', count=2)
    print("Farms owned:", bm.get_count('farm'))

    # Check production
    print("Total production:", bm.get_total_production())

    # Simulate production
    bm.update_production(delta_time=10.0)
    print("Food after 10s:", rm.get_amount('food'))
