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


class EmojizeCommands(Enum):
    _T = ":{0}:"
    WARNING = _T.format("warning")
    WHITE_CHECK_MARK = _T.format("white_check_mark")
    BUG = _T.format("bug")
    LANG = _T.format("globe_with_meridians")
    RU = _T.format("flag_for_Russia")
    EN = _T.format("flag_for_United_States")
    INN = _T.format("beers")

    def __str__(self):
        return f'{self.name}'.lower()

    def mk(self):
        return f"{emojize(self.value)}"

    def get(self):
        return f"^{emojize(self.value)}"
