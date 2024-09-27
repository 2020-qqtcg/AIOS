from typing import Any

_AGENT_ACTION_MAP = {}
_AGENT_ACTION_DESC_MAP = {}


def agent_action(action_name: str, action_desc: str):
    """
    register agent action

    Args:
        action_desc: action description
        action_name: agent action name
    """

    def helper(cls):
        _AGENT_ACTION_MAP[action_name] = cls
        _AGENT_ACTION_DESC_MAP[action_name] = action_desc
        print(f"Action {action_name} has been registerd.")

    return helper


def get_agent_action(action_name: str) -> Any:
    """
    Get agent action by action name

    Args:
        action_name: agent action name

    Returns: agent action if exists, None otherwise

    """
    if action_name in _AGENT_ACTION_MAP:
        return _AGENT_ACTION_MAP[action_name]
    else:
        return None


def actions_prompt() -> str:
    """
    Get actions prompt

    Returns: actions prompt

    """
    action_prompt_str = ""
    for action_name, action_desc in _AGENT_ACTION_DESC_MAP.items():
        action_prompt_str += f"- {action_name}: {action_desc}\n"
    return action_prompt_str
