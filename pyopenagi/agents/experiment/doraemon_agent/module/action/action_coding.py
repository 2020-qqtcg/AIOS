from pyopenagi.agents.experiment.doraemon_agent.module.action.action import Action
from pyopenagi.agents.experiment.doraemon_agent.register.action_register import agent_action
from pyopenagi.utils.chat_template import Response
from pyopenagi.utils.logger import AgentLogger

ACTION_DESC = """
When you think it is necessary to write code to solve the problem,
you can use the code_solve tool by indicating that you need to write code through code_solve(question).
For example, code_solve(What is the result of 1 + 1).
"""

@agent_action("coding", ACTION_DESC)
class ActionCoding(Action):

    def __init__(self):
        self.logger = AgentLogger("coding")

    def run(self, response: Response):

        return
