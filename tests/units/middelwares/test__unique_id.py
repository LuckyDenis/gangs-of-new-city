# coding: utf8
import pytest
from app.middlewares.unique_id import UniqueIdMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware


@pytest.mark.unit
def test__is_subclass():
    assert issubclass(UniqueIdMiddleware, BaseMiddleware)


@pytest.mark.unit
def test__make(message):
    UNIQUE_ID = f"{message.chat.id}-{message.message_id}"

    unique_id_mdw = UniqueIdMiddleware()
    unique_id = unique_id_mdw.make(message)
    assert unique_id == UNIQUE_ID


@pytest.mark.unit
async def test__on_process_message(message):
    data = {}
    unique_id_mdw = UniqueIdMiddleware()
    await unique_id_mdw.on_process_message(message, data)
    assert data.get("unique_id")
