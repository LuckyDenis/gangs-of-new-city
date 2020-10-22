# coding: utf8
import pytest
from app.core.statuses import Statuses


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__statuses_is_ok():
    assert Statuses.IS_OK is True


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__statuses_emergency_stop():
    assert Statuses.EMERGENCY_STOP is False
