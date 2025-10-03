"""
Resource Definitions
====================

Dark sci-fi resources for colony.sh.
Data-oriented design - pure dictionaries for engine consumption.
"""

RESOURCES = {
    'energy': {
        'name': 'energy',
        'display_name': '⚡ Energy',
        'description': 'Life support. Without it, everything stops.',
        'amount': 20.0,
        'max_storage': 100.0,
        'generation_rate': 0.0,
        'unlocked': True,
        'metadata': {
            'icon': '⚡',
            'color': 'cyan',
            'critical_threshold': 10.0,  # Warning below this
        }
    },

    'metal': {
        'name': 'metal',
        'display_name': '⛏ Metal',
        'description': 'Salvaged from dead rock. Construction material.',
        'amount': 10.0,
        'max_storage': 50.0,
        'generation_rate': 0.0,
        'unlocked': True,
        'metadata': {
            'icon': '⛏',
            'color': 'white',
        }
    },

    'biomass': {
        'name': 'biomass',
        'display_name': '🧬 Biomass',
        'description': 'Recycled organic matter. Keeps colonists alive. Don\'t think about it.',
        'amount': 15.0,
        'max_storage': 75.0,
        'generation_rate': 0.0,
        'unlocked': True,
        'metadata': {
            'icon': '🧬',
            'color': 'green',
            'warning': 'Low biomass = starvation',
        }
    },

    'colonists': {
        'name': 'colonists',
        'display_name': '👤 Colonists',
        'description': 'Fragile human units. They break easily.',
        'amount': 3.0,
        'max_storage': 10.0,  # Max capacity from hab modules
        'generation_rate': 0.0,
        'unlocked': True,
        'metadata': {
            'icon': '👤',
            'color': 'yellow',
            'integer_only': True,  # Can't have fractional colonists
            'precious': True,
        }
    },
}


def get_resource_definitions():
    """
    Get all resource definitions.

    Returns:
        dict: Resource definitions keyed by name
    """
    return RESOURCES.copy()


def get_starting_resources():
    """
    Get starting resource amounts for new game.

    Returns:
        dict: {resource_name: amount}
    """
    return {
        'energy': 20.0,
        'metal': 10.0,
        'biomass': 15.0,
        'colonists': 3.0,
    }
