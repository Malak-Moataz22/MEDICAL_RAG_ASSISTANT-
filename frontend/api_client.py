import os
import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def ask_question(question: str):
    response = requests.post(
        f"{API_BASE_URL}/api/query",
        json={"question": question}
    )

    response.raise_for_status()
    return response.json()