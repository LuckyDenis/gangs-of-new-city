# coding: utf8

import logging

from .helpers import Types
from .i18n import I18N
from . import templates as t
from . import keyboards as k

logger = logging.getLogger("answers")

i18n = I18N()


class BaseAnswer:
    @classmethod
    async def get(cls, state):
        i18n.set_locale(state["language"])
        return await cls._get(state)

    @classmethod
    async def _get(cls, state):
        raise NotImplementedError()


class SystemException(BaseAnswer):
    """
    SystemException

    Перезагружаем метод `get` для того,
    что бы использовать язык по умолчанию, так как
    не знаем что могло сломаться, а пользователю
    обезательно нужно отдать ответ.
    """
    @classmethod
    async def get(cls, state):
        return await cls._get(state)

    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.SystemException.get_template(state),
            "keyboard": k.SystemException.get()
        }


class UserIsNotFound(BaseAnswer):
    """
    UserIsNotFound

    Перезагружаем метод `get` так как не нашли
    пользователя, а следовательно, у нас нет языка,
    в котором надо отдать ответ, по этому используем
    язык по умолчанию, пользователю обезательно
    нужно отдать хоть какой-то ответ.
    """
    @classmethod
    async def get(cls, state):
        return await cls._get(state)

    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": "не нашли пользователя"
        }


class NewUser(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        keyboard = k.StartKeyboard.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.StartMessage.get_template(),
            "keyboard": keyboard
        }


class UserIsNotAgree(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        keyboard = k.StartKeyboard.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsNotAgree.get_template(),
            "keyboard": keyboard
        }


class UserIsAgree(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        keyboard = k.Remove.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsAgree.get_template(),
            "keyboard": keyboard
        }


class UserIsAgreeHint(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        keyboard = k.Remove.get()
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsAgreeHint.get_template(),
            "keyboard": keyboard
        }


class UserIsNotNew(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": "нашли пользователя"
        }


class HeroNickIsNotCorrect(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.HeroNickIsNotCorrect.get_template()
        }


class ViewLanguages(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.ViewLanguages.get_template(),
            "keyboard": k.LanguagesKeyboard.get()
        }


class DoesUserHaveAgreeing(BaseAnswer):
    @classmethod
    async def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.DoesUserHaveAgreeing.get_template(),
            "keyboard": k.StartKeyboard.get()
        }
