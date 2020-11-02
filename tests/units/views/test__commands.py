# coding: utf8
import pytest

from app.views.cmds import Commands as Cmds

CMDS = [
    Cmds.START,
    Cmds.ANO,
    Cmds.AYES,
    Cmds.HNAME,
    Cmds.BUG
]


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("cmd", CMDS)
def test__lower(cmd):
    assert cmd.mk().islower()


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("cmd", CMDS)
def test__correct_make_cmd(cmd):
    assert cmd.mk()[0] == "/"


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.parametrize("cmd", CMDS)
def test__correct_get(cmd):
    assert cmd.get() == cmd.name.lower()
