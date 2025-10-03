"""
Structure Definitions
=====================

Dark sci-fi structures for colony.sh.
Each structure is defined as a dictionary for engine consumption.
"""

STRUCTURES = {
    'solar_array': {
        'name': 'solar_array',
        'display_name': 'Solar Array',
        'description': 'Harvests dim starlight. Barely enough.',
        'cost': {
            'metal': 5.0,
        },
        'production': {
            'energy': 3.0,  # Per second
        },
        'consumption': {},
        'count': 1,  # Start with 1 for free
        'max_count': None,
        'unlocked': True,
        'metadata': {
            'icon': '⚡',
            'category': 'Power',
            'flavor': 'The panels are cold to the touch. Inefficient. But they work.',
        }
    },

    'mining_rig': {
        'name': 'mining_rig',
        'display_name': 'Mining Rig',
        'description': 'Drills into dead rock. Hungry for power.',
        'cost': {
            'metal': 10.0,
            'energy': 5.0,
        },
        'production': {
            'metal': 1.5,
        },
        'consumption': {
            'energy': 2.0,  # Constant drain
        },
        'count': 0,
        'max_count': None,
        'unlocked': True,
        'metadata': {
            'icon': '⛏',
            'category': 'Extraction',
            'flavor': 'Grinding metal teeth. They never stop.',
        }
    },

    'reclamation_bay': {
        'name': 'reclamation_bay',
        'display_name': 'Reclamation Bay',
        'description': 'Turns waste into something edible. Don\'t think about it.',
        'cost': {
            'metal': 15.0,
            'energy': 8.0,
        },
        'production': {
            'biomass': 2.0,
        },
        'consumption': {
            'energy': 1.5,
        },
        'count': 0,
        'max_count': None,
        'unlocked': True,
        'metadata': {
            'icon': '🧬',
            'category': 'Life Support',
            'flavor': 'The vats bubble. The smell is... organic.',
        }
    },

    'hab_module': {
        'name': 'hab_module',
        'display_name': 'Hab Module',
        'description': 'Cramped quarters. Better than vacuum.',
        'cost': {
            'metal': 20.0,
            'energy': 10.0,
        },
        'production': {},
        'consumption': {
            'energy': 0.5,  # Life support drain
        },
        'count': 1,  # Start with 1
        'max_count': None,
        'unlocked': True,
        'metadata': {
            'icon': '🏠',
            'category': 'Infrastructure',
            'flavor': 'Thin walls. You hear everything.',
            'colonist_capacity': 5,  # Each hab adds 5 max colonists
        }
    },

    'research_terminal': {
        'name': 'research_terminal',
        'display_name': 'Research Terminal',
        'description': 'Access to corrupted databases. Maybe they\'ll help.',
        'cost': {
            'metal': 25.0,
            'energy': 15.0,
        },
        'production': {},
        'consumption': {
            'energy': 3.0,
        },
        'count': 0,
        'max_count': 3,  # Limited research capacity
        'unlocked': True,
        'metadata': {
            'icon': '🖥',
            'category': 'Research',
            'flavor': 'Flickering screens. Fragments of lost knowledge.',
            'enables_research': True,
        }
    },
}


def get_structure_definitions():
    """
    Get all structure definitions.

    Returns:
        dict: Structure definitions keyed by name
    """
    return STRUCTURES.copy()


def get_starting_structures():
    """
    Get starting structure counts for new game.

    Returns:
        dict: {structure_name: count}
    """
    return {
        'solar_array': 1,  # Start with basic power
        'hab_module': 1,   # Start with basic housing
    }
