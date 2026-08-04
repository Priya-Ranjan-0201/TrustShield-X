import pytest
from app.core.password_policy import validate_password_strength


def test_password_too_short():
    is_valid, err = validate_password_strength("Short1!")
    assert not is_valid
    assert "at least 10 characters" in err


def test_password_missing_uppercase():
    is_valid, err = validate_password_strength("lowercase123!")
    assert not is_valid
    assert "uppercase letter" in err


def test_password_missing_lowercase():
    is_valid, err = validate_password_strength("UPPERCASE123!")
    assert not is_valid
    assert "lowercase letter" in err


def test_password_missing_digit():
    is_valid, err = validate_password_strength("NoDigitsHere!")
    assert not is_valid
    assert "digit" in err


def test_password_missing_special_char():
    is_valid, err = validate_password_strength("NoSpecialChar123")
    assert not is_valid
    assert "special character" in err


def test_common_password_rejected():
    is_valid, err = validate_password_strength("Password123!")
    assert not is_valid
    assert "too common" in err


def test_valid_strong_password():
    is_valid, err = validate_password_strength("StrongAuth#2026Secure")
    assert is_valid
    assert err is None
