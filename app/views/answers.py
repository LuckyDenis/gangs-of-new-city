# coding: utf8
from .helpers import Types
from .templates import Templates


class BaseAnswers:
    def __init__(self, state):
        self.state = state

    async def get(self):
        raise NotImplementedError()


class NewUser(BaseAnswers):
    async def get(self):
        return {
            "chat_id": self.state["chat_id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": "testing"
        }
