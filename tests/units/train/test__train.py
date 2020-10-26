# coding: utf8
import pytest
from app.core.train import Train, OrderedDict


ANSWER = {"test": "foo"}
EXCEPTION = {"args": "foo"}
NAME = "ASt"
STATION = {
    "name": NAME,
    "status": True
}


@pytest.fixture()
def train(data):
    return Train(data)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__has_payload(train):
    assert hasattr(train, "payload")
    assert isinstance(train.payload, dict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__payload_valid(train):
    payload = train.payload

    assert isinstance(payload["states"], dict)
    assert isinstance(payload["props"], dict)
    assert isinstance(payload["queries"], dict)
    assert isinstance(payload["data"], dict)
    assert isinstance(payload["answers"], list)
    assert isinstance(payload["__state__"], dict)
    assert isinstance(payload["__state__"]["exception"], dict)
    assert isinstance(payload["__state__"]["progress"], OrderedDict)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_data(train, data):
    assert hasattr(train, "data")
    assert train.data is data


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_queries(train):
    assert hasattr(train, "queries")
    assert len(train.queries) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_props(train):
    assert hasattr(train, "props")
    assert len(train.props) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_states(train):
    assert hasattr(train, "states")
    assert len(train.states) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_answers(train):
    assert hasattr(train, "answers")
    assert len(train.answers) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_setattr_answers(train):
    assert len(train.answers) == 0
    train.answers = ANSWER
    assert len(train.answers) == 1
    assert train.payload["answers"][-1] == ANSWER


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_deleter_answers(train):
    answer_id = id(train.answers)
    train.answers = ANSWER
    del train.answers
    assert len(train.answers) == 0
    assert id(train.answers) == answer_id


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_exception(train):
    assert hasattr(train, "exception")
    assert len(train.exception) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_setattr_exception(train):
    assert len(train.exception) == 0
    train.exception = EXCEPTION
    assert len(train.exception) == 1
    assert train.payload["__state__"]["exception"] == EXCEPTION


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_getattr_progress(train):
    assert hasattr(train, "progress")
    assert len(train.exception) == 0


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.train
def test__property_setattr_progress(train):
    assert len(train.progress) == 0
    train.progress = STATION
    assert len(train.progress) == 1
    assert NAME in train.payload["__state__"]["progress"]
