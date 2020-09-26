# coding: utf8
from enum import Enum
from enum import auto
from enum import unique


@unique
class Commands(Enum):
    def __str__(self):
        return f'{self.name}'.lower()

    START = auto()
