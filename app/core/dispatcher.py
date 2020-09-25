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


class NewUserTrain(BaseTrain):
    def __init__(self, data):
        self.train = {
            "stations": {
                "get_user": st.GetUserSt,
                "user_is_find": st.DataIsFound
            },
            "__state__": self.__state__,
            "data": data
        }

