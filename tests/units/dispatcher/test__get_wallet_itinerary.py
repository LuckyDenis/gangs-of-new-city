# coding: utf8
import pytest
from app.core import stations as st
from app.core.dispatcher import GetWalletItinerary


REQUIRED_KEYS = ["id"]

STATIONS = [
    st.StartRailwayDepotSt,
    st.GetUserSt,
    st.IsThereUserSt,
    st.IsUserBlockedSt,
    st.GetWalletSt,
    st.IsThereWalletSt,
    st.ViewWalletSt,
    st.FinishRailwayDepotSt
]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__required_keys(data):
    itinerary = GetWalletItinerary(data)
    required_keys = itinerary.required_keys()

    assert sorted(required_keys) == sorted(REQUIRED_KEYS)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__stations(data):
    itinerary = GetWalletItinerary(data)
    stations = itinerary.stations()

    assert stations == STATIONS
