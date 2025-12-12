from auth import authenticate_user, create_access_token
from fastapi.testclient import TestClient
from main import app
from jose import jwt
import os

client = TestClient(app)

def test_authenticate_user_success():
    # default FAKE_USERS_DB created at module import; these credentials exist per repo note
    user = authenticate_user("admin", "admin123")
    assert user and user.get("username") == "admin"

def test_authenticate_user_failure():
    user = authenticate_user("nope", "wrong")
    assert user is False

def test_create_access_token_contains_sub():
    token = create_access_token({"sub": "admin"})
    assert isinstance(token, str)
    # decode basic sanity check using the same secret/alg
    decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY", "test-secret-key"), algorithms=["HS256"])
    assert decoded.get("sub") == "admin"

def test_login_endpoint_success(monkeypatch):
    # Patch authenticate_user to deterministic behavior
    monkeypatch.setattr("auth.authenticate_user", lambda u, p: {"username": "admin"})
    r = client.post("/api/v1/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_endpoint_fail(monkeypatch):
    monkeypatch.setattr("auth.authenticate_user", lambda u, p: False)
    r = client.post("/api/v1/login", json={"username": "foo", "password": "bar"})
    assert r.status_code == 401