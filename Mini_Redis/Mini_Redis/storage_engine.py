from exceptions import KeyNotFoundError
from executor import Executor
from command_parser import Parser
import json
import time
import threading


class StorageEngine:

    def __init__(self):
        self.db = {}
        self.expiry = {}
        self.lock = threading.Lock()

    def _append_log(self, command):

        with open("db.aof", "a") as f:
            f.write(command + "\n")

    def _is_expired(self, key):

        if key not in self.expiry:
            return False

        return time.time() > self.expiry[key]

    def compact_aof(self):

        with self.lock:

            with open("db.aof", "w") as f:

                for key, value in self.db.items():

                    if key in self.expiry:

                        expiry_time = (
                            self.expiry[key]
                        )

                        f.write(
                            f"PUT {key} {value} "
                            f"EXPIRES_AT {expiry_time}\n"
                        )

                    else:

                        f.write(
                            f"PUT {key} {value}\n"
                        )

    def put(
        self,
        key,
        value,
        ttl=None,
        log=True
    ):

        with self.lock:

            self.db[key] = value

            if ttl is None:
                self.expiry.pop(key, None)

            expiry_time = None

            if ttl is not None:

                expiry_time = (
                    time.time() + ttl
                )

                self.expiry[key] = expiry_time

            if expiry_time:

                log_command = (
                    f"PUT {key} {value} "
                    f"EXPIRES_AT {expiry_time}"
                )

            else:

                log_command = (
                    f"PUT {key} {value}"
                )

        if log:

            self._append_log(
                log_command
            )

        return "OK"

    def get(self, key):

        with self.lock:

            if self._is_expired(key):

                del self.db[key]
                del self.expiry[key]

                raise KeyNotFoundError(
                    f'Key "{key}" not found'
                )

            if key not in self.db:

                raise KeyNotFoundError(
                    f'Key "{key}" not found'
                )

            return self.db[key]

    def delete(
        self,
        key,
        log=True
    ):

        with self.lock:

            if key not in self.db:

                raise KeyNotFoundError(
                    f'Key "{key}" not found'
                )

            del self.db[key]

            self.expiry.pop(key, None)

        if log:

            self._append_log(
                f"DELETE {key}"
            )

        return "OK"

    def replay_log(self):

        self.db = {}
        self.expiry = {}

        try:

            with open("db.aof", "r") as f:

                for line in f:

                    parts = line.strip().split()

                    if not parts:
                        continue

                    if parts[0] == "PUT":

                        key = parts[1]
                        value = parts[2]

                        self.db[key] = value

                        if len(parts) == 5:

                            expiry_time = float(parts[4])

                            self.expiry[key] = expiry_time

                    elif parts[0] == "DELETE":

                        key = parts[1]

                        self.db.pop(key, None)

                        self.expiry.pop(key, None)

        except FileNotFoundError:
            pass
