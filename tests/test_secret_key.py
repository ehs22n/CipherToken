import pytest
import base64
from ciphertoken.secret import (
    secret_key,
    secret_key_with_size,
    generate_hmac_secret,
    generate_hmac_secret_async,
    generate_rsa_keypair,
)
from ciphertoken.utils import DEFAULT_SECRET_SIZE


class TestSecretKey:
    """Tests for secret key generation functions."""

    def test_secret_key_default(self):
        key = secret_key()
        assert isinstance(key, str)
        assert len(key) > 0

    def test_secret_key_decodable(self):
        key = secret_key()
        decoded = base64.b64decode(key)
        assert len(decoded) == DEFAULT_SECRET_SIZE

    def test_secret_key_with_size(self):
        key = secret_key_with_size(32)
        assert isinstance(key, str)
        decoded = base64.b64decode(key)
        assert len(decoded) == 32

    def test_secret_key_with_size_large(self):
        key = secret_key_with_size(64)
        decoded = base64.b64decode(key)
        assert len(decoded) == 64

    def test_secret_key_with_size_invalid(self):
        with pytest.raises(ValueError, match="at least 16 bytes"):
            secret_key_with_size(15)

    def test_generate_hmac_secret_default(self):
        key = generate_hmac_secret(32)
        assert isinstance(key, str)
        decoded = base64.b64decode(key)
        assert len(decoded) == 32

    def test_generate_hmac_secret_invalid_size(self):
        with pytest.raises(ValueError, match="at least 16 bytes"):
            generate_hmac_secret(15)

    def test_generate_rsa_keypair_default(self):
        private_key, public_key = generate_rsa_keypair()
        assert isinstance(private_key, str)
        assert isinstance(public_key, str)
        assert "PRIVATE KEY" in private_key
        assert "PUBLIC KEY" in public_key

    def test_generate_rsa_keypair_custom_bits(self):
        private_key, public_key = generate_rsa_keypair(2048)
        assert isinstance(private_key, str)
        assert isinstance(public_key, str)

    def test_generate_rsa_keypair_invalid_bits(self):
        with pytest.raises(ValueError, match="at least 2048 bits"):
            generate_rsa_keypair(1024)


class TestAsyncSecretKey:
    """Tests for async secret key generation functions."""

    @pytest.mark.asyncio
    async def test_generate_hmac_secret_async_default(self):
        key = await generate_hmac_secret_async(32)
        assert isinstance(key, str)
        decoded = base64.b64decode(key)
        assert len(decoded) == 32

    @pytest.mark.asyncio
    async def test_generate_hmac_secret_async_invalid_size(self):
        with pytest.raises(ValueError, match="at least 16 bytes"):
            await generate_hmac_secret_async(15)
