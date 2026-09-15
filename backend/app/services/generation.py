from ollama import chat
from backend.app.core.config import settings


def generate_answer(question: str, context: str):
    prompt = f"""You are a helpful medical AI assistant.
Use ONLY the following medical context to answer the user's question.
If the context does not contain enough information, say that you don't know based on the provided medical documents.
Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    response = chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]