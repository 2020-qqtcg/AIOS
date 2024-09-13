from pyopenagi.agents.experiment.doraemon_agent.moduler.action.action import Action

_AGENT_ACTION_MAP = {}


def agent_action(action_name: str):
    """register agent action

    Args:
        action_name (str): agent action name
    """

    def helper(cls):
        _AGENT_ACTION_MAP[action_name] = cls

    return helper


def get_agent_action(action_name: str) -> Action | None:
    """Get agent action by action name

    Args:
        action_name: agent action name

    Returns: agent action if exists, None otherwise

    """
    if action_name in _AGENT_ACTION_MAP:
        return _AGENT_ACTION_MAP[action_name]
    else:
        return None
