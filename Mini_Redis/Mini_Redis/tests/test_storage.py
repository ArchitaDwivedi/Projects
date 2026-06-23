import pytest
from storage_engine import StorageEngine
from exceptions import KeyNotFoundError


def test_put_get():

    storage = StorageEngine()

    storage.put(
        "A",
        "HELLO",
        log=False
    )

    assert (
        storage.get("A")
        == "HELLO"
    )


def test_delete():

    storage = StorageEngine()

    storage.put(
        "A",
        "HELLO",
        log=False
    )

    storage.delete(
        "A",
        log=False
    )

    with pytest.raises(
        KeyNotFoundError
    ):

        storage.get("A")


def test_overwrite():

    storage = StorageEngine()

    storage.put(
        "A",
        "1",
        log=False
    )

    storage.put(
        "A",
        "2",
        log=False
    )

    assert (
        storage.get("A")
        == "2"
    )
