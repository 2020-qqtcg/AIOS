from pyopenagi.agents.experiment.doraemon_agent.module import planning
from pyopenagi.agents.experiment.doraemon_agent.module import action

import pkgutil
import importlib

from .action_register import (
    get_agent_action,
    actions_prompt
)
from .planning_register import (
    get_agent_planning,
    planning_prompt,
    deault_planning
)

def load_all_submodules(package):
    """
    Recursively loads all submodules of a package.

    Given a package, this function will traverse the package's
    submodules and import them all.

    Args:
        package: The package to load submodules from.
    """
    package_path = package.__path__
    for _, name, ispkg in pkgutil.iter_modules(package_path):
        # Get the full name of the submodule
        full_name = f"{package.__name__}.{name}"
        if ispkg:
            # If the submodule is also a package, recursively call
            # this function to load its submodules
            subpackage = importlib.import_module(full_name)
            load_all_submodules(subpackage)
        else:
            # Otherwise, just import the submodule
            importlib.import_module(full_name)

# load trigger decorators
load_all_submodules(planning)
load_all_submodules(action)

__all__ = [
    "get_agent_action",
    "actions_prompt",
    "get_agent_planning",
    "planning_prompt",
    "deault_planning"
]
