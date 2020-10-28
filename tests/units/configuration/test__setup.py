# coding: utf8
import os
import json
import pytest
from app.configuration.settings import Setup


root = os.path.dirname(__file__).split("/")
root = root[:len(root) - 2] + ["helpers", "test.json"]
PATH = "/".join(root)


@pytest.fixture(scope="module")
def setup():
    return Setup(PATH)


@pytest.mark.unit
@pytest.mark.settings
@pytest.mark.parametrize("attr", [
    "_data", "_path",
    "_read", "logging",
    "database", "bot",
    "i18n"
])
def test__setup_attr(setup, attr):
    assert hasattr(setup, attr)


@pytest.mark.unit
@pytest.mark.settings
def test__setup_must_once():
    first = Setup(PATH)
    second = Setup(PATH)
    assert id(first) == id(second)


@pytest.mark.unit
@pytest.mark.settings
def test__open_config(setup):
    with open(PATH, mode="r") as jf:
        config = json.load(jf)
    assert setup._data.to_dict() == config


@pytest.mark.unit
@pytest.mark.settings
def test__get_logging(setup):
    assert isinstance(setup.logging, dict)


@pytest.mark.unit
@pytest.mark.settings
def test__get_database(setup):
    assert isinstance(setup.database, dict)


@pytest.mark.unit
@pytest.mark.settings
def test__get_bot(setup):
    assert isinstance(setup.bot, dict)


@pytest.mark.unit
@pytest.mark.settings
def test__get_i18n(setup):
    assert isinstance(setup.i18n, dict)
