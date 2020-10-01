# coding: utf8
import pytest

from app.core.stations import GetUserSt
from app.core.statuses import Statuses as Code
from app.database.queries import User
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train, monkeypatch):
    monkeypatch.setattr(GetUserSt, "execution", fake_execution)
    await GetUserSt(train).traveled()
    assert train.status == Code.GET_USER
    assert isinstance(train.states['user'], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = GetUserSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("id", False)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = GetUserSt(train).storage_query()
    bound_method = User.get
    assert storage_query == bound_method


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(GetUserSt, "execution", fake_execution_with_error)
    await GetUserSt(train).traveled()
    assert train.status == Code.EMERGENCY_STOP
