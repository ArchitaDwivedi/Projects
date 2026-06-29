import json
import os


class RegistryService:

    def __init__(self):

        self.path = "data/documents.json"

    def load(self) -> dict:

        if not os.path.exists(self.path):
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            documents = json.load(file)

        return {
            document["filename"]: document
            for document in documents
        }

    def save(
        self,
        documents: dict
    ):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                list(documents.values()),
                file,
                indent=4
            )

    def get(
        self,
        filename: str,
        documents: dict
    ) -> dict | None:

        return documents.get(filename)

    def exists(
        self,
        filename: str,
        documents: dict
    ) -> bool:

        return filename in documents

    def get_next_vector_id(
        self,
        documents: dict
    ) -> int:

        highest_id = -1

        for document in documents.values():

            vector_ids = document.get(
                "vector_ids",
                []
            )

            if vector_ids:

                highest_id = max(
                    highest_id,
                    max(vector_ids)
                )

        return highest_id + 1

    def add_document(
        self,
        filename: str,
        file_hash: str,
        vector_ids: list[int],
        documents: dict
    ):

        documents[filename] = {
            "filename": filename,
            "hash": file_hash,
            "vector_ids": vector_ids
        }

        self.save(documents)

    def remove_document(
        self,
        filename: str,
        documents: dict
    ):

        documents.pop(
            filename,
            None
        )

        self.save(documents)
