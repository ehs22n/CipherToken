import pytest
from ciphertoken import CipherToken, is_jwt_format
from ciphertoken.jwt import access, refresh, rotation, access_async, refresh_async, rotation_async, TOKEN_ACCESS, TOKEN_REFRESH
from ciphertoken.algorithms import HS256
from ciphertoken.secret import secret_key


class TestJWTModuleSync:
    """Tests for JWT module sync functions."""

    def test_jwt_access(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        token = access(ct)
        assert is_jwt_format(token)

    def test_jwt_refresh(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        token = refresh(ct)
        assert is_jwt_format(token)

    def test_jwt_rotation(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        refresh_tok = refresh(ct)
        access_tok, new_refresh = rotation(ct, refresh_tok)
        assert is_jwt_format(access_tok)
        assert is_jwt_format(new_refresh)


class TestJWTModuleAsync:
    """Tests for async JWT module functions."""

    @pytest.mark.asyncio
    async def test_jwt_access_async(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        token = await access_async(ct)
        assert is_jwt_format(token)

    @pytest.mark.asyncio
    async def test_jwt_refresh_async(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        token = await refresh_async(ct)
        assert is_jwt_format(token)

    @pytest.mark.asyncio
    async def test_jwt_rotation_async(self):
        secret = secret_key()
        ct = CipherToken(secret, HS256, 3600, 7200)
        refresh_tok = await refresh_async(ct)
        access_tok, new_refresh = await rotation_async(ct, refresh_tok)
        assert is_jwt_format(access_tok)
        assert is_jwt_format(new_refresh)


class TestJWTConstants:
    """Tests for JWT module constants."""

    def test_token_access_constant(self):
        assert TOKEN_ACCESS == "access"

    def test_token_refresh_constant(self):
        assert TOKEN_REFRESH == "refresh"