# coding: utf8
import os
import pytest
from app.configuration.settings import Setup


@pytest.fixture()
def message():
    class message:
        message_id = 123

        class chat:
            id = 123456789

    return message


@pytest.fixture()
async def on_process_message(*_, **__):
    pass


@pytest.fixture(scope="session")
def setup():
    root = os.path.dirname(__file__).split("/")
    root = root[:len(root) - 2] + ["helpers", "test.json"]
    PATH = "/".join(root)
    return Setup(PATH)
