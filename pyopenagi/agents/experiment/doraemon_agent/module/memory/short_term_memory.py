from typing import List


class ShortTermMemory:

    def __init__(self):
        self.messages: List[dict] = []

    def generate_context(self) -> List[dict]:
        """Generate context from memory messages.

        Returns: llm context with content appending last

        """
        return self.messages

    def add_message(self, **kwargs) -> None:
        role = kwargs.get("role", None)
        content = kwargs.get("content", None)
        tool_call_id = kwargs.get("tool_call_id", None)

        if tool_call_id is None:
            self._add_message({"role": role, "content": content})
        else:
            self._add_message({"role": role, "content": content, "tool_call_id": tool_call_id})

    def _add_message(self, message: dict) -> None:
        """
        Add message to memory.
        Args:
            message: message to add

        """
        self.messages.append(message)

    def clear_history(self) -> None:
        """Clear messages
        """
        self.messages = []

    def last_message(self):
        """Get last message in memory messages

        Returns: last message

        """
        if len(self.messages) > 0:
            return self.messages[-1]
        else:
            return []
