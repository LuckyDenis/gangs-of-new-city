# coding: utf8
import pytest
from app.core.stations import StartRailwayDepotSt
from app.core.statuses import Statuses as Code


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    status = await StartRailwayDepotSt.traveled(train)
    assert status is Code.IS_OK
