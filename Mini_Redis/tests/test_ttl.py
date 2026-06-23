import time
import pytest

from storage_engine import StorageEngine
from exceptions import KeyNotFoundError


def test_ttl_expiry():

    storage = StorageEngine()

    storage.put(
        "A",
        "HELLO",
        ttl=1,
        log=False
    )

    time.sleep(2)

    with pytest.raises(
        KeyNotFoundError
    ):

        storage.get("A")


def test_ttl_not_expired():

    storage = StorageEngine()

    storage.put(
        "A",
        "HELLO",
        ttl=10,
        log=False
    )

    assert (
        storage.get("A")
        == "HELLO"
    )
