# coding: utf8
import pytest

from app.core.stations import IsUserBlockedSt
from app.core.statuses import Statuses as Code


USER_IS_BLOCKED = {
    "id": 123456789,
    "is_blocked": True
}

USER_IS_NOT_BLOCKED = {
    "id": 123456789,
    "is_blocked": False
}

USER_KEY = 'user'
STATUSES = [Code.USER_IS_BLOCKED, Code.EMERGENCY_STOP]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_not_blocked(train):
    train.states[USER_KEY] = USER_IS_NOT_BLOCKED
    await IsUserBlockedSt(train).traveled()

    assert train.status == Code.USER_IS_NOT_BLOCKED


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_blocked(train):
    train.states[USER_KEY] = USER_IS_BLOCKED
    await IsUserBlockedSt(train).traveled()

    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
