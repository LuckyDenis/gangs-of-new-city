# coding: utf8
import pytest

from app.core.stations import IsThereHeroSt
from app.core.statuses import Statuses as Code


HERO = {
    "id": 123456789,
    "nick": "test"
}

EMPTY_HERO = {}

HERO_KEY = 'hero'
STATUSES = [Code.HERO_IS_NOT_THERE, Code.EMERGENCY_STOP]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_there(train):
    train.states[HERO_KEY] = HERO
    await IsThereHeroSt(train).traveled()

    assert train.status == Code.HERO_IS_THERE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_not_there(train):
    train.states[HERO_KEY] = EMPTY_HERO
    await IsThereHeroSt(train).traveled()

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
