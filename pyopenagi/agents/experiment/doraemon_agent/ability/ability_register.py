from pyopenagi.agents.experiment.doraemon_agent.ability.base_ability import BaseAbility

AGENT_ABILITY_MAP = {}


def agent_ability(ability_name: str):
    """register agent ability

    Args:
        ability_name (str): agent ability name
    """

    def helper(cls):
        AGENT_ABILITY_MAP[ability_name] = cls

    return helper


def get_agent_ability(ability_name: str) -> BaseAbility | None:
    """Get agent ability by ability name

    Args:
        ability_name: agent ability name

    Returns: agent ability if exists, None otherwise

    """
    if ability_name in AGENT_ABILITY_MAP:
        return AGENT_ABILITY_MAP[ability_name]
    else:
        return None
