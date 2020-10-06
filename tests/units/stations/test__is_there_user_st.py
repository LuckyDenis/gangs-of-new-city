# coding: utf8
import pytest

from app.core.stations import IsThereUserSt
from app.core.statuses import Statuses as Code


USER = {
    "id": 123456789
}

VOID_USER = {}

USER_KEY = 'user'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_there(train):
    train.states[USER_KEY] = USER
    status = await IsThereUserSt(train).traveled()

    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_inviter_not_is_there(train):
    train.states[USER_KEY] = VOID_USER
    status = await IsThereUserSt(train).traveled()

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
