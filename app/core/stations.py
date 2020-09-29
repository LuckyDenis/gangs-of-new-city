# coding: utf8
"""
Использования подходов маленьких классов
содержащих какую-то одну логику упрощает
поддержку и повторное использования кода.

Например для вывода данных информации о
состоянии кошелька персонажа используется
класс `GetWalletSt` и этот же класс можно
переиспользовать для операции купли/продажи.
Принцип SOLID.
"""

from logging import getLogger

import app.database as db
from .statuses import Statuses as Code

logger = getLogger(__name__)


class BaseSt:
    def __init__(self, train):
        self.train = train
        logger.debug(self.train)

    @property
    def status(self):
        return self.train.status

    @status.setter
    def status(self, status):
        self.train.status = status

    @property
    def exception(self):
        return self.train.exception

    @exception.setter
    def exception(self, err):
        self.train.exception = err

    @property
    def answers(self):
        return self.train.answers

    @answers.setter
    def answers(self, answer):
        self.train.answers = answer

    async def traveled(self):
        raise NotImplemented

    async def execution(self, storage_query, query_name):
        result = {}
        try:
            result = await storage_query(
                self.train.queries[query_name])
        except Exception as e:
            self.exception = e
            self.status = Code.DATABASE_ERROR
        return result


class GetUserSt(BaseSt):
    """
    Получаем пользоватя из базы, если пользователя нет -
    добавляем пустой словарь.

    Контракт:
    Для работы нужна информация по пути ['data']['id']
    Добавляет информацию о пользователе по ключу: ['state']['user'].
    """
    def query_data(self):
        query_name = "get_user"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.get

    async def traveled(self):
        user = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["user"] = user

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.GET_USER
        return self.train


class IsThereUserSt(BaseSt):
    """
    Проверка, что пользователя нет в базе.

    Контракт:
    Для проверки необходима информация по пути ['state']['user']
    Если пользователь обнаружен, добавляем ответ в список answers
    и уходим с маршрута.
    """
    async def add_out_answer(self):
        self.train.status = Code.USER_IS_THERE
        self.answers = "нашли пользователя"  # todo: данные из модуля `views`

    async def traveled(self) -> dict:
        states = self.train.states
        if states['user']:  # Пользователь существует
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.USER_IS_NOT_THERE
        return self.train


class CreatingUserSt(BaseSt):
    async def add_out_answer(self):
        self.status = Code.CREATED_USER
        self.train.answers = 'создали пользователя'   # todo: данные из модуля `views`

    def query_data(self):
        query_name = "create_user"
        self.train.queries[query_name] = {
            "id": self.train.data["id"],
            "language": self.train.data["language"],
            "visited": self.train.data["datetime"],
            "registered": self.train.data["datetime"],
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.User.create

    async def traveled(self) -> dict:
        user = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["user"] = user

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        await self.add_out_answer()
        return self.train


'''
class UserIsBlockedSt(BaseSt):
    async def add_out_answer(self):
        pass

    async def traveled(self) -> dict:
        user_state = self["user_state"]
        if user_state and user_state["is_blocked"]:
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP

        return self.train


class UserIsDeveloperSt(BaseSt):
    async def add_out_answer(self):
        pass

    async def traveled(self) -> dict:
        user_state = self["user_state"]
        if user_state and not user_state["is_developer"]:
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP

        return self.train


class UserIsTesterSt(BaseSt):
    async def traveled(self) -> dict:
        user_state = self["user_state"]
        if user_state and user_state["is_tester"]:
            self.status = Code.USER_IS_TESTER
        return self.train


class UserHasHeroSt(BaseSt):
    async def traveled(self) -> dict:
        user_state = self["user_state"]
        if user_state and user_state["has_hero"]:
            self.status = Code.USER_HAS_NOT_HERO
        return self.train


class UserHasBonusSt(BaseSt):
    async def add_answer(self):
        pass

    async def traveled(self) -> dict:
        pass
'''

