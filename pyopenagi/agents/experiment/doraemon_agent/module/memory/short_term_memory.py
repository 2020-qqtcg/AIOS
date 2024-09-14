from typing import List

from pydantic import BaseModel


class ShortTermMemory(BaseModel):

    messages: List[dict] = []

    def generate_context(
            self, role: str | None = None,
            content: str | None = None,
            tool_call_id: int | None = None) -> List[dict]:
        """Append content into history messages. Generate context from memory messages.

        Args:
            role: role name
            content: request content
            tool_call_id: use when tool call

        Returns: llm context with content appending last

        """
        if role is None and content is None:
            return self.messages

        if tool_call_id:
            message = {"role": role, "content": content, "tool_call_id": tool_call_id}
        else:
            message = {"role": role, "content": content}
        self.messages.append(message)
        return self.messages

    def add_message(self, message: dict) -> None:
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
