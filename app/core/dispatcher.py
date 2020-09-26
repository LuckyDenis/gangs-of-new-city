# coding: utf8

from logging import getLogger
from . import stations as st
from .statuses import Statuses as Code

logger = getLogger(__name__)


class BaseTrain:
    @staticmethod
    def __state__() -> dict:
        return {
            "status": Code.IN_THE_WAY,
            "error": None
        }

    async def move(self):
        pass

    def get_result(self):
        pass


class NewUserTrain(BaseTrain):
    def __init__(self, data):
        self.train = {
            "stations": [
                st.GetUserSt,
                st.IsThereUserSt,
                st.CreatingUserSt,
            ],
            "__state__": self.__state__,
            "data": data,
            "answers": []
        }
