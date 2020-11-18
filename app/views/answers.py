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
    def get(cls, state):
        i18n.set_locale(state["language"])
        return cls._get(state)

    @classmethod
    def _get(cls, state):
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
    def get(cls, state):
        return cls._get(state)

    @classmethod
    def _get(cls, state):
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
    def get(cls, state):
        return cls._get(state)

    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": "не нашли пользователя"
        }


class NewUser(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.NewUser.get_template(),
            "keyboard": k.NewUserKeyboard.get(),
            "disable_web_page_preview": True
        }


class NewUserIsNotAccept(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.NewUserIsNotAccept.get_template(),
            "keyboard": k.NewUserIsNotAcceptKeyboard.get(),
            "disable_web_page_preview": True
        }


class NewUserIsAccept(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.NewUserIsAccept.get_template(),
            "keyboard": k.Remove.get()
        }


class UserIsAccept(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.NewUserIsAccept.get_template(),
            "keyboard": k.Remove.get()
        }


class UserIsReturn(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserIsReturn.get_template(),
            "keyboard": k.UserIsReturnKeyboard.get()
        }


class UserRejectPolicy(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.UserRejectPolicy.get_template(),
            "keyboard": k.UserRejectPolicyKeyboard.get()
        }


class ViewLanguages(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.ViewLanguages.get_template(),
            "keyboard": k.LanguagesKeyboard.get()
        }


class HeroNickIsNotCorrect(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.HeroNickIsNotCorrect.get_template()
        }


class CreateNewHeroHint(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.CreateNewHeroHint.get_template()
        }


class CreateNewHero(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.CreateNewHero.get_template(),
            "keyboard": k.Remove.get()
        }


class HeroIsNotNew(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.HeroIsNotNew.get_template(),
            "keyboard": k.Default.get()
        }


class ThereIsNotHero(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.ThereIsNotHero.get_template(),
            "keyboard": k.Remove.get()
        }


class NewHeroIsNotUnique(BaseAnswer):
    @classmethod
    def _get(cls, state):
        return {
            "chat_id": state["id"],
            "message_type": Types.TEXT_MESSAGE,
            "text": t.NewHeroIsNotUnique.get_template(),
            "keyboard": k.Remove.get()
        }
