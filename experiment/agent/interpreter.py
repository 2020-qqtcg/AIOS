from interpreter import interpreter

from experiment.agent.experiment_agent import ExpirementAgent
from aios.sdk.interpreter.adapter import prepare_interpreter


class InterpreterAgent(ExpirementAgent):
    def __init__(self, agent_process_factory):
        # super().__init__("interpreter", agent_process_factory)
        prepare_interpreter(agent_process_factory)
        interpreter.messages = []
        interpreter.auto_run = True
        self.interpreter = interpreter

    def run(self, input_str: str):

        input_str += ("\n You can try writing some code to solve the problem, but please note that you are not in the "
                      "problem repository.")
        result = self.interpreter.chat(input_str)
        result = result[0] if isinstance(result, list) else result
        return result["content"]
