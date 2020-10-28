# coding: utf8
import pytest
from app.helpers.decorators import singleton


@singleton
class Foo:
    pass


@pytest.mark.unit
def test__singleton():
    first = Foo()
    second = Foo()
    assert id(first) == id(second)
