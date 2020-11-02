# coding: utf8

from enum import Enum
from enum import auto
from enum import unique


@unique
class Types(Enum):
    TEXT_MESSAGE = auto()
