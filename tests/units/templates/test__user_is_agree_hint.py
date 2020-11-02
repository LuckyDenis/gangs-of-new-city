# coding: utf8
import pytest
from app.views import templates as t
from tests.helpers.fake_i18n import I18N


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__get_template(monkeypatch):
    monkeypatch.setattr(t, "I18N", I18N)
    text = t.UserIsAgreeHint.get_template()

    assert isinstance(text, str)
