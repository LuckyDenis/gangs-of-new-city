# coding: utf8

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from .i18n import I18N
from .cmds import EmojizeCommands as ECmds


i18n = I18N()
_ = i18n.gettext_lazy


class StartKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_agree} To agree").format(
                i_agree=ECmds.WHITE_CHECK_MARK.mk())),
            KeyboardButton(_("{i_not_agree} Not to agree").format(
                i_not_agree=ECmds.WARNING.mk()
            ))
        )


class Remove:
    @staticmethod
    def get():
        return ReplyKeyboardRemove()


class SystemException:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_bug} Bug").format(
                i_bug=ECmds.BUG.mk()
            ))
        )
