from pyopenagi.agents.experiment.doraemon_agent.moduler.action.action import Action
from pyopenagi.agents.experiment.doraemon_agent.register.action_register import agent_action
from pyopenagi.utils.logger import AgentLogger

@agent_action("coding")
class ActionCoding(Action):

    def __init__(self):
        self.logger = AgentLogger("coding")

    def run(self, message: str):
        # TODO: run code

        return
