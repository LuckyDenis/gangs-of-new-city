# coding: utf8
import pytest

from app.core.stations import NewHeroCreateSt
from app.core.statuses import Statuses as Code
from app.database.queries import Hero
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error
from tests.helpers.fake_executions import fake_execution_empty


@pytest.fixture()
def up_train(train):
    train.data["hero_nick"] = "nick"
    return train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(up_train, monkeypatch):
    train = up_train
    monkeypatch.setattr(NewHeroCreateSt, "execution", fake_execution_empty)
    await NewHeroCreateSt(train).traveled()
    assert train.status == Code.NEW_HERO_CREATE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(up_train, monkeypatch):
    train = up_train
    monkeypatch.setattr(NewHeroCreateSt, "execution", fake_execution_with_error)
    await NewHeroCreateSt(train).traveled()

    STATUSES = [Code.DATABASE_ERROR, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(up_train):
    train = up_train
    query_name = NewHeroCreateSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("id")
    assert query_data.get("hero_nick")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = NewHeroCreateSt(train).storage_query()
    bound_method = Hero.create
    assert storage_query == bound_method


@pytest.mark.skip("Требуется `views.answers`.")
@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__add_out_answer():
    """
    Добавить когда будет реализован пакет `app.views`.
    """
    pass