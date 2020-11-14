# coding: utf8
import pytest

from app.core.stations import UserIsInviterSt
from app.core.statuses import Statuses as Code


USER = {
    "id": 123456789
}

INVITER = {
    "id": 987654321
}

USER_KEY = 'user'
INVITER_KEY = "inviter"


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_not_invited(train):
    train.states[USER_KEY] = USER
    train.states[INVITER_KEY] = INVITER

    status = await UserIsInviterSt.traveled(train)
    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_invited(train):
    train.states[USER_KEY] = USER
    train.states[INVITER_KEY] = USER

    status = await UserIsInviterSt.traveled(train)
    assert status is Code.EMERGENCY_STOP
