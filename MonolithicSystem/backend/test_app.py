from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app

client = TestClient(app)

def test_signup():
    response = client.post("/signup/", data={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200 

def test_signin():
    response = client.post("/signin/", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200

def test_create_post():
    response = client.post("/post/", data={"title": "My Post", "content": "This is a test post."}, headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200

def test_create_notification():
    response = client.post("/notifications/", data={"post_id": 1}, headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200
