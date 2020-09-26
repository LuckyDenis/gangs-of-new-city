# coding: utf8

import app.database as db
from logging import getLogger
from .statuses import Statuses as Code
from asyncpg import PostgresConnectionError

logger = getLogger(__name__)


class BaseSt:
    """
    :param: __state__: словарь, в котором храниться информация,
    о состоянии обработки запроса.
    """
    def __init__(self, train: dict):
        self.train = train
        logger.debug(self.train)

    def __getitem__(self, key: [int, str]) -> [any, bool]:
        return self.train.get(key, False)

    def __setitem__(self, key: [int, str], value: any):
        self.train[key] = value

    @property
    def status(self) -> str:
        return self["__state__"]["status"]

    @status.setter
    def status(self, code: str) -> None:
        self["__state__"]["status"] = code

    @property
    def error(self) -> str:
        return self["__state__"]["error"]

    @error.setter
    def error(self, e: Exception) -> None:
        self["__state__"]["error"] = e

    async def traveled(self) -> dict:
        raise NotImplemented


class GetUserSt(BaseSt):
    """
    Получаем пользоватя из базы, если пользователя нет -
    добавляем пустой словарь.

    Контракт:
    Для работы нужна информация по пути ['data']['id']
    Добавляет информацию о пользователе по ключу: ['user_state'].
    """
    async def get_user(self) -> None:
        user_state = {}
        try:
            user_state = await db.User.get(props=self['user_props'])
        except PostgresConnectionError as e:
            self.error = e
            self.status = Code.DATABASE_ERROR
        self["user_state"] = user_state

    def add_props(self):
        self["user_props"] = {
            "id": self["data"]["id"]
        }

    async def traveled(self) -> dict:
        self.add_props()
        await self.get_user()

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP

        return self.train


class IsThereUserSt(BaseSt):
    """
    Проверка, что пользователя нет в базе.

    Контракт:
    Для проверки необходима информация по пути ['user_state']
    Если пользователь не обнаружен, добавляем ответ в спиоск views
    и уходим с маршрута.
    """
    async def add_out_answer(self):
        pass

    async def traveled(self) -> dict:
        user_state = self["user_state"]
        if user_state:  # Пользователь существует
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP

        return self.train


class CreatingUserSt(BaseSt):
    async def add_out_answer(self):
        pass

    async def create_user(self):
        pass

    def add_props(self):
        self["props"] = {
            "id": self["data"]["id"],
            "language": self["data"]["language"],
            "visited": self["data"]["datetime"],
            "registered": self["data"]["datetime"],
        }

    async def traveled(self) -> dict:
        self.add_props()
        await self.create_user()

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        await self.add_out_answer()
        return self.train


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
