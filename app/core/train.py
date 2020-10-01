# coding: utf8
from logging import getLogger

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
    def __init__(self, data):
        self.payload = {
            "states": dict(),
            "props": dict(),
            "queries": dict(),
            "data": data,
            "answers": list(),
            "__state__": {
                "exception": None,
                "statuses": []
            }
        }

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    @property
    def status(self):
        return self.payload["__state__"]["statuses"][-1]

    @status.setter
    def status(self, status):
        self.payload["__state__"]["statuses"].append(status)

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
