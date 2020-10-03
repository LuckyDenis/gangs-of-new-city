# coding: utf8
from enum import Enum, auto, unique
"""
Статус коды используется для лучшего понимаю,
того что происходит в системе. Данные `train.Train`
будут писаться в лог. А по списку сататус кодов можно
будет понять, какие этапы прошел пользовательский запрос
без просмотра списка станций.
"""


@unique
class Statuses(Enum):
    NEW_HERO_IS_NOT_UNIQUE = auto()
    NEW_HERO_IS_UNIQUE = auto()
    HEW_HERO_CREATE = auto()
    ADD_REFERRAL_DATA = auto()
    DATABASE_ERROR = auto()
    EMERGENCY_STOP = auto()
    FINISHED = auto()
    GET_HERO = auto()
    GET_INVITER = auto()
    GET_USER = auto()
    HAS_OUT_ANSWER = auto()
    INVITER_IS_NOT_THERE = auto()
    INVITER_IS_THERE = auto()
    IN_THE_WAY = auto()
    USER_HAS_INVITER = auto()
    USER_IS_BLOCKED = auto()
    USER_CREATE = auto()
    USER_IS_INVITER = auto()
    USER_IS_NEW = auto()
    USER_IS_NOT_INVITER = auto()
    USER_IS_NOT_BLOCKED = auto()
    USER_IS_NOT_NEW = auto()
    USER_IS_NOT_THERE = auto()
    USER_IS_THERE = auto()
    USER_DOSE_NOT_HAVE_REFERRAL_ID = auto()
    USER_HAS_REFERRAL_ID = auto()
    HERO_IS_NOT_NEW = auto()
    HERO_IS_NEW = auto()
    NEW_HERO_CREATE = auto()

    def __repr__(self):
        return self._name_
