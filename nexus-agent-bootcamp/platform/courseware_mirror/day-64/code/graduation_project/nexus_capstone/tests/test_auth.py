"""Day 64 — 认证模块单元测试"""
import pytest
from app.auth.service import hash_password, verify_password, create_access_token


def test_password_hash_and_verify():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_token():
    token = create_access_token(user_id=42)
    assert isinstance(token, str)
    assert len(token) > 20
