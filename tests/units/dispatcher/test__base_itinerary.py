# coding: utf8
import pytest
from app.core.dispatcher import BaseItinerary
from app.core.stations import BaseSt
from app.core.statuses import Statuses as Code


ANSWER = "answer test"


class ASt(BaseSt):
    async def traveled(self):
        self.train.states["A"] = True
        return Code.IS_OK


class BSt(BaseSt):
    async def traveled(self):
        self.train.states["B"] = True
        return Code.EMERGENCY_STOP


class CSt(BaseSt):
    async def traveled(self):
        self.train.states["C"] = True
        self.train.answers = ANSWER
        return Code.IS_OK


def fake_required_keys(*_):
    return ["id"]


def fake_required_keys_not_correct(*_):
    return ["not_correct"]


def fake_stations(*_):
    return [
        ASt,
        CSt
    ]


def fake_stations_emergency_stop(*_):
    return [
        ASt,
        BSt,
        CSt
    ]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__init(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    base_itinerary = BaseItinerary(data)
    assert base_itinerary.train.data == data


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
async def test__move(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    base_itinerary = BaseItinerary(data)
    assert base_itinerary.train.data == data


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
async def test__move(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    monkeypatch.setattr(
        BaseItinerary, "stations", fake_stations)
    base_itinerary = BaseItinerary(data)
    await base_itinerary.move()
    assert base_itinerary.get_answers() == [ANSWER]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
async def test__move_with_emergency_stop(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    monkeypatch.setattr(
        BaseItinerary, "stations", fake_stations_emergency_stop)
    base_itinerary = BaseItinerary(data)
    await base_itinerary.move()
    assert base_itinerary.get_answers() == []


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__stations(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    with pytest.raises(NotImplementedError):
        BaseItinerary(data).stations()


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__required_keys(data):
    with pytest.raises(NotImplementedError):
        BaseItinerary(data)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__data_has_required_keys_correct(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys)
    base_itinerary = BaseItinerary(data)
    assert base_itinerary.data_has_required_keys() is True


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__data_has_required_keys_not_correct(data, monkeypatch):
    monkeypatch.setattr(
        BaseItinerary, "required_keys", fake_required_keys_not_correct)
    base_itinerary = BaseItinerary(data)
    assert base_itinerary.data_has_required_keys() is False
