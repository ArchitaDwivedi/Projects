import os

from storage_engine import StorageEngine


def setup_function():

    try:
        os.remove("db.aof")
    except FileNotFoundError:
        pass


def test_compaction_keeps_latest_value():

    storage = StorageEngine()

    storage.put(
        "A",
        "1"
    )

    storage.put(
        "A",
        "2"
    )

    storage.put(
        "A",
        "3"
    )

    storage.compact_aof()

    recovered = StorageEngine()

    recovered.replay_log()

    assert (
        recovered.get("A")
        == "3"
    )
