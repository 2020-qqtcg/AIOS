import time
from typing import List

from pyopenagi.agents.agent_process import AgentProcessFactory
from pyopenagi.agents.base_agent import BaseAgent
from pyopenagi.agents.experiment.doraemon_agent.module.action.action import Action
from pyopenagi.agents.experiment.doraemon_agent.module.memory.short_term_memory import ShortTermMemory
from pyopenagi.agents.experiment.doraemon_agent.prompt.system_prompt import SYSTEM_PROMPT
from pyopenagi.agents.experiment.doraemon_agent.register import (
    get_agent_action,
    actions_prompt,
    get_agent_planning,
    planning_prompt,
    deault_planning
)

_TERMINATE = "<TERMINATE>"


class DoraemonAgent(BaseAgent):

    def __init__(
            self,
            agent_name: str,
            task_input: str,
            agent_process_factory: AgentProcessFactory,
            log_mode: str,
    ):
        super().__init__(agent_name, task_input, agent_process_factory, log_mode)

        self.actions = {}
        self.planning = None
        self.short_term_memory: ShortTermMemory | None = None

        self._load_agent_moduler()
        self.build_system_instruction()

    def run(self):
        self.messages.add_message(role="user", content=self.task_input)

        result = ""
        while not self.is_terminated():
            planning_result = self.planning.plan(self, self.logger)
            if _TERMINATE not in planning_result:
                result = planning_result

        self._set_end_success()
        return self._build_result(result)

    def take_action(self, action_name: str) -> Action:
        action = self.actions[action_name] if action_name in self.actions else None
        if action is None:
            raise AttributeError(f"Action {action_name} not found")
        else:
            return action

    def build_system_instruction(self):
        system_prompt = SYSTEM_PROMPT.format(
            actions=actions_prompt(),
            planning=planning_prompt(self.planning.name),
            terminate=_TERMINATE
        )
        self.messages.add_message(role="system", content=system_prompt)

    def _load_agent_moduler(self):
        """Load module in agent"""
        action_name_list = self.config["action"] if "action" in self.config else []
        planning_name = self.config["planning"] if "planning" in self.config else ""

        self._load_module_actions(action_name_list)
        self._load_module_planning(planning_name)

        self.short_term_memory = ShortTermMemory()

    def _load_module_actions(self, action_name_list: List[str]) -> None:
        not_found_action = []
        for action_name in action_name_list:
            if action := get_agent_action(action_name) is not None:
                action = action()
                self.actions[action_name] = action
            else:
                not_found_action.append(action_name)

        if not_found_action:
            not_found_action_str = ', '.join(not_found_action)
            self.logger.log(f"Action ({not_found_action_str}) do not exist.", "warn")

    def _load_module_planning(self, planning_name: str) -> None:
        if planning := get_agent_planning(planning_name) is not None:
            self.planning = planning()
        else:
            self.planning = deault_planning()

    def is_terminated(self):
        if _TERMINATE in self.messages.last_message()["content"]:
            return True
        return False

    def set_monitor_info(self, start_times, waiting_times, turnaround_times):
        self.request_waiting_times.extend(waiting_times)
        self.request_turnaround_times.extend(turnaround_times)
        if self.rounds == 0:
            self.set_start_time(start_times[0])
        self.rounds += 1

    def _set_end_success(self):
        self.set_status("done")
        self.set_end_time(time=time.time())

    def _build_result(self, result_message: str):
        return {
            "agent_name": self.agent_name,
            "result": result_message,
            "rounds": self.rounds,
            "agent_waiting_time": self.start_time - self.created_time,
            "agent_turnaround_time": self.end_time - self.created_time,
            "request_waiting_times": self.request_waiting_times,
            "request_turnaround_times": self.request_turnaround_times,
        }

    @property
    def messages(self):
        return self.short_term_memory

    @messages.setter
    def messages(self, value):
        pass
