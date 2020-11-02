# coding: utf8
import pytest
from app.views.icons import emojize
from app.views.icons import demojize

EMOJIZE = ":thumbsup:"
DEMOJIZE = "👍"


@pytest.mark.unit
@pytest.mark.views
def test__emojize():
    assert emojize(EMOJIZE) == DEMOJIZE


@pytest.mark.unit
@pytest.mark.views
def test__demojize():
    assert demojize(DEMOJIZE) == EMOJIZE
