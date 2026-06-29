from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        embedding = self.model.encode(text)

        return embedding.tolist()

    def index_chunks(
        self,
        chunks: list[dict],
        start_id: int
    ) -> list[dict]:

        indexed_chunks = []

        current_id = start_id

        for chunk in chunks:

            indexed_chunks.append(
                {
                    "id": current_id,
                    "page": chunk["page"],
                    "text": chunk["text"],
                    "embedding": self.generate_embedding(
                        chunk["text"]
                    )
                }
            )

            current_id += 1

        return indexed_chunks
