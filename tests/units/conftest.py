# coding: utf8
import pytest
from app.core.train import Train
from tests.helpers.data import DATA


@pytest.fixture()
def train():
    train = Train(DATA)
    return train
