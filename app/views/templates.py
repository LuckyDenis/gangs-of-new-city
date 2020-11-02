# coding: utf8
from .cmds import Commands as Cmds
from .cmds import EmojizeCommands as ECmds
from .i18n import I18N
from .icons import emojize


i18n = I18N()
_ = i18n.gettext_lazy


class BaseMessage:
    @staticmethod
    def get_template(states=None):
        raise NotImplementedError()


class StartMessage(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_not_agree": Cmds.ANO.mk(),
            "cmd_agree": Cmds.AYES.mk(),
            "i_cmd_agree": ECmds.WHITE_CHECK_MARK.mk(),
            "i_cmd_not_agree": ECmds.WARNING.mk(),
        }

        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "To get to the city, you need to register."
                     "Read these documents first. This is a privacy "
                     "policy and a license agreement. To continue, "
                     "send a command indicating consent.\n\n"
                     "{i_cmd_agree} To agree: {cmd_agree}\n"
                     "{i_cmd_not_agree} Not to agree: {cmd_not_agree}"
                     ).format(**format_data)

        return emojize(template)


class SystemException(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "i_cmd_bug": ECmds.BUG.mk(),
            "cmd_bug": Cmds.BUG.mk(),
            **states
        }

        template = _(":teddy_bear: [ <b>Teddy</b> ]\n"
                     "Something went wrong. We don't know what happened, "
                     "so we decided to show you a cute bear so you won't "
                     "be nervous. We would also appreciate it if you let "
                     "us know about this error. To do this, you can send "
                     "a command {i_cmd_bug} {cmd_bug} and follow the "
                     "instructions, or contact us via the feedback "
                     "provided in the description. Index of the message "
                     "where the error occurred: {unique_id}."
                     ).format(**format_data)

        return emojize(template)


class UserIsNotAgree(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_not_agree": Cmds.ANO.mk(),
            "cmd_agree": Cmds.AYES.mk(),
            "i_cmd_agree": ECmds.WHITE_CHECK_MARK.mk(),
            "i_cmd_not_agree": ECmds.WARNING.mk(),
        }

        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "Unfortunately, I cannot allow you to enter "
                     "the city until you have read and accepted the "
                     "license agreement and privacy policy.\n\n"
                     "{i_cmd_agree} To agree: {cmd_agree}\n"
                     "{i_cmd_not_agree} Not to agree: {cmd_not_agree}"
                     ).format(**format_data)
        return emojize(template)


class UserIsAgree(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk(),
        }

        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "Great! Now tell me your name. "
                     "To do this, send {cmd_name} NickName."
                     ).format(**format_data)
        return emojize(template)


class UserIsAgreeHint(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":interrobang: [ <b> Hint </b>]\n"
                     "Choose your name carefully. "
                     "It will be difficult to change your name in the future. "
                     "The name must be unique and must "
                     "not be longer than 20 characters.")

        return emojize(template)


class HeroNickIsNotCorrect(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk(),
        }
        template = _(":guardsman: [ <b>Guardsman</b> ]\n"
                     "The selected hero name is not supported. "
                     "The hero's name can contain uppercase or "
                     "lowercase Latin letters, decimal digits, "
                     "a period, and underscores. The hero's name "
                     "must be between 5 and 20 characters long "
                     "and unique. To do this, send {cmd_name} NickName."
                     ).format(**format_data)

        return emojize(template)
