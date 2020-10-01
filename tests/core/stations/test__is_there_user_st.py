# coding: utf8
import pytest

from app.core.stations import IsThereUserSt
from app.core.statuses import Statuses as Code
from app.core.train import Train

USER_IS_THERE = {
    "id": 123456789
}

USER_IS_NOT_THERE = {

}

USER_KEY = 'user'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_is_there():
    train = Train({})
    train.states[USER_KEY] = USER_IS_THERE
    train = await IsThereUserSt(train).traveled()

    STATUSES = [Code.USER_IS_THERE, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_user_not_is_there():
    train = Train({})
    train.states[USER_KEY] = USER_IS_NOT_THERE
    train = await IsThereUserSt(train).traveled()

    STATUSES = [Code.USER_IS_NOT_THERE]
    statuses = train["__state__"]["statuses"]
    assert statuses == STATUSES


@pytest.mark.skip
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
