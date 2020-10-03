# coding: utf8
import pytest

from app.core.stations import IsThereUserSt
from app.core.statuses import Statuses as Code


USER = {
    "id": 123456789
}

VOID_USER = {}

USER_KEY = 'user'
STATUSES = [Code.USER_IS_NOT_THERE, Code.EMERGENCY_STOP]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_there(train):
    train.states[USER_KEY] = USER
    await IsThereUserSt(train).traveled()

    assert train.status == Code.USER_IS_THERE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_inviter_not_is_there(train):
    train.states[USER_KEY] = VOID_USER
    await IsThereUserSt(train).traveled()

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
