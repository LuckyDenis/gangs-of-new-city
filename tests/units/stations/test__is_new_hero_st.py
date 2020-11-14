# coding: utf8
import pytest

from app.core.stations import IsNewHeroSt
from app.core.statuses import Statuses as Code


NEW_HERO = {
    "id": 123456789,
    "is_hero": None
}

NOT_NEW_HERO = {
    "id": 123456789,
    "is_hero": "hero"
}

USER_KEY = 'user'


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_new(train):
    train.states[USER_KEY] = NEW_HERO
    status = await IsNewHeroSt.traveled(train)

    assert status == Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_not_new(train):
    train.states[USER_KEY] = NOT_NEW_HERO
    status = await IsNewHeroSt.traveled(train)

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
