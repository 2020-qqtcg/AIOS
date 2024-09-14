from typing import List

from pyopenagi.agents.experiment.doraemon_agent.module.action.action import Action
from pyopenagi.agents.experiment.doraemon_agent.register.action_register import agent_action
from pyopenagi.utils.chat_template import Response
from pyopenagi.utils.logger import AgentLogger

@agent_action("tool",
              "The underlying system supports this feature, and you don't need to do anything extra.")
class ActionTool(Action):

    def __init__(self, tools: List = None):
        self.tools = tools if tools else None
        self.logger = AgentLogger("tool")

    def run(self, response: Response) -> tuple[str, int] | None:
        # execute first tool
        if len(response.tool_calls) > 1:
            tool_call = response.tool_calls[0]
            function_name = tool_call["name"]
            param = tool_call["parameters"]
            tool_call_id = tool_call["id"]
            function = self.tools[function_name]
            function_response = function.run(param)

            return function_response, tool_call_id

        return None
