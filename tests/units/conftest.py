# coding: utf8
import pytest
from app.core.train import Train
from tests.helpers.data import DATA
from app.core.statuses import Statuses as Code


@pytest.fixture()
def train():
    train = Train(DATA)
    train.status = Code.IN_THE_WAY
    return train
