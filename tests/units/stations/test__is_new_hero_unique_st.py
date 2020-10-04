# coding: utf8
import pytest

from app.core.stations import IsNewHeroUniqueSt
from app.core.statuses import Statuses as Code
from app.database.queries import Hero
from tests.helpers.fake_executions import fake_execution
from tests.helpers.fake_executions import fake_execution_with_error
from tests.helpers.fake_executions import fake_execution_empty

HERO_NICK_KEY = "hero_nick"
HERO_NICK = "hero"


@pytest.fixture()
def up_train(train):
    train.data[HERO_NICK_KEY] = HERO_NICK
    return train


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(up_train, monkeypatch):
    train = up_train
    monkeypatch.setattr(IsNewHeroUniqueSt, "execution", fake_execution_empty)
    await IsNewHeroUniqueSt(train).traveled()
    assert train.status == Code.NEW_HERO_IS_UNIQUE


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_with_error(up_train, monkeypatch):
    train = up_train
    monkeypatch.setattr(
        IsNewHeroUniqueSt, "execution", fake_execution_with_error)
    await IsNewHeroUniqueSt(train).traveled()

    assert isinstance(train.states['is_hero'], dict)

    STATUSES = [Code.DATABASE_ERROR, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_hero_is_not_unique(up_train, monkeypatch):
    train = up_train
    monkeypatch.setattr(IsNewHeroUniqueSt, "execution", fake_execution)
    await IsNewHeroUniqueSt(train).traveled()

    STATUSES = [Code.NEW_HERO_IS_NOT_UNIQUE, Code.EMERGENCY_STOP]
    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__query_data(up_train):
    train = up_train
    query_name = IsNewHeroUniqueSt(train).query_data()
    query_data = train.queries[query_name]
    assert query_data.get("hero_nick")


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__storage_query(train):
    storage_query = IsNewHeroUniqueSt(train).storage_query()
    bound_method = Hero.get_by_nick
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
