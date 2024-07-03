from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the data processing API"}

def test_cors_headers():
    # Make a preflight request to check CORS headers
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET",
    }
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert set(response.headers.get("access-control-allow-methods").replace(" ", "").split(",")) == set("GET,HEAD,POST,OPTIONS,PUT,PATCH,DELETE".split(","))
    assert response.headers.get("access-control-allow-credentials") == "true"
    allow_headers = response.headers.get("access-control-allow-headers")
    assert allow_headers is None or allow_headers == "*"
