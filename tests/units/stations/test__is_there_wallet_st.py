# coding: utf8
import pytest

from app.core.stations import IsThereWalletSt
from app.core.statuses import Statuses as Code


WALLET = {
    "id": 123456789,
    "is_blocked": True
}

EMPTY_WALLET = {}

WALLET_KEY = 'wallet'
STATUSES = [Code.WALLET_IS_NOT_THERE, Code.EMERGENCY_STOP]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_wallet_is_there(train):
    train.states[WALLET_KEY] = WALLET
    await IsThereWalletSt(train).traveled()

    assert train.status == Code.WALLET_IS_THERE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_wallet_is_not_there(train):
    train.states[WALLET_KEY] = EMPTY_WALLET
    await IsThereWalletSt(train).traveled()

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
