# coding: utf8

from logging import getLogger

from . import models as m
from . import default as d

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
        query["language"] = m.fixture.Languages.for_user(query["language"])
        await cls.model.create(query)
        return {"id": query["id"], "language": query["language"]}

    @classmethod
    async def is_agree_policy(cls, query):
        await cls.model.is_agree_policy(query)

    @classmethod
    async def is_not_agree_policy(cls, query):
        await cls.model.is_not_agree_policy(query)

    @classmethod
    async def user_time_visited_update(cls, query):
        await cls.model.user_time_visited_update(query)


class Hero:
    model = m.Hero
    skip_keys = ["id"]

    @classmethod
    async def get(cls, query):
        state = {
            "id": query["id"]
        }
        result = await cls.model.get(state)
        return {**result} if result else {}

    @classmethod
    async def create(cls, query):
        states = {
            "id": query["id"],
            "nick": query["hero_nick"],
            "gang": d.HERO.GANG,
            "level": d.HERO.LEVEL,
            "health": d.HERO.HEALTH,
            "mana": d.HERO.MANA,
            "stamina": d.HERO.STAMINA,
            "max_health": d.HERO.MAX_HEALTH,
            "max_mana": d.HERO.MAX_MANA,
            "max_stamina": d.HERO.MAX_STAMINA,
            "accuracy": d.HERO.ACCURACY,
            "strength": d.HERO.STRENGTH,
            "intellect": d.HERO.INTELLECT,
            "agility": d.HERO.AGILITY
        }
        await cls.model.create(states)
        return query

    @classmethod
    async def get_by_nick(cls, query):
        state = {
            "nick": query["hero_nick"]
        }
        result = await cls.model.get_by_nick(state)
        return {**result} if result else {}


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
