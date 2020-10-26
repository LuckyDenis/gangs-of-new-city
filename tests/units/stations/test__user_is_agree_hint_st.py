# coding: utf8
import pytest

from app.core.stations import UserIsAgreeHintSt
from app.database.fixture import Languages
from app.core.statuses import Statuses as Code


@pytest.fixture()
def up_train(train):
    train.states["user"] = {"language": Languages.RUSSIAN}
    return train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(up_train):
    train = up_train
    status = await UserIsAgreeHintSt(train).traveled()
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
