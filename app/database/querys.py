# coding: utf8

from logging import getLogger
from . import models as m


logger = getLogger(__name__)


class User:
    model = m.User
    skip_key = ["id"]

    @classmethod
    async def get(cls, props: dict) -> dict:
        user = await m.User.get(props)
        return user.__values__
