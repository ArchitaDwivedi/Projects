from services.pdf_service import PDFService
from services.chunk_service import ChunkService
from services.embedding_service import EmbeddingService
from services.similarity_service import SimilarityService
from services.pdf_clean_service import TextCleaner
from services.answer_service import AnswerService

pdf_service = PDFService()
chunk_service = ChunkService()
embedding_service = EmbeddingService()

text = pdf_service.extract_text("data/uploads/redis.pdf")
text = TextCleaner.clean(text)
chunks = chunk_service.chunk_text(text)

embeddings = embedding_service.generate_embedding(chunks)

indexed_chunks = []

for chunk, embedding in zip(chunks, embeddings):
    indexed_chunks.append(
        {
            "text": chunk,
            "embedding": embedding
        }
    )

question = "What is durability?"

question_embedding = embedding_service.generate_embedding(
    question
)

matches = SimilarityService.find_best_matches(
    question_embedding,
    indexed_chunks,
    k=3
)

# for idx, match in enumerate(matches, start=1):
#     print(f"\nMatch {idx}")
#     print(
#         len(matches[0]["text"].split())
#     )
#     print("-" * 50)
#     print(match["text"])

contexts = [
    match["text"]
    for match in matches
]

answer_service = AnswerService()

contexts = [
    match["text"]
    for match in matches
]

answer = answer_service.generate_answer(
    question,
    contexts
)

print(answer)
