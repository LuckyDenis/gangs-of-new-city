# coding: utf8

from datetime import datetime
from logging import getLogger
from pprint import pp

import uvloop

from app.core import stations as st
from app.core.statuses import Statuses as Code
from app.core.train import Train

logger = getLogger(__name__)


class BaseItinerary:
    def __init__(self, data):
        self.train = Train(data)
        self.data_has_required_keys()

    async def move(self):
        """
        Перемещаемся от станции к станции, пока не дойдем
        до последней или не получим сообщение
        `core.statuses.EMERGENCE_STOP`. Входе движения
        получаем, обрабатываем, сохраняем данные для ответа
        пользователю.
        :return: None
        """
        for station in self.stations():
            if self.train.status == Code.EMERGENCY_STOP:
                break
            await station(self.train).traveled()

    def data_has_required_keys(self):
        for key in self.required_keys():
            if not self.train.data.get(key, False):
                raise AttributeError(f'Key `{key}` is required')

    def get_answers(self):
        return self.train.answers

    def stations(self):
        """
        Возращает список классов порожденных от класса
        `core.stations.BaseSt`. Используется для сбора и
        обработки информации сообщения пользователя.
        Подробней о мотивации в модуле `core.stations`.
        :return: [BaseSt]
        """
        raise NotImplemented

    def required_keys(self):
        """
        Список ключей которые должные быть обезательно
        во входном словаре `data`.
        :return: [str, int]
        todo:
        Подумать о том, являются ли данные которые
        передаются в класс доверительными в плане
        типов, если нет то добавить валидацию.
        Например: check_data = [
            {"key": "id", "type": int},
            {"key": "datetime", "type": datetime}
        ] или https://pypi.org/project/schema/
        """
        raise NotImplemented


class NewUserItinerary(BaseItinerary):
    """
    :param data: {
        "id": user id,
        "language": database.fixture.Language,
        "datetime": datetime.datetime,
        "referral_link": referral link
    }
    """
    def required_keys(self):
        return ["id", "language", "datetime"]

    def stations(self):
        """
        Сначало создам пользователя, потом обработываем
        пригласившего.
        """
        return [
            st.GetUserSt,
            st.IsThereUserSt,
            st.CreatingUserSt,
            st.UserHasReferralIdSt,
            st.GetInviterSt,
            st.IsThereInviterSt,
            st.UserIsInviterSt,
            st.AddReferralDataSt
        ]


class NewHeroItinerary(BaseItinerary):
    def required_keys(self):
        return ["id"]

    def stations(self):
        return [
            st.GetUserSt,
            st.UserIsBlockedSt,

        ]


async def main():
    itinerary = NewUserItinerary({
        "id": 123456789,
        "language": "en",
        "datetime": datetime.now(),
        "referral_id": 123123123,
    })
    await itinerary.move()
    train = itinerary.train
    pp(train.payload)


if __name__ == "__main__":
    loop = uvloop.new_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
