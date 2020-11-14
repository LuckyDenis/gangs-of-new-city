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
    LANG = auto()
    EN = auto()
    RU = auto()
    INN = auto()
    SETUP = auto()
    HERO = auto()
    SATCHEL = auto()

    FACCEPT = auto()
    FNOTACCEPT = auto()
    SACCEPT = auto()

    FRU = auto()
    FEN = auto()

    INTO_FS = auto()
    INTO_FP = auto()
    INTO_DH = auto()
    INTO_MR = auto()


class EmojizeCommands(Enum):
    _T = ":{0}:"
    WARNING = _T.format("warning")
    WHITE_CHECK_MARK = _T.format("white_check_mark")
    BUG = _T.format("bug")
    LANG = _T.format("globe_with_meridians")
    RU = _T.format("flag_for_Russia")
    EN = _T.format("flag_for_United_States")
    INN = _T.format("beers")
    SETUP = _T.format("gear")
    HERO = _T.format("bust_in_silhouette")
    SATCHEL = _T.format("school_backpack")

    FACCEPT = _T.format("white_check_mark")
    FNOTACCEPT = _T.format("ballot_box_with_check")

    SACCEPT = _T.format("radio_button")

    INTO_FS = _T.format("")
    INTO_FP = _T.format("")
    INTO_DH = _T.format("")
    INTO_MR = _T.format("")

    GANG_RED = _T.format("")
    GANG_YELLOW = _T.format("")
    GANG_GREEN = _T.format("")
    GANG_PURPLE = _T.format("")

    def __str__(self):
        return f'{self.name}'.lower()

    def mk(self):
        return f"{emojize(self.value)}"

    def get(self):
        return f"^{emojize(self.value)}"
