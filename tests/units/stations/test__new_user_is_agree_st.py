# coding: utf8
import pytest

from app.core.stations import UserIsAcceptSt
from app.database.fixture import Languages
from app.core.statuses import Statuses as Code
from app.database.queries import User
from tests.helpers.fake_executions import fake_execution_with_error
from tests.helpers.fake_executions import fake_execution_empty


@pytest.fixture()
def up_train(train):
    train.states["user"] = {"language": Languages.RUSSIAN}
    return train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(up_train, monkeypatch):
    monkeypatch.setattr(UserIsAcceptSt, "execution", fake_execution_empty)
    status = await UserIsAcceptSt.traveled(up_train)
    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(up_train, monkeypatch):
    monkeypatch.setattr(
        UserIsAcceptSt, "execution", fake_execution_with_error)
    status = await UserIsAcceptSt.traveled(up_train)

    assert status is Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(up_train):
    query_name = UserIsAcceptSt.query_data(up_train)
    query_data = up_train.queries[query_name]
    assert query_data.get("id")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query():
    storage_query = UserIsAcceptSt.storage_query()
    bound_method = User.is_accept_policy
    assert storage_query == bound_method
