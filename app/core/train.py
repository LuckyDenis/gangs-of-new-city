# coding: utf8
from logging import getLogger
from collections import OrderedDict


logger = getLogger(__name__)


class Train:
    """
    Данный класс служит оберткой для данных которые находятся
    в зоне `core`. Используется классами порожденными классом
    `core.dispatcher.BaseItinerary`.

    :param data (dict) содержит базовую информацию от запроса
    из модуля `controllers.handlers`. Используется словарь, как
    стандартный тип python, для снижения связанностей модулей
    системы.
    Пример: { 'timestamp': 123456789, 'user_id': 123456789 }

    payload (dict) непосредственный контейнер для хранения данных
    """

    __slots__ = ["payload"]

    def __init__(self, data):
        self.payload = {
            "states": dict(),
            "props": dict(),
            "queries": dict(),
            "data": data,
            "answers": list(),
            "__state__": {
                "exception": dict(),
                "progress": OrderedDict(),
            }
        }

    @property
    def progress(self):
        return self.payload["__state__"]["progress"]

    @progress.setter
    def progress(self, station):
        station_name = station["name"]
        status = station["status"]
        self.payload["__state__"]["progress"][station_name] = status

    @property
    def exception(self):
        return self.payload["__state__"]["exception"]

    @exception.setter
    def exception(self, err):
        self.payload["__state__"]["exception"] = err

    @property
    def answers(self):
        return self.payload["answers"]

    @answers.setter
    def answers(self, answer):
        self.payload["answers"].append(answer)

    @answers.deleter
    def answers(self):
        self.payload["answers"].clear()

    @property
    def data(self):
        return self.payload["data"]

    @property
    def states(self):
        return self.payload["states"]

    @property
    def props(self):
        return self.payload["props"]

    @property
    def queries(self):
        return self.payload["queries"]
