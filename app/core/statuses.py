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
    # todo: Отсортировать в алфавитном порядке

    FINISHED = auto()
    IN_THE_WAY = auto()
    CREATED_USER = auto()
    GET_USER = auto()
    USER_IS_THERE = auto()
    USER_IS_NOT_THERE = auto()
    HAS_OUT_ANSWER = auto()
    USER_IS_BLOCKED = auto()
    GET_HERO = auto()
    GET_INVITER = auto()
    USER_NOT_REFERRAL_ID = auto()
    USER_HAS_INVITER = auto()
    INVITER_IS_THERE = auto()
    INVITER_IS_NOT_THERE = auto()
    USER_IS_INVITER = auto()
    USER_IS_NOT_INVITER = auto()
    ADD_REFERRAL_DATA = auto()
    EMERGENCY_STOP = auto()
    DATABASE_ERROR = auto()

    def __repr__(self):
        return self._name_
