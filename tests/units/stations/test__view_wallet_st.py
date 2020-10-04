# coding: utf8
import pytest

from app.core.stations import ViewWalletSt
from app.core.statuses import Statuses as Code


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    await ViewWalletSt(train).traveled()

    assert train.status == Code.VIEW_WALLET


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass
