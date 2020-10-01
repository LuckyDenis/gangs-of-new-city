# coding: utf8
import pytest

from tests.helpers.data import DATA


@pytest.fixture(scope='session')
def data():
    return DATA
