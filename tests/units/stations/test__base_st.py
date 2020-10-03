# coding: utf8
import pytest
from app.core.stations import BaseSt
from app.core.train import Train
from app.core.statuses import Statuses as Code


@pytest.fixture()
def base_st(data):
    return BaseSt(Train(data))


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__push_status(base_st: BaseSt):
    STATUSES = [
        Code.IN_THE_WAY,
        Code.FINISHED
    ]
    for status in STATUSES:
        base_st.status = status
    assert base_st.train["__state__"]["statuses"] == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
def test__get_status(base_st: BaseSt):
    base_st.status = Code.EMERGENCY_STOP
    assert base_st.status is Code.EMERGENCY_STOP


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
    CORRECT_STATUSES = [Code.DATABASE_ERROR]

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

    statuses = base_st.train["__state__"]["statuses"]
    assert statuses == CORRECT_STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_not_realize(train):
    with pytest.raises(NotImplementedError):
        await BaseSt(train).traveled()
