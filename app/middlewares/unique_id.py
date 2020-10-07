# coding: utf8

from aiogram.dispatcher.middlewares import BaseMiddleware


__all__ = ["UniqueIdMiddleware"]


class UniqueIdMiddleware(BaseMiddleware):
    def __init__(self):
        super(UniqueIdMiddleware, self).__init__()

    async def on_process_message(self, message, data: dict):
        data['unique_id'] = self.make(message)

    @staticmethod
    def make(message):
        return f'{message.chat.id}-{message.message_id}'
