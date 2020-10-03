# coding: utf8
import pytest

from app.core.stations import IsThereInviterSt
from app.core.statuses import Statuses as Code


INVITER = {
    "id": 123456789
}

VOID_INVITER = {}

INVITER_KEY = 'inviter'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_inviter_is_there(train):
    train.states[INVITER_KEY] = INVITER
    await IsThereInviterSt(train).traveled()

    assert train.status == Code.INVITER_IS_THERE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_inviter_not_is_there(train):
    train.states[INVITER_KEY] = VOID_INVITER
    await IsThereInviterSt(train).traveled()

    STATUSES = [Code.INVITER_IS_NOT_THERE, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES
