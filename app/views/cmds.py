# coding: utf8
from enum import Enum
from enum import auto
from enum import unique
from .icons import emojize


@unique
class Commands(Enum):
    def __str__(self):
        return f'{self.name}'.lower()

    def mk(self):
        return f'/{self}'

    def get(self):
        return str(self)

    START = auto()
    AYES = auto()
    ANO = auto()
    HNAME = auto()
    BUG = auto()
    INN = auto()
    SETUP = auto()
    HERO = auto()
    SATCHEL = auto()

    # Пользовательское соглашение
    FACCEPT = auto()
    FNOTACCEPT = auto()
    SACCEPT = auto()

    # языки
    LANG = auto()
    FRU = auto()
    FEN = auto()
    RU = auto()
    EN = auto()

    # местность
    MAP = auto()
    FOREST = auto()
    STRONGHOLD = auto()
    SAWMILL = auto()


class EmojizeCommands(Enum):
    _T = ":{0}:"
    WARNING = _T.format("warning")
    WHITE_CHECK_MARK = _T.format("white_check_mark")
    BUG = _T.format("bug")
    INN = _T.format("beers")
    SETUP = _T.format("gear")
    HERO = _T.format("person_in_lotus_position")
    SATCHEL = _T.format("school_backpack")

    # Пользовательское соглашение
    FACCEPT = _T.format("white_check_mark")
    FNOTACCEPT = _T.format("ballot_box_with_check")
    SACCEPT = _T.format("radio_button")

    # языки
    LANG = _T.format("globe_with_meridians")
    RU = _T.format("flag_for_Russia")
    EN = _T.format("flag_for_United_States")

    # местность
    MAP = _T.format("world_map")
    FOREST = _T.format("")
    STRONGHOLD = _T.format("")
    SAWMILL = _T.format("")

    def __str__(self):
        return f'{self.name}'.lower()

    def mk(self):
        return f"{emojize(self.value)}"

    def get(self):
        return f"^{emojize(self.value)}"
