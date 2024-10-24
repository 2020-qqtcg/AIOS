import os
from interpreter import interpreter

from experiment.agent.experiment_agent import ExpirementAgent
from aios.sdk.interpreter.adapter import prepare_interpreter

SYSTEM_PROMPT_WRITE = """\n You can try writing some code to solve the problem, but please note that you are not in the
problem repository. Must write your final patch into patch.diff. If code is hard to run, just write the patch you
think right. You should write patch.diff use Here Document, for example:
    cat <<EOF_59812759871 > patch.diff
    <patch content here>
    EOF_59812759871 \n"""

SYSTEM_PROMPT = """\n You can try writing some code to solve the problem, but please note that you are not in the
problem repository. Finally give me a patch that can be written into git diff file, format like this:
```patch
patch content here
```
"""


class InterpreterAgent(ExpirementAgent):
    def __init__(self):
        # super().__init__("interpreter", agent_process_factory)
        prepare_interpreter()
        interpreter.messages = []
        interpreter.auto_run = True
        self.interpreter = interpreter

    def run(self, input_str: str):

        input_str += SYSTEM_PROMPT
        result = self.interpreter.chat(input_str)

        try:
            result = result[0] if isinstance(result, list) else result
        except IndexError:
            return str(result)

        try:
            # read model output
            current_directory = os.getcwd()
            diff_path = os.path.join(current_directory, "patch.diff")

            with open(diff_path, 'r') as file:
                diff_content = file.read()
                result_content = f"```patch {diff_content}```"

            os.remove(diff_path)

        except Exception:
            result_content = result["content"]
            # content_lines = result_content.split("\n")
            # result_content = "\n".join(content_lines[1:-1])
            # result_content = f"```patch {result_content}```"

        print(f"Interterper result is: {result_content} \n")
        return result_content
