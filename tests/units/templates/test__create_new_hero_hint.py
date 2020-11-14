# coding: utf8
import pytest
from app.views import templates as t
from app.views.cmds import Commands as Cmds
from app.views.cmds import EmojizeCommands as ECmds
from tests.helpers.fake_i18n import I18N


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
def test__get_template(monkeypatch):
    monkeypatch.setattr(t, "I18N", I18N)
    text = t.NewUserIsAccept.get_template()

    assert isinstance(text, str)


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.dispatcher
@pytest.mark.parametrize("cmd", [
    Cmds.FACCEPT.mk(),
    ECmds.FACCEPT.mk()
])
def test__checking_cmds(monkeypatch, cmd):
    monkeypatch.setattr(t, "I18N", I18N)
    text = t.NewUserIsNotAccept.get_template()

    assert text.find(cmd) != -1
