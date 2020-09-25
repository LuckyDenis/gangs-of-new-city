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
    Добавляет информацию о пользователе по ключу: ['state'].
    """
    async def get_user(self) -> None:
        state = {}
        try:
            state = await db.User.get(props=self['props'])
        except PostgresConnectionError as e:
            self.error = e
            self.status = Code.DATABASE_ERROR
        self["state"] = state

    def add_props(self):
        self["props"] = {
            "id": self["data"]["id"]
        }

    async def traveled(self) -> dict:
        self.add_props()
        await self.get_user()
        return self.train


class DataIsFound(BaseSt):
    """
    Проверка, что данные найден в базе.

    Контракт:
    Для проверки необходима информация по пути ['state']
    Если данные не обнаружен, меняет статус.
    """
    async def traveled(self) -> dict:
        state = self["state"]
        if state is {}:
            self.status = Code.DATA_IS_NOT_FOUND

        return self.train


class CreateUserSt(BaseSt):
    async def create_user(self):
        pass

    def add_props(self):
        self["props"] = {
            "id": self["data"]["id"],
            "language": self["data"]["language"],
            "visited": self["data"]["datetime"],
            "registered": self["data"]["datetime"]
        }

    async def traveled(self) -> dict:
        if self.status is not Code.DATA_IS_NOT_FOUND:
            return self.train

        self.add_props()
        await self.create_user()

        if self.status is not Code.DATABASE_ERROR:
            self.status = Code.CREATED_USER

        return self.train

