import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Run a real quality check" in response.data


def test_run_rejects_missing_url(client):
    response = client.post("/api/run", json={"type": "web"})
    assert response.status_code == 400
    assert "URL" in response.get_json()["error"]


def test_run_rejects_invalid_url_format(client):
    response = client.post("/api/run", json={"url": "not-a-real-url", "type": "web"})
    assert response.status_code == 400


def test_run_api_check_against_real_endpoint(client):
    """Runs a real check against a known-stable public API to prove the pipeline works end to end."""
    response = client.post(
        "/api/run",
        json={"url": "https://jsonplaceholder.typicode.com/posts/1", "type": "api"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] >= 1
    assert data["passed"] >= 1


def test_history_endpoint_returns_list(client):
    response = client.get("/api/history")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
