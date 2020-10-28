# coding: utf8
import pytest
from app.core.stations import BaseSt
from app.core.train import Train
from app.views import answers as an

EXCEPTION_ANSWER = {"test": "foo"}


class FooSt(BaseSt):
    async def _traveled(self):
        return True


class ErrorSt(BaseSt):
    async def add_exception_answer(self):
        self.answers = EXCEPTION_ANSWER

    async def _traveled(self):
        raise KeyError()


@pytest.fixture()
def base_st(data):
    return BaseSt(Train(data))


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__push_answers(base_st: BaseSt):
    ANSWERS = ["string 1", "string 2"]
    for answer in ANSWERS:
        base_st.answers = answer

    assert len(base_st.answers) == len(ANSWERS)
    assert base_st.answers == ANSWERS


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__get_answers(base_st: BaseSt):
    answer = "string 1"
    base_st.answers = answer
    assert base_st.answers[-1] == answer


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__del_answers(base_st: BaseSt):
    ANSWERS = ["string 1", "string 2"]
    for answer in ANSWERS:
        base_st.answers = answer

    del base_st.answers
    assert len(base_st.answers) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_exception_answer(base_st: BaseSt, monkeypatch):
    async def get(*_):
        return EXCEPTION_ANSWER

    monkeypatch.setattr(an.SystemException, "get", get)
    ANSWERS = ["string 1", "string 2"]
    for answer in ANSWERS:
        base_st.answers = answer

    await base_st.add_exception_answer()
    assert len(base_st.answers) == 1
    assert base_st.answers == [EXCEPTION_ANSWER]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__execution(base_st: BaseSt, data: dict):
    QUERY_NAME = "get_test"

    class DBTable:
        @classmethod
        async def get(cls, query):
            return query

    base_st.train.queries[QUERY_NAME] = data
    result = await base_st.execution(
        DBTable.get, QUERY_NAME
    )
    assert isinstance(result, dict)
    assert result == data


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__execution_with_error(base_st: BaseSt, data: dict):
    QUERY_NAME = "get_test"

    class DBTable:
        @classmethod
        async def get(cls, query):
            raise IOError()

    base_st.train.queries[QUERY_NAME] = data
    result = await base_st.execution(
        DBTable.get, QUERY_NAME
    )
    assert isinstance(result, dict)
    assert base_st.exception is not None


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__inside_traveled_not_realize(train):
    with pytest.raises(NotImplementedError):
        await BaseSt(train)._traveled()


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_is_ok(train):
    is_ok = await FooSt(train).traveled()
    assert is_ok is True


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_is_not_ok(train):
    error_st = ErrorSt(train)
    is_ok = await error_st.traveled()
    assert is_ok is False
    assert error_st.answers == [EXCEPTION_ANSWER]
