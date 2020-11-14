# coding: utf8
import pytest

from app.core.stations import IsThereHeroSt
from app.core.statuses import Statuses as Code


USER = {
    "id": 123456789,
    "is_hero": "test"
}

USER_IS_NOT_HAVE_HERO = {
    "id": 123456789,
    "is_hero": None
}

USER_KEY = 'user'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_there(train):
    train.states[USER_KEY] = USER
    status = await IsThereHeroSt.traveled(train)

    assert status == Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_not_there(train):
    train.states[USER_KEY] = USER_IS_NOT_HAVE_HERO
    status = await IsThereHeroSt.traveled(train)

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
