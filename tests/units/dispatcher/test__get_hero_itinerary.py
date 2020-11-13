# coding: utf8
import pytest
from app.core import stations as st
from app.core.dispatcher import GetHeroItinerary


REQUIRED_KEYS = ["id"]

STATIONS = [
    st.StartRailwayDepotSt,
    st.GetUserSt,
    st.IsThereUserSt,
    st.IsUserBlockedSt,
    st.IsThereHeroSt,
    st.GetHeroSt,
    st.ViewHeroSt,
    st.FinishRailwayDepotSt
]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__required_keys(data):
    itinerary = GetHeroItinerary(data)
    required_keys = itinerary.required_keys()

    assert sorted(required_keys) == sorted(REQUIRED_KEYS)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__stations(data):
    itinerary = GetHeroItinerary(data)
    stations = itinerary.stations()

    assert stations == STATIONS
