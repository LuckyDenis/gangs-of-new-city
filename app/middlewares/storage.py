# coding: utf8

from aiogram.dispatcher.middlewares import BaseMiddleware
from gino import create_engine
from app.database import db

__all__ = ["GinoMiddleware"]


class GinoMiddleware(BaseMiddleware):
    def __init__(self, setup):
        self.url = self.make_url(setup["connect"])

        self.min_size = setup["pool"]["min"]
        self.max_size = setup["pool"]["max"]
        self.engine = None
        super(GinoMiddleware, self).__init__()

    @staticmethod
    def make_url(connect):
        return (f'{connect["engine"]}://{connect["login"]}:'
                f'{connect["password"]}@{connect["host"]}/{connect["name"]}')

    async def on_process_message(self, message, data: dict):
        data['db'] = await self.database()

    async def database(self):
        if not self.engine:
            self.engine = await create_engine(
                self.url,
                min_size=self.min_size,
                max_size=self.max_size
            )
        db.bind = self.engine
        return db

    async def shutdown(self):
        if self.engine:
            engine, db.bind = db.bind, None
            await engine.close()
        else:
            db.bind = None
