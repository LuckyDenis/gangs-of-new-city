# coding: utf8

import logging

from .helpers import Types
from .i18n import I18N
from . import templates as t
from . import keyboards as k

logger = logging.getLogger("answers")

i18n = I18N()


class BaseAnswers:
    @staticmethod
    async def get(self):
        raise NotImplementedError()


class NewUser(BaseAnswers):
    @staticmethod
    async def get(state):
        i18n.set_locale(state["language"])
        keyboard = k.StartKeyboard.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.StartMessage.get_template(),
            "keyboard": keyboard
        }


class UserIsNotAgree(BaseAnswers):
    @staticmethod
    async def get(state):
        i18n.set_locale(state["language"])
        text = t.UserIsNotAgree.get_template()
        keyboard = k.StartKeyboard.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": text,
            "keyboard": keyboard
        }


class UserIsAgree(BaseAnswers):
    @staticmethod
    async def get(state):
        i18n.set_locale(state["language"])
        keyboard = k.Remove.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsAgree.get_template(),
            "keyboard": keyboard
        }


class UserIsAgreeHint(BaseAnswers):
    @staticmethod
    async def get(state):
        i18n.set_locale(state["language"])
        keyboard = k.Remove.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsAgreeHint.get_template(),
            "keyboard": keyboard
        }


class UserIsNotNew(BaseAnswers):
    @staticmethod
    async def get(state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": "нашли пользователя"
        }
