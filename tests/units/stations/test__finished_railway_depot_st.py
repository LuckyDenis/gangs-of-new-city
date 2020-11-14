# coding: utf8
import pytest

from app.core.stations import FinishRailwayDepotSt
from app.core.statuses import Statuses as Code
from app.core.train import Train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    status = await FinishRailwayDepotSt.traveled(train)
    assert status == Code.IS_OK
