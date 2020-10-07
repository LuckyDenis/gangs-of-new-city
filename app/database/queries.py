# coding: utf8

from logging import getLogger

from . import models as m

logger = getLogger(__name__)


class User:
    model = m.User
    skip_key = ["id"]

    @classmethod
    async def get(cls, query):
        """
        :param query: {
            "id": user id
        }
        :return: {
            "id": user id,
            "language": database.fixture.Language
            "is_developer": bool,
            "is_tester": bool,
            "is_blocked": bool
        } or {}
        """
        result = await cls.model.get(query)
        return {**result} if result else {}

    @classmethod
    async def create(cls, query):
        """
        :param query: {
            "id": user id,
            "language": database.fixture.Language
            "visited": datetime.datetime
            "registered": datetime.datetime,
            "is_bot": bool
        }
        :return: {
            "id": user id,
            "language" database.fixture.Language
        }
        """
        await cls.model.create(query)
        return {"id": query["id"], "language": query["language"]}

    @classmethod
    async def change(cls, query):
        pass


class Hero:
    model = None
    skip_keys = ["id"]

    @classmethod
    async def get(cls, query):
        return {}

    @classmethod
    async def create(cls, query):
        return query

    @classmethod
    async def get_by_nick(cls, query):
        return query


class Referral:
    model = None
    skip_keys = ["id"]

    @classmethod
    async def create(cls, query):
        return query

    @classmethod
    async def get(cls, query):
        return {"id": 123123123}


class Wallet:
    model = None
    skip_keys = ["id"]

    @classmethod
    async def get(cls, query):
        return query
