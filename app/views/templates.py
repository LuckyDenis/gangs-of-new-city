# coding: utf8
from app.helpers import Cmds
from .i18n import I18N
from .emoji import emojize


i18n = I18N()
_ = i18n.gettext_lazy


class BaseMessage:
    @staticmethod
    def get_template(states=None):
        raise NotImplementedError()


class StartMessage(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "To get to the city, you need to register."
                     "Read these documents first. This is a privacy "
                     "policy and a license agreement. To continue, "
                     "send a command indicating consent.\n\n"
                     ":white_check_mark: To agree: {cmd_agree}\n"
                     ":warning: Not to agree: {cmd_not_agree}").format(
            cmd_not_agree=Cmds.ANO.mk(),
            cmd_agree=Cmds.AYES.mk()
        )
        if states:
            template.format(states)
        return emojize(template)


class UserIsNotAgree(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "Unfortunately, I cannot allow you to enter "
                     "the city until you have read and accepted the "
                     "license agreement and privacy policy.\n\n"
                     ":white_check_mark: To agree: {cmd_agree}\n"
                     ":warning: Not to agree: {cmd_not_agree}").format(
            cmd_not_agree=Cmds.ANO.mk(),
            cmd_agree=Cmds.AYES.mk()
        )
        if states:
            template.format(states)
        return emojize(template)


class UserIsAgree(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "Great! Now tell me your name. "
                     "To do this, send {cmd_name} NickName.\n\n"
                     ).format(
            cmd_name=Cmds.HNAME.mk()
        )
        if states:
            template.format(states)
        return emojize(template)


class UserIsAgreeHint(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":interrobang: [ <b> Hint </b>]\n"
                     "Choose your name carefully. "
                     "It will be difficult to change your name in the future. "
                     "The name must be unique and must "
                     "not be longer than 20 characters.")
        if states:
            template.format(states)
        return emojize(template)
