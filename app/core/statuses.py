# coding: utf8
from enum import Enum, auto


class Statuses(Enum):
    FINISHED = auto()
    IN_THE_WAY = auto()
    CREATED_USER = auto()
    GET_USER = auto()
    USER_IS_THERE = auto()
    USER_IS_NOT_THERE = auto()
    HAS_OUT_ANSWER = auto()
    EMERGENCY_STOP = auto()
    DATABASE_ERROR = auto()

    def __repr__(self):
        return self._name_

