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
STATUSES = [Code.USER_IS_INVITER, Code.EMERGENCY_STOP]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_not_invited(train):
    train.states[USER_KEY] = USER
    train.states[INVITER_KEY] = INVITER

    await UserIsInviterSt(train).traveled()
    assert train.status is Code.USER_IS_NOT_INVITER


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_invited(train):
    train.states[USER_KEY] = USER
    train.states[INVITER_KEY] = USER

    await UserIsInviterSt(train).traveled()

    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES
