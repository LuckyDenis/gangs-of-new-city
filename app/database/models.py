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
    is_accepted = sa.Column(sa.Boolean(), default=False)
    is_developer = sa.Column(sa.Boolean(), default=False)
    is_tester = sa.Column(sa.Boolean(), default=False)
    is_blocked = sa.Column(sa.Boolean(), default=False)
    is_hint = sa.Column(sa.Boolean(), default=True)

    @classmethod
    async def get(cls, state):
        return await db.select(
            [cls.id,
             cls.language,
             cls.is_bot,
             cls.is_blocked,
             cls.is_developer,
             cls.is_accepted,
             cls.is_tester,
             cls.is_hint,
             Hero.nick.label("is_hero")]
        ).select_from(
            cls.outerjoin(
                Hero, cls.id == Hero.user
            )
        ).where(
            cls.id == state["id"]
        ).gino.one_or_none()

    @classmethod
    async def create(cls, state):
        await cls.insert().values(
            id=state["id"],
            is_bot=state["is_bot"],
            visited=state["visited"],
            registered=state["registered"],
            language=state["language"]
        ).gino.status()

    @classmethod
    async def is_accept_policy(cls, state):
        async with db.transaction():
            await cls.update.values(
                is_accepted=True
            ).where(
                cls.id == state["id"]
            ).gino.status()

    @classmethod
    async def is_not_accept_policy(cls, state):
        async with db.transaction():
            await cls.update.values(
                is_accepted=False
            ).where(
                cls.id == state["id"]
            ).gino.status()

    @classmethod
    async def time_visited_update(cls, state):
        async with db.transaction():
            await cls.update.values(
                visited=state["visited"]
            ).where(
                cls.id == state["id"]
            ).gino.status()

    @classmethod
    async def language_update(cls, state):
        async with db.transaction():
            await cls.update.values(
                language=state["language"]
            ).where(
                cls.id == state["id"]
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
    gang = sa.Column(
        sa.String(10), sa.ForeignKey(
            Gang.color, ondelete="CASCADE", onupdate="CASCADE"
        ), index=True
    )
    level = sa.Column(sa.Integer(), default=1, nullable=False)
    health = sa.Column(sa.Integer(), default=1, nullable=False)
    mana = sa.Column(sa.Integer(), default=1, nullable=False)
    stamina = sa.Column(sa.Integer(), default=1, nullable=False)
    max_health = sa.Column(sa.Integer(), default=1, nullable=False)
    max_mana = sa.Column(sa.Integer(), default=1, nullable=False)
    max_stamina = sa.Column(sa.Integer(), default=1, nullable=False)
    accuracy = sa.Column(sa.Integer(), default=1, nullable=False)
    strength = sa.Column(sa.Integer(), default=1, nullable=False)
    intellect = sa.Column(sa.Integer(), default=1, nullable=False)
    agility = sa.Column(sa.Integer(), default=1, nullable=False)

    @classmethod
    async def create(cls, states):
        await cls.insert().values(
            user=states["id"],
            nick=states["nick"],
            gang=states["gang"],
            level=states["level"],
            health=states["health"],
            mana=states["mana"],
            stamina=states["stamina"],
            max_health=states["max_health"],
            max_mana=states["max_mana"],
            max_stamina=states["max_stamina"],
            accuracy=states["accuracy"],
            intellect=states["intellect"],
            agility=states["agility"]
        ).gino.status()

    @classmethod
    async def get(cls, states):
        return await cls.query.where(
            cls.user == states["id"]
        ).gino.one_or_none()

    @classmethod
    async def get_by_nick(cls, states):
        return await db.select(
            [cls.nick]
        ).select_from(
            cls
        ).where(
            cls.nick == states["nick"]
        ).gino.one_or_none()
