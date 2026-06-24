class ChunkService:

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> list[str]:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            chunk_words = words[start:start + chunk_size]

            chunks.append(
                " ".join(chunk_words)
            )

            start += chunk_size - overlap

        return chunks


if __name__ == "__main__":

    text = " ".join(
        [f"word{i}" for i in range(1200)]
    )

    chunk_service = ChunkService()

    chunks = chunk_service.chunk_text(
        text,
        chunk_size=500,
        overlap=100
    )

    print(f"Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}")
        print(chunk[:100])
