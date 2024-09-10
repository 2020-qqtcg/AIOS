from typing import List

from pyopenagi.agents.agent_process import AgentProcessFactory
from pyopenagi.agents.base_agent import BaseAgent
from ability import get_agent_ability


class DoraemonAgent(BaseAgent):

    def __init__(
            self,
            agent_name: str,
            task_input: str,
            agent_process_factory: AgentProcessFactory,
            log_mode: str,
            agent_abilities: List[str] | str | None = None,
    ):
        super().__init__(agent_name, task_input, agent_process_factory, log_mode)

        self.abilities = []
        self.load_abilities(agent_abilities)

    def load_abilities(self, agent_abilities) -> None:
        not_found_abilities = []
        for ability_name in agent_abilities:
            if ability := get_agent_ability(ability_name) is not None:
                self.abilities.append(ability)
            else:
                not_found_abilities.append(ability_name)

        if not_found_abilities:
            not_found_abilities_str = ', '.join(not_found_abilities)
            self.logger.log(f"Ability {not_found_abilities_str} does not exist.", "warn")

    def run(self):
        pass
