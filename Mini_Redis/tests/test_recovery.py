import os

from storage_engine import StorageEngine


def setup_function():

    try:
        os.remove("db.aof")
    except FileNotFoundError:
        pass


def test_replay_put():

    storage = StorageEngine()

    storage.put(
        "A",
        "1"
    )

    recovered = StorageEngine()

    recovered.replay_log()

    assert (
        recovered.get("A")
        == "1"
    )


def test_replay_delete():

    storage = StorageEngine()

    storage.put(
        "A",
        "1"
    )

    storage.delete(
        "A"
    )

    recovered = StorageEngine()

    recovered.replay_log()

    assert "A" not in recovered.db
