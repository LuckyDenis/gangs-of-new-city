# coding: utf8
import pytest
from enum import Enum
from app.views.helpers import Types


TYPES = [
    Types.TEXT_MESSAGE
]


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("message_type", Types)
def test__message_type(message_type):
    assert isinstance(message_type, Enum)
