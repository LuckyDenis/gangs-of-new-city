# coding: utf8
import pytest

from app.core.stations import ViewHeroSt
from app.core.statuses import Statuses as Code


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    status = await ViewHeroSt.traveled(train)
    assert status is Code.IS_OK


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
