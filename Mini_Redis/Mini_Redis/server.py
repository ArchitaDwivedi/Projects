import time
import socket
import threading
from command_parser import Parser


class RedisServer:

    def __init__(
        self,
        executor,
        host="localhost",
        port=6379
    ):

        self.executor = executor
        self.lock = threading.Lock()
        self.host = host
        self.port = port

    def handle_command(self, raw_command):

        parser = Parser(raw_command)

        typ, key, value, ttl = (
            parser.command_split()
        )

        parser.validation(
            typ,
            key,
            value,
            ttl
        )

        command = parser.build_cmd_object(
            typ,
            key,
            value,
            ttl
        )

        result = self.executor.execute(command)

        return result if result is not None else "OK"

    def cleanup_expired_keys(self):

        while True:

            with self.lock:

                expired_keys = []

                for key, expiry_time in list(self.expiry.items()):

                    if time.time() > expiry_time:

                        expired_keys.append(key)

                for key in expired_keys:
                    print(f"Cleaning up {key}")
                    self.db.pop(key, None)

                    self.expiry.pop(key, None)

            time.sleep(1)

    def compact_daemon(self):

        while True:

            time.sleep(600)  # 10 min

            self.compact_aof()

    def start(self):

        server = socket.socket()

        server.bind(
            (self.host, self.port)
        )

        server.listen()

        print(
            f"Listening on {self.host}:{self.port}"
        )

        while True:

            conn, addr = server.accept()

            thread = threading.Thread(
                target=self.handle_client,
                args=(conn,)
            )

            thread.start()

            print(
                f"Client connected: {addr}"
            )
            print(
                f"Thread started: {threading.current_thread().name}"
            )

            self.handle_client(conn)

    def handle_client(self, conn):

        with conn:

            while True:

                data = conn.recv(1024)

                if not data:
                    break

                try:

                    response = (
                        self.handle_command(
                            data.decode().strip()
                        )
                    )

                except Exception as e:

                    response = str(e)

                conn.send(
                    (str(response) + "\n").encode()
                )
