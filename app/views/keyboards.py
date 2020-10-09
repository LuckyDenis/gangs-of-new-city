# coding: utf8

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from .emoji import emojize as e
from .i18n import I18N

i18n = I18N()
_ = i18n.gettext_lazy


class StartKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(e(_(f":white_check_mark: To agree"))),
            KeyboardButton(e(_(f":warning: Not to agree")))
        )


class Remove:
    @staticmethod
    def get():
        return ReplyKeyboardRemove()
