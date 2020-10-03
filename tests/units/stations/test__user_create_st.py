# coding: utf8
import pytest

from app.core.stations import UserCreateSt
from app.core.statuses import Statuses as Code
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error
from app.database.queries import User


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(data, train, monkeypatch):
    monkeypatch.setattr(UserCreateSt, "execution", fake_execution)
    await UserCreateSt(train).traveled()

    assert train.status == Code.USER_CREATE
    assert train.states["user"]["id"] == data["id"]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(UserCreateSt, "execution", fake_execution_with_error)
    await UserCreateSt(train).traveled()

    assert train.status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = UserCreateSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("id")
    assert query_data.get("language")
    assert query_data.get("visited")
    assert query_data.get("registered")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = UserCreateSt(train).storage_query()
    bound_method = User.create
    assert storage_query == bound_method


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answers():
    """
    todo:
    добавить после того как будет
    реализован пакет `views.answers`
    """
    pass
