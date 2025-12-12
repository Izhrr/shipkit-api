from auth import authenticate_user, create_access_token
from fastapi.testclient import TestClient
from main import app
from jose import jwt
import pytest
import os

client = TestClient(app)

def test_authenticate_user_success():
    # default FAKE_USERS_DB created at module import; these credentials exist per repo note
    user = authenticate_user("admin", "admin123")
    assert user and user.get("username") == "admin"

def test_verify_token_missing_sub():
    from auth import verify_token
    from fastapi import HTTPException
    from fastapi.security import HTTPAuthorizationCredentials
    from jose import jwt
    import os

    secret = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    token = jwt.encode({"exp": 9999999999}, secret, algorithm="HS256") 

    creds = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    with pytest.raises(HTTPException):
        import asyncio
        asyncio.run(verify_token(creds))

def test_verify_token_user_not_found():
    from auth import verify_token
    from fastapi.security import HTTPAuthorizationCredentials
    from jose import jwt
    import os
    import asyncio
    from auth import FAKE_USERS_DB

    # pastikan user_name yang TIDAK ada
    missing_user = "ghost-user"
    assert missing_user not in FAKE_USERS_DB

    secret = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    token = jwt.encode({"sub": missing_user}, secret, algorithm="HS256")

    creds = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    import pytest
    with pytest.raises(Exception):
        asyncio.run(verify_token(creds))

def test_authenticate_user_failure():
    user = authenticate_user("nope", "wrong")
    assert user is False

def test_create_access_token_contains_sub():
    token = create_access_token({"sub": "admin"})
    assert isinstance(token, str)
    # decode basic sanity check using the same secret/alg
    decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY", "test-secret-key"), algorithms=["HS256"])
    assert decoded.get("sub") == "admin"

def test_verify_token_invalid_signature():
    from auth import verify_token
    from fastapi import HTTPException
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="this.is.not.a.valid.jwt"
    )

    with pytest.raises(HTTPException):
        # must call asyncio loop manually because verify_token is async
        import asyncio
        asyncio.run(verify_token(creds))

def test_verify_password():
    from auth import pwd_context, verify_password
    plain = "admin123"
    hashed = pwd_context.hash(plain)
    assert verify_password(plain, hashed) is True
    assert verify_password("salah", hashed) is False

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