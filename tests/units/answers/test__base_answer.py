# coding: utf8
import pytest
from app.views import answers as an
from tests.helpers.fake_i18n import I18N


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.answers
async def test__inside_get(state, monkeypatch):
    monkeypatch.setattr(an, "I18N", I18N)
    with pytest.raises(NotImplementedError):
        await an.BaseAnswer._get(state)


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.answers
async def test__get(state, monkeypatch):
    monkeypatch.setattr(an, "I18N", I18N)
    with pytest.raises(NotImplementedError):
        await an.BaseAnswer._get(state)
