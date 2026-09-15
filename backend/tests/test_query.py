from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_query_happy_path():
    response = client.post(
        "/api/query",
        json={"question": "What are the common symptoms of diabetes?"}
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data


def test_query_invalid_input():
    response = client.post(
        "/api/query",
        json={}
    )

    assert response.status_code == 422