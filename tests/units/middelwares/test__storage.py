# coding: utf8
import pytest
from app.middlewares import storage
from app.middlewares.storage import GinoMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from gino import Gino


async def create_engine(*_, **__):
    class engine:
        @staticmethod
        async def close():
            return None

    return engine


@pytest.fixture(scope="module")
def _gino_mdw(setup):
    return GinoMiddleware(setup.database)


@pytest.fixture()
def gino_mdw(_gino_mdw, monkeypatch):
    monkeypatch.setattr(storage, "create_engine", create_engine)
    return _gino_mdw


@pytest.mark.unit
def test__is_subclass():
    assert issubclass(GinoMiddleware, BaseMiddleware)


@pytest.mark.unit
@pytest.mark.parametrize("attr", [
    "url", "min_size", "max_size",
    "engine", "make_url",
    "on_process_message",
    "database", "shutdown"
])
def test__storage_attr(gino_mdw, attr):
    assert hasattr(gino_mdw, attr)


@pytest.mark.unit
def test__make_url(setup, gino_mdw):
    connect = setup.database["connect"]
    CORRECT_URL = (f'{connect["engine"]}://{connect["login"]}:'
                   f'{connect["password"]}@{connect["host"]}/'
                   f'{connect["name"]}')

    assert gino_mdw.make_url(connect) == CORRECT_URL


@pytest.mark.unit
async def test__database(gino_mdw):
    db = await gino_mdw.database()
    isinstance(db, Gino)


@pytest.mark.unit
async def test__shutdown_with_engine(gino_mdw):
    await gino_mdw.database()
    await gino_mdw.shutdown()
    assert gino_mdw.engine is None


@pytest.mark.unit
async def test__shutdown_with_not_engine(gino_mdw):
    await gino_mdw.shutdown()
    assert gino_mdw.engine is None


@pytest.mark.unit
async def test__on_process_message(gino_mdw, message):
    data = {}
    await gino_mdw.on_process_message(message, data)
    db = data.get("db")
    assert isinstance(db, Gino)
