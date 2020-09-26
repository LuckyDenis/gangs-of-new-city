# coding: utf8

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from gino import create_engine
from app.database import db
from sqlalchemy import create_engine

__all__ = ["GinoMiddleware"]


class GinoMiddleware(BaseMiddleware):
    def __init__(self):
        self._dns = None
        self._min_size = 5
        self._max_size = 10
        self._engine = None
        super(GinoMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['db'] = await self.database()

    async def init_gino(self):
        await self.database()

    async def database(self):
        if not self._engine:
            self._engine = await create_engine(
                self._dns,
                min_size=self._min_size,
                max_size=self._max_size
            )
        db.bind = self._engine
        return db

    async def shutdown(self):
        if self._engine:
            engine, db.bind = db.bind, None
            await engine.close()
        else:
            db.bind = None
