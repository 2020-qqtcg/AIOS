from autogen import ConversableAgent

from aios.sdk import prepare_framework, FrameworkType
from experiment.agent.experiment_agent import ExpirementAgent

_TERMINATION = "<TERMINATION>"


class AutoGenAgent(ExpirementAgent):
    def __init__(self, on_aios: bool = True):
        if on_aios:
            prepare_framework(FrameworkType.AutoGen)

    def run(self, input_str: str):
        assistant_sender = ConversableAgent(
            name="assistant_1",
            system_message="Your name is assistant_1. When you think task is finished, say <TERMINATION>.",
            human_input_mode="NEVER"
        )

        assistant_recipient = ConversableAgent(
            name="assistant_2",
            is_termination_msg=lambda msg: _TERMINATION in msg["content"],
            human_input_mode="NEVER"
        )

        chat_result = assistant_sender.initiate_chat(
            assistant_recipient, message=input_str)

        chat_history = chat_result.chat_history
        for message in reversed(chat_history):
            if "```patch" in message["content"]:
                result = message["content"]
                print(f"AutoGen result is: {result}")
                return message["content"]

        return ""
