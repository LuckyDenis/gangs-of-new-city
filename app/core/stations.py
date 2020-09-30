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
    Обязательные данные: ['data']['id']
    Добавленные данные: ['states']['user']
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

    Если пользователь обнаружен, добавляем ответ в список answers
    и уходим с маршрута.

    Контракт:
    Обязательные данные: ['state']['user']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        self.train.status = Code.USER_IS_THERE
        self.answers = "нашли пользователя"  # todo: данные из модуля `views`

    async def traveled(self) -> dict:
        user = self.train.states['user']
        if user:  # Пользователь существует
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.USER_IS_NOT_THERE
        return self.train


class CreatingUserSt(BaseSt):
    """
    Создаем нового пользователя.

    Контракт:
    Обязательные данные:
        ['data']['id']
        ['data']['language']
        ['data']['datetime']
    Добавленные данные: ['states']['user']
    """
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


class UserHasReferralIdSt(BaseSt):
    """
    Проверка наличия пригласившиего пользователя.
    Если такого пользователя нет, то дальше
    идти нет смысла. Для отсутсвующего пользователя
    передовать аргумент None.

    Контракт:
    Обезателные данные: ['data']['referral_id']
    Дабавленные данные: None
    """
    async def traveled(self):
        referral_id = self.train.data["referral_id"]
        if not referral_id:
            self.status = Code.USER_NOT_REFERRAL_ID
            self.status = Code.EMERGENCY_STOP
            return self.train
        return self.train


class GetInviterSt(BaseSt):
    """
    Берем пригласившего пользователя из базыданных.
    Делаем это для того, что бы убедиться, что пригла
    сивший пользователь существует.

    Контракт:
    Обезательные данные: ['data']['referral_id']
    Добавленные данные: ['states']['inviter']
    """
    def query_data(self):
        query_name = "get_inviter"
        self.train.queries[query_name] = {
            "referral_id": self.train.data["referral_id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Referral.get

    async def traveled(self):
        inviter = await self.execution(
            self.storage_query(), self.query_data())
        self.train.states["inviter"] = inviter

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.GET_USER
        return self.train


class IsThereInviterSt(BaseSt):
    """
    Проверяем что нашли приглашающего в налей базе
    данных.

    Контракт:
    Обезательные данные: ['states']['inviter']
    Добавленные данные: None
    """
    async def traveled(self):
        inviter = self.train.states["inviter"]
        if not inviter:
            self.status = Code.INVITER_IS_NOT_THERE
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.INVITER_IS_THERE
        return self.train


class UserIsInviterSt(BaseSt):
    """
    Пользователь не может сам себя пригласить.

    Контракт:
    Обезательные данные:
        ['states']['user']
        ['states']['inviter']
    Добавленные данные: None
    todo:
    Подумать, может ли возникнуть така ситуация.
    """
    async def traveled(self):
        user = self.train.states['user']
        inviter = self.train.states['inviter']
        if user["id"] == inviter["id"]:
            self.status = Code.USER_IS_INVITER
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.USER_IS_NOT_INVITER
        return self.train


class AddReferralDataSt(BaseSt):
    """
    Добавляем информацию для будущего начисления бонуса.

    Контракт:
    Обезаетельные данные:
        ['data']['id']
        ['states']['inviter']['id']
    Добавленные данные: ['answers']['answer']
    """
    async def add_out_answers(self):
        self.status = Code.ADD_REFERRAL_DATA
        self.train.answers = "сообщаем что дан боннус"

    def query_data(self):
        query_name = "add_referral_data"
        self.train.queries[query_name] = {
            'invited': self.train.data["id"],
            'inviter': self.train.states["inviter"]["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Referral.create

    async def traveled(self):
        await self.execution(
            self.storage_query(), self.query_data()
        )

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        await self.add_out_answers()
        return self.train


class UserIsBlockedSt(BaseSt):
    """
    Проверяем права на доступ к приложению.

    Контракт:
    Обязательные данные: ['states']['user']['is_blocked']
    Добавленные данные: ['answers']['answer'] или None
    """
    async def add_out_answer(self):
        self.status = Code.USER_IS_BLOCKED
        self.answers = "Пользователь заблокирован"

    async def traveled(self) -> dict:
        user = self.train.status["user"]
        if user and user["is_blocked"]:
            await self.add_out_answer()
            self.status = Code.EMERGENCY_STOP

        return self.train


class GetHeroSt(BaseSt):
    def query_name(self):
        query_name = "get_hero"
        self.train.queries[query_name] = {
            "id": self.train.data["id"]
        }
        return query_name

    @staticmethod
    def storage_query():
        return db.Hero.get

    async def traveled(self):
        hero = await self.execution(
            self.storage_query(), self.query_name()
        )
        self.train.states["hero"] = hero

        if self.status is Code.DATABASE_ERROR:
            self.status = Code.EMERGENCY_STOP
            return self.train

        self.status = Code.GET_HERO
        return self.train


'''
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

