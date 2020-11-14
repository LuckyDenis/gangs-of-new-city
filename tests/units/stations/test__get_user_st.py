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
    status = await GetUserSt.traveled(train)
    assert status == Code.IS_OK
    assert isinstance(train.states['user'], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(GetUserSt, "execution", fake_execution_with_error)
    status = await GetUserSt.traveled(train)
    assert status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = GetUserSt.query_data(train)
    query_data = train.queries[query_name]
    assert query_data.get("id")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query():
    storage_query = GetUserSt.storage_query()
    bound_method = User.get
    assert storage_query == bound_method
