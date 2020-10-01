# coding: utf8
import pytest
from app.core.stations import StartRailwayDepotSt
from app.core.statuses import Statuses as Code
from app.core.train import Train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled():
    train = await StartRailwayDepotSt(Train({})).traveled()
    assert train.status == Code.IN_THE_WAY
