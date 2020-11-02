# coding: utf8
import pytest
from app.views.cmds import EmojizeCommands as ECmds
from app.views.icons import emojize


E_CMDS = [
    ECmds.WARNING,
    ECmds.WHITE_CHECK_MARK,
    ECmds.BUG
]


@pytest.mark.unit
@pytest.mark.views
def test__template():
    assert ECmds._T.value == ":{0}:"


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("cmd", E_CMDS)
def test__make(cmd):
    assert cmd.mk() == emojize(cmd.value)


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("cmd", E_CMDS)
def test__get(cmd):
    assert cmd.get() == f"^{emojize(cmd.value)}"
