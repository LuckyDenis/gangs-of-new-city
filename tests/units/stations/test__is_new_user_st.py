# coding: utf8
import pytest

from app.core.stations import IsNewUserSt
from app.core.statuses import Statuses as Code


USER_IS_NO_NEW = {
    "id": 123456789
}

USER_IS_NEW = {

}

USER_KEY = 'user'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_there(train):
    train.states[USER_KEY] = USER_IS_NO_NEW
    train = await IsNewUserSt(train).traveled()

    STATUSES = [Code.USER_IS_NOT_NEW, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_not_is_there(train):
    train.states[USER_KEY] = USER_IS_NEW
    train = await IsNewUserSt(train).traveled()

    STATUSES = Code.USER_IS_NEW
    statuses = train["__state__"]["statuses"]
    assert statuses[-1] == STATUSES


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
