# coding: utf8

from logging import getLogger

import sqlalchemy as sa
from gino import Gino

logger = getLogger(__name__)

db = Gino()


class OPTIONS:
    CASCADE = "CASCADE"


class DEFAULT:
    LANG = "en"


class UserLanguage(db.Model):
    __tablename__ = "user_language"

    # ISO 639-2
    code = sa.Column(sa.String(2), primary_key=True, index=True)


class User(db.Model):
    __tablename__ = "user"

    id = sa.Column(
        sa.BigInteger(), primary_key=True, index=True)
    language = sa.Column(
        sa.String(2), sa.ForeignKey(
            UserLanguage.code,
            onupdate=OPTIONS.CASCADE),
        default=DEFAULT.LANG
    )
    visited = sa.Column(sa.DateTime())
    registered = sa.Column(sa.DateTime())
    is_developer = sa.Column(sa.Boolean(), default=False)
    is_tester = sa.Column(sa.Boolean(), default=False)
    is_blocked = sa.Column(sa.Boolean(), default=False)

    # @db.bake
    def _get(cls):
        return cls.model.query.where(
            cls.model.id == db.bindparam("uid"))

    @classmethod
    async def get(cls, props: dict):
        return await cls._get.one_or_none(uid=props["uid"])

