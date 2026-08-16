from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_invalid_file_type():
    response = client.post(
        "/api/detect/image",
        files={"file": ("test.txt", b"hello world", "text/plain")})
    assert response.status_code == 400

def test_image_upload():
    with open("bus_test.jpg","rb") as f:
        response = client.post("/api/detect/image", files={"file":("bus_test.jpg", f, "image/jpeg")})
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "detection" in data