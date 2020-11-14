# coding: utf8
import pytest
from app.core import stations as st
from app.core.dispatcher import UserStartItinerary


REQUIRED_KEYS = ["id", "language", "datetime"]

STATIONS = [
            st.StartRailwayDepotSt,
            st.GetUserSt,
            st.IsNewUserSt,
            st.UserCreateSt,
            st.DoesUserHaveReferralIdSt,
            st.GetInviterSt,
            st.IsThereInviterSt,
            st.UserIsInviterSt,
            st.AddReferralDataSt,
            st.FinishRailwayDepotSt
        ]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__required_keys(data):
    itinerary = UserStartItinerary(data)
    required_keys = itinerary.required_keys()

    assert sorted(required_keys) == sorted(REQUIRED_KEYS)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__stations(data):
    itinerary = UserStartItinerary(data)
    stations = itinerary.stations()

    assert stations == STATIONS
