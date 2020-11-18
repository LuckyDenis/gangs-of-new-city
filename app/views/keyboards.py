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


class NewUserKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_accept} Accept").format(
                i_accept=ECmds.FACCEPT.mk())),
            KeyboardButton(_("{i_not_accept} Not accept").format(
                i_not_accept=ECmds.FNOTACCEPT.mk()
            ))
        )


class UserIsReturnKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_map} Map").format(
                i_map=ECmds.MAP.mk()))
        )


class NewUserIsNotAcceptKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_accept} Accept").format(
                i_accept=ECmds.FACCEPT.mk()))
        )


class UserIsAcceptKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_map} Map").format(
                i_map=ECmds.MAP.mk()))
        )


class UserRejectPolicyKeyboard:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_accept} Accept").format(
                i_accept=ECmds.SACCEPT.mk()))
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


class Default:
    @staticmethod
    def get():
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False
        ).row(
            KeyboardButton(_("{i_map} Map").format(
                i_map=ECmds.MAP.mk()
            ))
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
