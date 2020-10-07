# coding: utf8

from logging import getLogger

import sqlalchemy as sa
from gino import Gino
from . import fixture


logger = getLogger(__name__)

db = Gino()


class Language(db.Model):
    __tablename__ = "language"

    # ISO 639-2
    code = sa.Column(
        sa.String(2), primary_key=True, index=True)


class Gang(db.Model):
    __tablename__ = "gang"

    color = sa.Column(
        sa.String(10), primary_key=True, index=True)


class User(db.Model):
    __tablename__ = "user"

    id = sa.Column(
        sa.BigInteger(), primary_key=True, index=True)
    language = sa.Column(
        sa.String(2), sa.ForeignKey(
            Language.code,
            onupdate="CASCADE"),
        default=fixture.Languages.ENGLISH
    )
    visited = sa.Column(sa.DateTime())
    registered = sa.Column(sa.DateTime())
    is_bot = sa.Column(sa.Boolean(), default=False)
    is_permission = sa.Column(sa.Boolean(), default=False)
    is_developer = sa.Column(sa.Boolean(), default=False)
    is_tester = sa.Column(sa.Boolean(), default=False)
    is_blocked = sa.Column(sa.Boolean(), default=False)

    @classmethod
    async def get(cls, states):
        return await db.select(
            [cls.id,
             cls.language,
             cls.is_bot,
             cls.is_blocked,
             cls.is_developer,
             cls.is_permission,
             cls.is_tester,
             Hero.nick.label("is_hero")]
        ).select_from(
            cls.outerjoin(
                Hero, cls.id == Hero.user
            )
        ).where(
            cls.id == states["id"]
        ).gino.one_or_none()

    @classmethod
    async def create(cls, states):
        await cls.insert().values(
            id=states["id"],
            is_bot=states["is_bot"],
            visited=states["visited"],
            registered=states["registered"],
            language=states["language"]
        ).gino.status()


class Referral(db.Model):
    __tablename__ = "referral"

    invited = sa.Column(sa.BigInteger(), sa.ForeignKey(
        User.id, ondelete="CASCADE", onupdate="CASCADE"))
    inviter = sa.Column(sa.BigInteger(), sa.ForeignKey(
        User.id, ondelete="CASCADE", onupdate="CASCADE"
    ))
    is_play = sa.Column(sa.Boolean(), default=False)


class Hero(db.Model):
    __tablename__ = "hero"

    user = sa.Column(
        sa.BigInteger(), sa.ForeignKey(
            User.id, ondelete="CASCADE", onupdate="CASCADE"
        ), primary_key=True, index=True)
    nick = sa.Column(
        sa.String(20), unique=True, index=True)
