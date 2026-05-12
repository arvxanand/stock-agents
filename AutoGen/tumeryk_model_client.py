from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage, SystemMessage
from autogen_core.models import ChatCompletionClient

class TumerykModelClient(ChatCompletionClient):
    """
    Wrapper around OpenAIChatCompletionClient that fixes the system message
    issue on our Tumeryk instance.
    
    The problem: Tumeryk ignores {"role": "system"} messages.
    The fix: Take the system message content, prepend it to the user message,
    and send everything as a single user message.
    
    AutoGen agents don't know this wrapper exists — they use system_message
    normally and this class handles the conversion silently.
    """

    def __init__(self, **kwargs):
        self._client = OpenAIChatCompletionClient(**kwargs)
    
    def _fix_messages(self, messages):
        """
        Take a list of messages from AutoGen, find any SystemMessage,
        and merge its content into the UserMessage.
        
        Before: [SystemMessage("Be a pirate"), UserMessage("What is the capital?")]
        After:  [UserMessage("Instructions: Be a pirate\n\nUser request: What is the capital?")]
        """
        system_content = None
        other_messages = []

        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_content = msg.content
            else:
                other_messages.append(msg)

        if system_content and len(other_messages) > 0:
            last_msg = other_messages[-1]
            if isinstance(last_msg, UserMessage):
                combined = f"Instructions: {system_content}\n\nUser request: {last_msg.content}"
                other_messages[-1] = UserMessage(content=combined, source=last_msg.source)

        return other_messages
    
    async def create(self, messages, **kwargs):
        fixed = self._fix_messages(messages)
        return await self._client.create(fixed, **kwargs)

    def create_stream(self, messages, **kwargs):
        fixed = self._fix_messages(messages)
        return self._client.create_stream(fixed, **kwargs)

    async def close(self):
        await self._client.close()

    @property
    def model_info(self):
        return self._client.model_info

    @property
    def capabilities(self):
        return self._client.capabilities
    
    @property
    def actual_usage(self):
        return self._client.actual_usage

    @property
    def total_usage(self):
        return self._client.total_usage

    def count_tokens(self, messages, **kwargs):
        return self._client.count_tokens(messages, **kwargs)

    def remaining_tokens(self, messages, **kwargs):
        return self._client.remaining_tokens(messages, **kwargs)