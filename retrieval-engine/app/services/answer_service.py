import ollama


class AnswerService:

    def generate_answer(
        self,
        question: str,
        context_chunks: list[str]
    ) -> str:

        context = "\n\n".join(context_chunks)

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are answering questions using ONLY the provided context.

Rules:
- Use only information explicitly stated in the context.
- Never use outside knowledge.
- Never guess or infer details.
- If the answer is not fully present, say:
  "I could not find the answer in the provided document."
- Keep answers concise (3-6 sentences).
- Do not
"""
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{question}"
                }
            ]
        )

        return response["message"]["content"]
