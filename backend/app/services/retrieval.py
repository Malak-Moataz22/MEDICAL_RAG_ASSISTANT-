from chromadb import PersistentClient
from backend.app.core.config import settings
from backend.app.services.generation import generate_answer


def get_vector_store():
    client = PersistentClient(path=settings.VECTOR_STORE_PATH)

    try:
        collection = client.get_collection(name="medical_rag")
    except Exception:
        collection = client.get_or_create_collection(name="medical_rag")

    return collection


def query_rag_pipeline(question: str):
    collection = get_vector_store()

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    retrieved_docs = results["documents"][0] if results["documents"] else []
    sources = results["metadatas"][0] if results["metadatas"] else []

    context = "\n\n".join(retrieved_docs)

    answer_text = generate_answer(
        question=question,
        context=context
    )

    source_list = [
        str(s.get("source", "Unknown"))
        for s in sources
    ] if sources else ["Medical Documents"]

    return {
        "answer": answer_text,
        "sources": list(set(source_list))
    }