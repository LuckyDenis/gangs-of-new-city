# coding: utf8

from logging import getLogger
from . import models as m

logger = getLogger(__name__)


class User:
    model = m.User
    skip_key = ["id"]

    @classmethod
    async def get(cls, query):
        # user = await m.User.get(props)
        return {}  # {'id': query['id']}

    @classmethod
    async def create(cls, query):
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
