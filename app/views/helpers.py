# coding: utf8

from enum import Enum
from enum import auto


class Types(Enum):
    TEXT_MESSAGE = auto()

    def __repr__(self):
        return self._name_
