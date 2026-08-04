import uuid
import pytest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token


def test_argon2id_password_hashing():
    pw = "SuperSecure#2026Password"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword#1", hashed) is False


def test_jwt_access_token():
    user_id = str(uuid.uuid4())
    token = create_access_token(data={"sub": user_id, "role": "CITIZEN"})
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == "CITIZEN"
    assert payload["type"] == "access"


def test_jwt_refresh_token():
    user_id = uuid.uuid4()
    token_str, jti, expires_at = create_refresh_token(user_id)
    payload = decode_token(token_str)
    assert payload["sub"] == str(user_id)
    assert payload["jti"] == jti
    assert payload["type"] == "refresh"
