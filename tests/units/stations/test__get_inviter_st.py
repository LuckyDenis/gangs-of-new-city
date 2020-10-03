# coding: utf8
import pytest

from app.core.stations import GetInviterSt
from app.core.statuses import Statuses as Code
from app.database.queries import User
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error


REFERRAL_ID = 123456789
KEY_REFERRAL_ID = "referral_id"


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train, monkeypatch):
    monkeypatch.setattr(GetInviterSt, "execution", fake_execution)
    train.data[KEY_REFERRAL_ID] = REFERRAL_ID
    await GetInviterSt(train).traveled()

    assert train.status == Code.GET_INVITER
    assert isinstance(train.states['inviter'], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(GetInviterSt, "execution", fake_execution_with_error)
    await GetInviterSt(train).traveled()

    assert train.status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = GetInviterSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("id")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = GetInviterSt(train).storage_query()
    bound_method = User.get
    assert storage_query == bound_method
