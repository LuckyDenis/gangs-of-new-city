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


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_not_blocked(train):
    train.states[USER_KEY] = USER_IS_NOT_BLOCKED
    status = await IsUserBlockedSt.traveled(train)

    assert status == Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_blocked(train):
    train.states[USER_KEY] = USER_IS_BLOCKED
    status = await IsUserBlockedSt.traveled(train)

    assert status is Code.EMERGENCY_STOP


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
