from math import sqrt
import heapq


class SimilarityService:

    @staticmethod
    def cosine_similarity(
        vector_a: list[float],
        vector_b: list[float]
    ) -> float:

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = sum(
            a * a
            for a in vector_a
        ) ** 0.5

        magnitude_b = sum(
            b * b
            for b in vector_b
        ) ** 0.5

        return dot_product / (
            magnitude_a * magnitude_b
        )

    @staticmethod
    def find_best_matches(
        query_embedding: list[float],
        indexed_chunks: list[dict],
        k: int = 3
    ) -> list[dict]:

        heap = []

        for idx, chunk in enumerate(indexed_chunks):

            score = SimilarityService.cosine_similarity(
                query_embedding,
                chunk["embedding"]
            )

            heapq.heappush(
                heap,
                (score, idx, chunk)
            )

            if len(heap) > k:
                heapq.heappop(heap)

        results = []

        for score, idx, chunk in sorted(
            heap,
            reverse=True
        ):
            results.append(chunk)

        return results
