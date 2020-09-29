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
        return {}  # {'id': query['id']}

    @classmethod
    async def create(cls, query):
        """
        :param query: {
            "id": user id,
            "language": database.fixture.Language
            "visited": datetime.datetime
            "registered": datetime.datetime
        }
        :return: {
            "id": user id,
            "language" database.fixture.Language
        }
        """
        return query

    @classmethod
    async def change(cls, query):
        pass


class Referral:
    model = None
    skip_keys = ["id"]

    @classmethod
    async def create(cls, query):
        return query
