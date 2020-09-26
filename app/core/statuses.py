# coding: utf8
from enum import Enum, auto


class Statuses(Enum):
    FINISHED = auto()
    IN_THE_WAY = auto()
    CREATED_USER = auto()
    USER_IS_NOT_FOUND = auto()
    USER_IS_BLOCKER = auto()
    USER_IS_DEVELOPER = auto()
    USER_IS_TESTER = auto()
    USER_HAS_NOT_HERO = auto()
    USER_IS_NOT_THERE = auto()
    HAS_OUT_ANSWER = auto()
    EMERGENCY_STOP = auto()
    DATABASE_ERROR = auto()

