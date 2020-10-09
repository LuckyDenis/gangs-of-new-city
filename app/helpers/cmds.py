# coding: utf8
from enum import Enum
from enum import auto
from enum import unique


@unique
class Commands(Enum):
    def __str__(self):
        return f'{self.name}'.lower()

    def mk(self):
        return f'/{self}'

    START = auto()
    AYES = auto()
    ANO = auto()
    HNAME = auto()
