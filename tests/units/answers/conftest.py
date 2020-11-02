# coding: utf8
import pytest
from app.database.fixture import Languages


@pytest.fixture(scope="session")
def state(data):
    return {
        "language": Languages.ENGLISH,
        "id": data["id"]
    }
