from typing import Any

_AGENT_PLANNING_MAP = {}
_AGENT_PLANNING_DESC_MAP = {}


def agent_planning(planning_name: str, planning_desc: str):
    """
    register agent planning strategy

    Args:
        planning_name: agent planning name
        planning_desc: agent planning description

    """

    def helper(cls):
        _AGENT_PLANNING_MAP[planning_name] = cls
        _AGENT_PLANNING_DESC_MAP[planning_name] = planning_desc
        print(f"Planning {planning_name} has been registerd.")

    return helper


def get_agent_planning(planning_name: str) -> Any:
    """
    Get agent action by action name

    Args:
        planning_name: agent planning name

    Returns: agent planning strategy if exists, None otherwise

    """
    if planning_name in _AGENT_PLANNING_MAP:
        return _AGENT_PLANNING_MAP[planning_name]
    else:
        return None


def planning_prompt(planning_name: str) -> str:
    """
    Get the prompt string of the given planning name.

    Args:
        planning_name: The name of the planning.

    Returns:
        The prompt string if the planning exists, otherwise an empty string.
    """
    if planning_name in _AGENT_PLANNING_DESC_MAP:
        planning_prompt_str = f"- {planning_name}: {_AGENT_PLANNING_DESC_MAP[planning_name]}"
    else:
        planning_prompt_str = ""
    return planning_prompt_str


def deault_planning():
    return get_agent_planning("normal")()
