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
    status = await IsThereInviterSt.traveled(train)

    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_inviter_not_is_there(train):
    train.states[INVITER_KEY] = VOID_INVITER
    status = await IsThereInviterSt.traveled(train)

    assert status is Code.EMERGENCY_STOP
