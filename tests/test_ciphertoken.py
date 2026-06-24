import pytest
from ciphertoken import CipherToken, is_jwt_format, validate_jwt_format
from ciphertoken.algorithms import HS256
from ciphertoken.secret import secret_key


class TestCipherToken:
    """Tests for CipherToken class."""

    @pytest.fixture
    def hmac_secret(self):
        return secret_key()

    @pytest.fixture
    def token_hs256(self, hmac_secret):
        return CipherToken(hmac_secret, HS256, 3600, 7200)

    def test_create_access_token(self, token_hs256):
        token = token_hs256.access()
        assert is_jwt_format(token)

    def test_create_refresh_token(self, token_hs256):
        token = token_hs256.refresh()
        assert is_jwt_format(token)

    def test_decode_token(self, token_hs256):
        token = token_hs256.access({"user_id": 123, "role": "admin"})
        decoded = token_hs256.decode(token)
        assert decoded["token_type"] == "access"
        assert decoded["user_id"] == 123
        assert decoded["role"] == "admin"
        assert "exp" in decoded
        assert "ttl" in decoded
        assert "jti" in decoded

    def test_verify_valid_token(self, token_hs256):
        token = token_hs256.access()
        assert token_hs256.verify(token) is True

    def test_verify_invalid_token(self, token_hs256):
        assert token_hs256.verify("invalid.token.here") is False

    def test_inspect_token(self, token_hs256):
        token = token_hs256.access({"data": "test"})
        inspected = token_hs256.inspect(token)
        assert inspected["token_type"] == "access"
        assert inspected["data"] == "test"

    def test_remaining_time(self, token_hs256):
        token = token_hs256.access()
        remaining = token_hs256.remaining_time(token)
        assert remaining is not None
        assert remaining > 0

    def test_token_rotation(self, token_hs256):
        refresh_token = token_hs256.refresh({"user_id": 456})
        access_token, new_refresh = token_hs256.rotation(
            refresh_token, {"user_id": 456}
        )
        assert is_jwt_format(access_token)
        assert is_jwt_format(new_refresh)

        access_decoded = token_hs256.decode(access_token)
        assert access_decoded["token_type"] == "access"
        assert access_decoded["user_id"] == 456

    def test_rotation_non_refresh_token(self, token_hs256):
        access_token = token_hs256.access()
        with pytest.raises(ValueError, match="Only refresh tokens"):
            token_hs256.rotation(access_token)

    def test_algorithm_name(self, token_hs256):
        assert token_hs256.algorithm_name() == HS256

    def test_access_ttl_property(self, token_hs256):
        assert token_hs256.access_ttl == 3600

    def test_refresh_ttl_property(self, token_hs256):
        assert token_hs256.refresh_ttl == 7200

    def test_secret_property_masked(self, token_hs256):
        masked = token_hs256.secret
        assert masked.endswith("...")


class TestAsyncCipherToken:
    """Tests for async CipherToken methods."""

    @pytest.fixture
    def hmac_secret(self):
        return secret_key()

    @pytest.fixture
    def token_hs256(self, hmac_secret):
        return CipherToken(hmac_secret, HS256, 3600, 7200)

    @pytest.mark.asyncio
    async def test_access_async(self, token_hs256):
        token = await token_hs256.access_async()
        assert is_jwt_format(token)
        decoded = token_hs256.decode(token)
        assert decoded["token_type"] == "access"

    @pytest.mark.asyncio
    async def test_refresh_async(self, token_hs256):
        token = await token_hs256.refresh_async()
        assert is_jwt_format(token)
        decoded = token_hs256.decode(token)
        assert decoded["token_type"] == "refresh"

    @pytest.mark.asyncio
    async def test_decode_async(self, token_hs256):
        token = await token_hs256.access_async({"user": "test"})
        decoded = await token_hs256.decode_async(token)
        assert decoded["token_type"] == "access"
        assert decoded["user"] == "test"

    @pytest.mark.asyncio
    async def test_verify_async_valid(self, token_hs256):
        token = await token_hs256.access_async()
        result = await token_hs256.verify_async(token)
        assert result is True

    @pytest.mark.asyncio
    async def test_verify_async_invalid(self, token_hs256):
        result = await token_hs256.verify_async("invalid.token.here")
        assert result is False

    @pytest.mark.asyncio
    async def test_rotation_async(self, token_hs256):
        refresh_token = await token_hs256.refresh_async({"user_id": 789})
        access_token, new_refresh = await token_hs256.rotation_async(
            refresh_token, {"user_id": 789}
        )
        assert is_jwt_format(access_token)
        assert is_jwt_format(new_refresh)
        decoded = token_hs256.decode(access_token)
        assert decoded["token_type"] == "access"
        assert decoded["user_id"] == 789


class TestCreateToken:
    """Tests for create_token method."""

    def test_create_token_access(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        access = token.create_token(3600, "access")
        decoded = token.decode(access)
        assert decoded["token_type"] == "access"

    def test_create_token_with_defaults(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        t = token.create_token()
        decoded = token.decode(t)
        assert decoded["token_type"] == "jwt"

    def test_create_token_refresh(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        refresh = token.create_token(7200, "refresh")
        decoded = token.decode(refresh)
        assert decoded["token_type"] == "refresh"


class TestPayloadMethod:
    """Tests for payload method."""

    def test_payload_creates_access_token(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        access = token.payload({"data": "value"})
        decoded = token.decode(access)
        assert decoded["token_type"] == "access"
        assert decoded["data"] == "value"


class TestPayloadEdgeCases:
    """Tests for payload edge cases."""

    def test_empty_payload(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        access = token.access()
        decoded = token.decode(access)
        assert decoded["token_type"] == "access"

    def test_complex_payload(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        access = token.access(
            {
                "nested": {"key": "value"},
                "list": [1, 2, 3],
                "number": 42,
                "string": "hello",
                "bool": True,
            }
        )
        decoded = token.decode(access)
        assert decoded["nested"]["key"] == "value"
        assert list(decoded["list"]) == [1, 2, 3]
        assert decoded["number"] == 42
        assert decoded["string"] == "hello"
        assert decoded["bool"] == 1  # PyO3 converts bool to int for JSON


class TestJWTFormat:
    """Tests for JWT format validation."""

    def test_is_jwt_format_valid(self):
        assert is_jwt_format("a.b.c") is True
        assert is_jwt_format("header.payload.signature") is True
        assert (
            is_jwt_format(
                "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            )
            is True
        )

    def test_is_jwt_format_invalid(self):
        assert is_jwt_format("invalid") is False
        assert is_jwt_format("a.b") is False
        assert is_jwt_format("") is False
        assert is_jwt_format("..") is False

    def test_validate_jwt_format_valid(self):
        assert validate_jwt_format("a.b.c") is True

    def test_validate_jwt_format_invalid(self):
        with pytest.raises(ValueError):
            validate_jwt_format("invalid")


class TestInvalidAlgorithm:
    """Tests for invalid algorithm handling."""

    def test_invalid_algorithm(self):
        with pytest.raises(ValueError, match="Unsupported algorithm"):
            CipherToken(secret_key(), "INVALID", 3600, 7200)
