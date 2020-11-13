# coding: utf8

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from .i18n import I18N
from .cmds import EmojizeCommands as ECmds


i18n = I18N()
_ = i18n.gettext_lazy


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


class LanguagesKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_en} English").format(
                i_en=ECmds.EN.mk())),
            KeyboardButton(_("{i_ru} Russian").format(
                i_ru=ECmds.RU.mk()
            ))
        ).row(
            KeyboardButton(_("{i_inn} Inn").format(
                i_inn=ECmds.INN.mk()
            ))
        )


class InnKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_hero} Hero").format(
                i_hero=ECmds.HERO.mk()
            )),
            KeyboardButton(_("{i_satchel} Satchel").format(
                i_satchel=ECmds.SATCHEL.mk()
            )),
            KeyboardButton(_("{i_setup} Setup").format(
                i_setup=ECmds.SETUP.mk()
            ))
        )


class SelectInnKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_salamander} Fire Salamander").format(
                i_hero=ECmds.HERO.mk()
            ))
        ).row(
            KeyboardButton(_("{i_salamander} Fire Salamander").format(
                i_hero=ECmds.HERO.mk()
            ))
        )
