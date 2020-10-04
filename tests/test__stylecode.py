# coding: utf8
import subprocess
import pytest


@pytest.mark.style
def test__style_pep8():
    result = subprocess.run(
        ["pycodestyle", "app/", "tests/"],
        stdout=subprocess.PIPE,
        text=True)
    assert result.stdout == ""
    assert result.returncode == 0
