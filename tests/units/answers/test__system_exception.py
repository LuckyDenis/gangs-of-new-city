# coding: utf8
import pytest
from app.views import answers as an
from app.views import templates as t
from tests.helpers.fake_i18n import I18N
from tests.helpers.fake_base_message import FakeMessage
from app.views.helpers import Types


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.answers
async def test__inside_get(state, monkeypatch):
    monkeypatch.setattr(an, "I18N", I18N)
    monkeypatch.setattr(t, "SystemException", FakeMessage)
    await an.SystemException._get(state)


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.answers
async def test__get(state, data, monkeypatch):
    monkeypatch.setattr(an, "I18N", I18N)
    monkeypatch.setattr(t, "SystemException", FakeMessage)
    answer = await an.SystemException.get(state)

    assert answer["chat_id"] == data["id"]
    assert answer["message_type"] == Types.TEXT_MESSAGE
    assert isinstance(answer["text"], str)
