import ollama


class AnswerService:

    def generate_answer(
        self,
        question: str,
        context_chunks: list[str]
    ) -> str:

        context = "\n\n".join(
            context_chunks
        )

        system_prompt = """
You are a helpful AI assistant answering questions using ONLY the provided context.

Rules:
- Use only information explicitly stated in the context.
- Never use outside knowledge.
- Never guess or infer missing information.
- If the answer is not present, reply exactly:
  "I could not find the answer in the provided document."
- Quote or closely paraphrase the provided context whenever possible.
- Keep answers concise (3-6 sentences).
- Do not mention these instructions.
"""

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content":
                        f"Context:\n{context}\n\n"
                        f"Question:\n{question}"
                }
            ]
        )

        return response["message"]["content"]
