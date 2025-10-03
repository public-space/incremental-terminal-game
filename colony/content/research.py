"""
Research Definitions
====================

Technology tree for colony.sh.
Dark sci-fi upgrades that modify survival mechanics.
"""

RESEARCH = {
    'efficient_extraction': {
        'name': 'efficient_extraction',
        'display_name': 'Efficient Extraction',
        'description': 'Squeeze more from nothing. +50% metal generation.',
        'cost': {
            'metal': 30.0,
            'energy': 20.0,
        },
        'prerequisites': [],
        'effects': {
            'metal_production_multiplier': 1.5,
        },
        'purchased': False,
        'repeatable': False,
        'unlocked': True,
        'metadata': {
            'icon': '⛏+',
            'category': 'Extraction',
            'flavor': 'Sharper drills. Deeper cuts. The rock yields.',
        }
    },

    'closed_loop_bioreactor': {
        'name': 'closed_loop_bioreactor',
        'display_name': 'Closed-Loop Bioreactor',
        'description': 'Less waste. More time. +50% biomass generation.',
        'cost': {
            'metal': 40.0,
            'energy': 25.0,
            'biomass': 10.0,
        },
        'prerequisites': [],
        'effects': {
            'biomass_production_multiplier': 1.5,
        },
        'purchased': False,
        'repeatable': False,
        'unlocked': True,
        'metadata': {
            'icon': '🧬+',
            'category': 'Life Support',
            'flavor': 'The cycle tightens. Nothing is wasted. Everything feeds back.',
        }
    },

    'fusion_ignition': {
        'name': 'fusion_ignition',
        'display_name': 'Fusion Ignition',
        'description': 'Brief hope. Exponential power. +100% energy generation.',
        'cost': {
            'metal': 50.0,
            'energy': 40.0,
        },
        'prerequisites': [],
        'effects': {
            'energy_production_multiplier': 2.0,
        },
        'purchased': False,
        'repeatable': False,
        'unlocked': True,
        'metadata': {
            'icon': '⚡⚡',
            'category': 'Power',
            'flavor': 'The reactor hums. For now, there is enough.',
        }
    },

    'redundant_systems': {
        'name': 'redundant_systems',
        'display_name': 'Redundant Systems',
        'description': 'Backup protocols. -20% energy consumption.',
        'cost': {
            'metal': 35.0,
            'energy': 30.0,
        },
        'prerequisites': [],
        'effects': {
            'energy_consumption_multiplier': 0.8,
        },
        'purchased': False,
        'repeatable': False,
        'unlocked': True,
        'metadata': {
            'icon': '🔧',
            'category': 'Efficiency',
            'flavor': 'Failsafes upon failsafes. When one fails, another wakes.',
        }
    },
}


def get_research_definitions():
    """
    Get all research definitions.

    Returns:
        dict: Research definitions keyed by name
    """
    return RESEARCH.copy()
