# coding: utf8
from .cmds import Commands as Cmds
from .cmds import EmojizeCommands as ECmds
from .i18n import I18N
from .icons import emojize


LINK_LA = "https://ya.ru"
LINK_PP = "https://ya.ru"


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
            "link_pp": LINK_PP,
            "link_la": LINK_LA
        }

        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "To enter our game world, you need to read "
                     "and accept the documents below.\n\n "
                     "<a href='{link_la}'>License Agreement</a>\n "
                     "<a href='{link_pp}'>Privacy Policy</a>\n\n"
                     "{i_cmd_accept} To accept: {cmd_accept}\n"
                     "{i_cmd_not_accept} Not to accept: {cmd_not_accept}"
                     ).format(**format_data)

        return emojize(template)


class UserIsReturn(BaseMessage):
    """
    Если пользователь не новый.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_map": Cmds.MAP.mk(),
            "i_cmd_map": ECmds.MAP.mk()
        }

        template = _(":man_cook: [ <b>Innkeeper Bo</b> ]\n"
                     "Decided to return. It is right. "
                     "The road of adventure is waiting for you.\n\n"
                     "Open the Map {i_cmd_map}: {cmd_map}"
                     ).format(**format_data)
        return emojize(template)


class NewUserIsNotAccept(BaseMessage):
    """
    Если новый пользователь не дает свое
    согласие, то мы отдаем ему этот ответ.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_accept": Cmds.FACCEPT.mk(),
            "i_cmd_accept": ECmds.FACCEPT.mk(),
            "link_la": LINK_LA,
            "link_pp": LINK_PP
        }

        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "Unfortunately, until you give me permission, "
                     "I can't let you through. You must read and "
                     "accept the documents listed below.\n\n"
                     "<a href='{link_la}'>License Agreement</a>\n"
                     "<a href='{link_pp}'>Privacy Policy</a>\n\n"
                     "{i_cmd_accept} To accept: {cmd_accept}\n"
                     ).format(**format_data)
        return emojize(template)


class NewUserIsAccept(BaseMessage):
    """
    После того как новый пользователь дал свое согласие,
    предлагаем выбрать ему язык.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_fru": Cmds.FRU.mk(),
            "cmd_fen": Cmds.FEN.mk(),
            "i_cmd_en": ECmds.EN.mk(),
            "i_cmd_ru": ECmds.RU.mk()
        }

        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "Specify your preferred language.\n\n"
                     "{i_cmd_en} English: {cmd_fen}\n"
                     "{i_cmd_ru} Russian: {cmd_fru}"
                     ).format(**format_data)
        return emojize(template)


class UserIsAccept(BaseMessage):
    """
    Пользователь получает свободу перемещения
    после того, как повторно дал согласие с
    политокой конфидициальности и
    пользовательского соглашения.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_map": Cmds.MAP.mk(),
            "i_cmd_map": ECmds.MAP.mk()
        }

        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "Everything is fine now. "
                     "I won't keep you any longer.\n\n"
                     "Open the {i_cmd_map} {cmd_map}"
                     ).format(**format_data)
        return emojize(template)


class CreateNewHeroHint(BaseMessage):
    """
    Подсказка о том, какие требования к
    нику героя.
    """
    @staticmethod
    def get_template(states=None):
        template = _(":interrobang: [ <b> Hint </b>]\n"
                     "Choose your name carefully. "
                     "The hero's name can contain uppercase or "
                     "lowercase Latin letters, decimal digits, "
                     "a period, and underscores. The hero's name "
                     "must be between 5 and 20 characters long "
                     "and unique.")

        return emojize(template)


class CreateNewHero(BaseMessage):
    """
    Создание нового героя.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk()
        }

        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "Great! Now tell me your name. To do "
                     "this, send {cmd_name} NickName."
                     ).format(**format_data)

        return emojize(template)


class HeroNickIsNotCorrect(BaseMessage):
    """
    Сообщаем пользователю, что выбранный
    ник для героя не проходит по ограничениям
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_name": Cmds.HNAME.mk(),
        }
        template = _(":guardsman: [ <b>Knight Verax</b> ]\n"
                     "The selected hero name is not supported. "
                     "The hero's name can contain uppercase or "
                     "lowercase latin letters, decimal digits, "
                     "a period, and underscores. The hero's name "
                     "must be between 5 and 20 characters long "
                     "and unique. To do this, send {cmd_name} NickName."
                     ).format(**format_data)

        return emojize(template)


class ViewLanguages(BaseMessage):
    """
    Секция с языками для пользователя.
    Рассположенна в разделе с настройками.
    """
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
    """
    Сообщаем пользователю, что у него нет
    согласия с пользовательским соглашиением
    и политикой конфидициальности.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_accept": Cmds.SACCEPT.mk(),
            "i_cmd_accept": ECmds.SACCEPT.mk(),
            "link_la": LINK_LA,
            "link_pp": LINK_PP
        }

        template = _(":guardsman: [ <b>Guardsman Verax</b> ]\n"
                     "I'm sorry, I have to keep you. Our documents "
                     "have changed or you have revoked your permission. "
                     "In order to continue, you need to accept "
                     "the documents below:\n\n"
                     "<a href='{link_la}'>License Agreement</a>\n "
                     "<a href='{link_pp}'>Privacy Policy</a>\n\n"
                     "{i_cmd_accept} To agree: {cmd_accept}\n"
                     ).format(**format_data)
        return emojize(template)


class HeroIsNotNew(BaseMessage):
    """
    Герой уже существует у пользователя.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_map": Cmds.MAP.mk(),
            "cmd_satchel": Cmds.SATCHEL.mk(),
            "i_cmd_map": ECmds.MAP.mk(),
            "i_cmd_satchel": ECmds.SATCHEL.mk()
        }

        template = _(":cloud: [ <b>Mysterious cloud</b> ]\n"
                     "You already have a hero.\n\n"
                     "Open the map {i_cmd_map}: {cmd_map}\n"
                     "Open the satchel {i_cmd_satchel}: {cmd_satchel}\n"
                     ).format(**format_data)
        return emojize(template)


class ThereIsNotHero(BaseMessage):
    """
    Герой не существует. Просим создать его.
    """
    @staticmethod
    def get_template(states=None):
        format_data = {
            "cmd_hname": Cmds.HNAME.mk(),
        }

        template = _(":cloud: [ <b>Mysterious cloud</b> ]\n"
                     "You don't have a hero yet. "
                     "To find out how to create "
                     "it send the command: {cmd_hname}"
                     ).format(**format_data)
        return emojize(template)


class NewHeroIsNotUnique(BaseMessage):
    """
    Сообщение о том, что имя героя не униклаьное
    """
    @staticmethod
    def get_template(states=None):
        template = _(":cloud: [ <b>Mysterious cloud</b> ]\n"
                     "This world already has a hero "
                     "with that name. Please choose a "
                     "different name."
                     )
        return emojize(template)
