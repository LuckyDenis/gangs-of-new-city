# coding: utf8
import pytest

from app.core.stations import DoesUserHaveAgreeingSt
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
    train.states["user"]["is_agreeing"] = True
    status = await DoesUserHaveAgreeingSt(train).traveled()
    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_not_has_agreeing(up_train):
    train = up_train
    train.states["user"]["has_agreeing"] = False
    status = await DoesUserHaveAgreeingSt(train).traveled()

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
