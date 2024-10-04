from interpreter import OpenInterpreter

from experiment.agent.experiment_agent import ExpirementAgent
from aios.sdk.interpreter.adapter import prepare_interpreter


class InterpreterAgent(ExpirementAgent):
    def __init__(self, agent_process_factory):
        # super().__init__("interpreter", agent_process_factory)
        prepare_interpreter(agent_process_factory)
        self.interpreter = OpenInterpreter()

    def run(self, input_str: str):
        result = self.interpreter.chat(input_str)
        result = result[0] if isinstance(result, list) else result
        return result["content"]
