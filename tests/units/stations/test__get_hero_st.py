# coding: utf8
import pytest

from app.core.stations import GetHeroSt
from app.core.statuses import Statuses as Code
from app.database.queries import Hero
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error


HERO_KEY = "hero"


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train, monkeypatch):
    monkeypatch.setattr(GetHeroSt, "execution", fake_execution)
    status = await GetHeroSt.traveled(train)
    assert status == Code.IS_OK
    assert isinstance(train.states[HERO_KEY], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(GetHeroSt, "execution", fake_execution_with_error)
    status = await GetHeroSt.traveled(train)
    assert status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = GetHeroSt.query_data(train)
    query_data = train.queries[query_name]
    assert query_data.get("id")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query():
    storage_query = GetHeroSt.storage_query()
    bound_method = Hero.get
    assert storage_query == bound_method
