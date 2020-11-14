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


class NewUser(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_accept": Cmds.FACCEPT.mk(),
            "cmd_not_accept": Cmds.FNOTACCEPT.mk(),
            "i_cmd_accept": ECmds.FACCEPT.mk(),
            "i_cmd_not_accept": ECmds.FNOTACCEPT.mk(),
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "To get to the city, you need to register."
                     "Read these documents first. This is a privacy "
                     "policy and a license agreement. To continue, "
                     "send a command indicating consent.\n\n"
                     "{i_cmd_accept} To accept: {cmd_accept}\n"
                     "{i_cmd_not_accept} Not to accept: {cmd_not_accept}"
                     ).format(**format_data)

        return emojize(template)


class UserIsReturn(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_inn": Cmds.INN.mk(),
            "i_cmd_inn": ECmds.INN.mk()
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "To get to the city, you need to register... "
                     "Wait, I know you! It seems that with your "
                     "return, we will have to increase patrols "
                     "on the streets.\n\n"
                     "Go to {i_cmd_inn} {cmd_inn}").format(**format_data)
        return emojize(template)


class NewUserIsNotAccept(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_accept": Cmds.FACCEPT.mk(),
            "i_cmd_accept": ECmds.FACCEPT.mk()
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "Unfortunately, I cannot allow you to enter "
                     "the city until you have read and accepted the "
                     "license agreement and privacy policy.\n\n"
                     "{i_cmd_accept} To accept: {cmd_accept}\n"
                     ).format(**format_data)
        return emojize(template)


class NewUserIsAccept(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_fru": Cmds.FRU.mk(),
            "cmd_fen": Cmds.FEN.mk(),
            "i_cmd_en": ECmds.EN.mk(),
            "i_cmd_ru": ECmds.RU.mk()
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "Specify your preferred language.\n\n"
                     "{i_cmd_en} English: {cmd_fen}\n"
                     "{i_cmd_ru} Russian: {cmd_fru}"
                     ).format(**format_data)
        return emojize(template)


class CreateNewHeroHint(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":interrobang: [ <b> Hint </b>]\n"
                     "Choose your name carefully. "
                     "The hero's name can contain uppercase or "
                     "lowercase Latin letters, decimal digits, "
                     "a period, and underscores. The hero's name "
                     "must be between 5 and 20 characters long "
                     "and unique."
                     )

        return emojize(template)


class CreateNewHero(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk()
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "Great! Now tell me your name. To do "
                     "this, send {cmd_name} NickName."
                     ).format(**format_data)

        return emojize(template)


class HeroNickIsNotCorrect(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk(),
        }
        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "The selected hero name is not supported. "
                     "The hero's name can contain uppercase or "
                     "lowercase Latin letters, decimal digits, "
                     "a period, and underscores. The hero's name "
                     "must be between 5 and 20 characters long "
                     "and unique. To do this, send {cmd_name} NickName."
                     ).format(**format_data)

        return emojize(template)


class ViewLanguages(BaseMessage):
    @staticmethod
    def get_template(state=None):
        format_data = {
            "cmd_ru": Cmds.RU.mk(),
            "cmd_en": Cmds.EN.mk(),
            "cmd_inn": Cmds.INN.mk(),
            "i_cmd_ru": ECmds.RU.mk(),
            "i_cmd_en": ECmds.EN.mk(),
            "i_cmd_inn": ECmds.INN.mk()
        }

        template = _(":man_mage: [ <b> Mage Astutus </b>]\n"
                     "You don't seem to be from around here. "
                     "Since I am truly great, I can cast a "
                     "spell on you to turn the local language "
                     "into a suitable one for you. Choose "
                     "which language is right for you.\n\n"
                     "{i_cmd_en} English: {cmd_en}\n"
                     "{i_cmd_ru} Russian: {cmd_ru}\n\n"
                     "Return {i_cmd_inn} inn: {cmd_inn}"
                     ).format(**format_data)

        return emojize(template)


class UserRejectPolicy(BaseMessage):
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_accept": Cmds.SACCEPT.mk(),
            "i_cmd_accept": ECmds.SACCEPT.mk()
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "The user agreement and privacy policy "
                     "may have been changed, or you did not "
                     "give your consent. Please read these "
                     "documents carefully.\n\n"
                     "{i_cmd_accept} To agree: {cmd_accept}\n"
                     ).format(**format_data)
        return emojize(template)


class ViewInnFireSalamander(BaseMessage):
    @staticmethod
    def get_template(state=None):

        template = _(":woman_genie: [<b>Jasmin</b>]"
                     "Silent night...")

        return emojize(template)


class ViewInnFluffyPaws(BaseMessage):
    @staticmethod
    def get_template(state=None):
        template = _(":smile_cat: [<b>Mr. John Wick</b>]"
                     "Silent night...")

        return emojize(template)


class ViewInnDancingHorse(BaseMessage):
    @staticmethod
    def get_template(state=None):
        template = _(":woman_fairy: [<b>Lady Jen</b>]"
                     "Silent night...")

        return emojize(template)


class ViewInnMoonRoad(BaseMessage):
    @staticmethod
    def get_template(state=None):
        template = _(":man_vampire: [<b>Sunny</b>]"
                     "Silent night...")

        return emojize(template)


class ViewSelectInn(BaseMessage):
    @staticmethod
    def get_template(states=None):
        template = _(":guardsman: [ <b>Guardsman Verax</b> ]"
                     "Silent night...")

        return emojize(template)
