# coding: utf8
import pytest
from app.views import templates as t


class I18N:
    def gettext_lazy(self, text):
        return text


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__get_template_is_not_realize(monkeypatch):
    monkeypatch.setattr(t, "I18N", I18N)
    with pytest.raises(NotImplementedError):
        t.BaseMessage.get_template({"test": "foo"})
