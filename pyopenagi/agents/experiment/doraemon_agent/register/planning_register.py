from pyopenagi.agents.experiment.doraemon_agent.moduler.planning.planning import Planning

_AGENT_PLANNING_MAP = {}

def agent_planning(planning_name: str):
    """register agent planning strategy

    Args:
        planning_name (str): agent planning name
    """

    def helper(cls):
        _AGENT_PLANNING_MAP[planning_name] = cls

    return helper


def get_agent_planning(planning_name: str) -> Planning | None:
    """Get agent action by action name

    Args:
        planning_name: agent planning name

    Returns: agent planning strategy if exists, None otherwise

    """
    if planning_name in _AGENT_PLANNING_MAP:
        return _AGENT_PLANNING_MAP[planning_name]
    else:
        return None

DEFAULT_PLANNING = get_agent_planning("normal")
