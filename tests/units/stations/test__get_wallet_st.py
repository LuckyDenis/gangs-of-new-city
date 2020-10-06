# coding: utf8
import pytest

from app.core.stations import GetWalletSt
from app.core.statuses import Statuses as Code
from app.database.queries import Wallet
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error


WALLET_KEY = "wallet"


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train, monkeypatch):
    monkeypatch.setattr(GetWalletSt, "execution", fake_execution)
    status = await GetWalletSt(train).traveled()
    assert status == Code.IS_OK
    assert isinstance(train.states[WALLET_KEY], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(train, monkeypatch):
    monkeypatch.setattr(GetWalletSt, "execution", fake_execution_with_error)
    status = await GetWalletSt(train).traveled()
    assert status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(train):
    query_name = GetWalletSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("id")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = GetWalletSt(train).storage_query()
    bound_method = Wallet.get
    assert storage_query == bound_method
