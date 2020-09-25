# coding: utf8
from enum import Enum, auto


class Statuses(Enum):
    FINISHED = auto()
    IN_THE_WAY = auto()
    CREATED_USER = auto()
    DATA_IS_NOT_FOUND = auto()
    DATABASE_ERROR = auto()
