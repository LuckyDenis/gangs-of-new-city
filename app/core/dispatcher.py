# coding: utf8

from logging import getLogger
from app.core import stations as st
from app.core.statuses import Statuses as Code
from app.core.train import Train

from pprint import pp
import uvloop
from datetime import datetime
logger = getLogger(__name__)


class BaseItinerary:
    def __init__(self, data):
        self.train = Train(data)
        self.data_has_required_keys()

    async def move(self):
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
        raise NotImplemented

    def required_keys(self):
        raise NotImplemented


class NewUserItinerary(BaseItinerary):
    def required_keys(self):
        return ["id", "language", "datetime"]

    def stations(self):
        return [
            st.GetUserSt,
            st.IsThereUserSt,
            st.CreatingUserSt
        ]


async def main():
    itinerary = NewUserItinerary({
        "id": 123456789,
        "language": "en",
        "datetime": datetime.now(),
        "referral_link": "123123123",

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
