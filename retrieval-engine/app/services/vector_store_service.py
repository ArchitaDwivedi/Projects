import faiss
import numpy as np


class VectorStoreService:

    def build_index(
        self,
        indexed_chunks: list[dict]
    ) -> faiss.Index:

        if not indexed_chunks:
            raise ValueError(
                "Cannot build an index with no chunks."
            )

        embeddings = np.array(
            [
                chunk["embedding"]
                for chunk in indexed_chunks
            ],
            dtype=np.float32
        )

        faiss.normalize_L2(
            embeddings
        )

        index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )

        index.add(
            embeddings
        )

        return index

    def search(
        self,
        index: faiss.Index,
        query_embedding: list[float],
        indexed_chunks: list[dict],
        k: int = 3
    ) -> list[dict]:

        query = np.array(
            [query_embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(
            query
        )

        _, positions = index.search(
            query,
            k
        )

        return [
            indexed_chunks[position]
            for position in positions[0]
            if position != -1
        ]

    def save(
        self,
        index: faiss.Index,
        path: str
    ):

        faiss.write_index(
            index,
            path
        )

    def load(
        self,
        path: str
    ) -> faiss.Index:

        return faiss.read_index(
            path
        )
