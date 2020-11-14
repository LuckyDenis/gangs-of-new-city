# coding: utf8
import pytest

from app.core.stations import IsCorrectHeroNickSt
from app.core.statuses import Statuses as Code
from app.core.train import Train
from app.database.fixture import Languages

USER = {
    "language": Languages.ENGLISH
}


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
@pytest.mark.parametrize("hero_nick", [
    "=====", "1234",
    "qwer", "qwertyuiopasdfghjklzxcqweqwerqwe",
    "+++++++", "(((((((", "********",
    "&&&&&&&", "             ",
    ")open()", "}select()"
])
async def test__hero_nick_is_not_correct(data, hero_nick):
    dt = {"hero_nick": hero_nick}
    dt.update(data)
    train = Train(dt)
    train.states["user"] = USER
    status = await IsCorrectHeroNickSt.traveled(train)
    assert status == Code.EMERGENCY_STOP


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
@pytest.mark.parametrize("hero_nick", [
    "12345", "12345678901234567890",
    "qwert", "qwertyuiopasdfghjklz",
    "_____", "......", "Mr.Smith",
    "Ms.Smith", "GOOD_LUCKY",
    ".snowman.", "_d_j_o_h_n_"
])
async def test__hero_nick_is_correct(data, hero_nick):
    dt = {"hero_nick": hero_nick}
    dt.update(data)
    train = Train(dt)
    train.states["user"] = USER
    status = await IsCorrectHeroNickSt.traveled(train)
    assert status == Code.IS_OK
