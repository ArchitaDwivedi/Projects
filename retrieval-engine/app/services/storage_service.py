import json
import os


class StorageService:

    @staticmethod
    def save(
        indexed_chunks: list[dict],
        file_path: str
    ) -> None:

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                indexed_chunks,
                file,
                indent=4
            )

    @staticmethod
    def load(
        file_path: str
    ) -> list[dict]:

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"{file_path} does not exist."
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)
