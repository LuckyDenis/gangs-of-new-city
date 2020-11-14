# coding: utf8
import pytest

from app.core.stations import AddReferralDataSt
from app.core.statuses import Statuses as Code
from app.database.queries import Referral
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error


INVITER = {
    "id": 987654321
}

USER = {
    "id": 123456789
}

KEY_INVITED = "invited"
KEY_INVITER = "inviter"


@pytest.fixture
def up_train(train):
    train.data["id"] = USER["id"]
    train.states["inviter"] = INVITER
    return train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(up_train, monkeypatch):
    monkeypatch.setattr(AddReferralDataSt, "execution", fake_execution)
    status = await AddReferralDataSt.traveled(up_train)

    assert status == Code.IS_OK
    assert isinstance(up_train.states['inviter'], dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(up_train, monkeypatch):
    monkeypatch.setattr(
        AddReferralDataSt, "execution", fake_execution_with_error)
    status = await AddReferralDataSt.traveled(up_train)

    assert status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(up_train):
    query_name = AddReferralDataSt.query_data(up_train)
    query_data = up_train.queries[query_name]
    assert query_data.get("invited")
    assert query_data.get("inviter")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query():
    storage_query = AddReferralDataSt.storage_query()
    bound_method = Referral.create
    assert storage_query == bound_method


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
