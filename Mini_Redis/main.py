from storage_engine import StorageEngine
from executor import Executor
from command_parser import Parser
from exceptions import KeyNotFoundError
from server import RedisServer
import threading
'''
    Main redis app
    Ever hunting for commands
'''
# main.py


def build_app():

    storage = StorageEngine()

    storage.replay_log()

    compact_thread = threading.Thread(
        target=storage.compact_daemon,
        daemon=True
    )

    compact_thread.start()

    cleanup_thread = threading.Thread(
        target=storage.cleanup_expired_keys,
        daemon=True
    )
    cleanup_thread.start()

    executor = Executor(storage)

    return RedisServer(executor)


def main():

    server = build_app()

    server.start()


if __name__ == "__main__":
    main()
