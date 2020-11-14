# coding: utf8
import pytest
from app.core.stations import BaseSt
from app.views import answers as an

EXCEPTION_ANSWER = {"test": "foo"}


class FooSt(BaseSt):
    @classmethod
    async def _traveled(cls, train):
        return True


class ErrorSt(BaseSt):
    @classmethod
    def add_exception_answer(cls, train):
        train.answers = EXCEPTION_ANSWER

    @classmethod
    async def _traveled(cls, train):
        raise KeyError()


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__add_exception_answer(train, monkeypatch):
    def get(*_):
        return EXCEPTION_ANSWER

    monkeypatch.setattr(an.SystemException, "get", get)
    ANSWERS = ["string 1", "string 2"]
    for answer in ANSWERS:
        train.answers = answer

    BaseSt.add_exception_answer(train)
    assert len(train.answers) == 1
    assert train.answers == [EXCEPTION_ANSWER]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__execution(train, data: dict):
    QUERY_NAME = "get_test"

    class DBTable:
        @classmethod
        async def get(cls, query):
            return query

    train.queries[QUERY_NAME] = data
    result = await BaseSt.execution(
        train, DBTable.get, QUERY_NAME
    )
    assert isinstance(result, dict)
    assert result == data


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__execution_with_error(train, data: dict):
    QUERY_NAME = "get_test"

    class DBTable:
        @classmethod
        async def get(cls, query):
            raise IOError()

    train.queries[QUERY_NAME] = data
    result = await BaseSt.execution(
        train, DBTable.get, QUERY_NAME
    )
    assert isinstance(result, dict)
    assert train.exception is not None


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__inside_traveled_not_realize(train):
    with pytest.raises(NotImplementedError):
        await BaseSt._traveled(train)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_is_ok(train):
    is_ok = await FooSt.traveled(train)
    assert is_ok is True


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_is_not_ok(train):
    is_ok = await ErrorSt.traveled(train)
    assert is_ok is False
    assert train.answers == [EXCEPTION_ANSWER]
