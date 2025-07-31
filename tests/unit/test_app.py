import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json == {"message": "Hello from Flask API!"}

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {"status": "healthy"}

def test_random_number(client):
    res = client.get("/random")
    assert res.status_code == 200
    assert "random_number" in res.json
    assert isinstance(res.json["random_number"], int)
    assert 1 <= res.json["random_number"] < 100
