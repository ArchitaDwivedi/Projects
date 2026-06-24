from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()


if __name__ == "__main__":
    service = EmbeddingService()

    text = """
    Redis supports persistence using AOF files.
    """

    embedding = service.generate_embedding(text)

    print(f"Dimensions: {len(embedding)}")
    print(embedding[:10])
