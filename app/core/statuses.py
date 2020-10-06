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
    EMERGENCY_STOP = auto()
    IS_OK = auto()

    def __repr__(self):
        return self._name_
