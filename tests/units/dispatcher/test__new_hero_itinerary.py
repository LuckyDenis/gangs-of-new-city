# coding: utf8
import pytest
from app.core import stations as st
from app.core.dispatcher import NewHeroItinerary


REQUIRED_KEYS = ["id", "hero_nick"]

STATIONS = [
    st.StartRailwayDepotSt,
    st.GetUserSt,
    st.IsThereUserSt,
    st.IsUserBlockedSt,
    st.IsNewHeroSt,
    st.IsNewHeroUniqueSt,
    st.NewHeroCreateSt,
    st.FinishRailwayDepotSt
]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__required_keys(data):
    itinerary = NewHeroItinerary(data)
    required_keys = itinerary.required_keys()

    assert sorted(required_keys) == sorted(REQUIRED_KEYS)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__stations(data):
    itinerary = NewHeroItinerary(data)
    stations = itinerary.stations()

    assert stations == STATIONS
