import pytest
from ciphertoken import CipherToken, is_jwt_format
from ciphertoken.algorithms import HS256, HS384, HS512, RS256, RS384, RS512, ES256, ES384, PS256, PS384, PS512, EDDSA
from ciphertoken.secret import secret_key, generate_rsa_keypair


class TestAlgorithmStrings:
    """Tests for algorithm string constants."""

    def test_hs256_constant(self):
        assert HS256 == "HS256"

    def test_hs384_constant(self):
        assert HS384 == "HS384"

    def test_hs512_constant(self):
        assert HS512 == "HS512"

    def test_rs256_constant(self):
        assert RS256 == "RS256"

    def test_rs384_constant(self):
        assert RS384 == "RS384"

    def test_rs512_constant(self):
        assert RS512 == "RS512"

    def test_es256_constant(self):
        assert ES256 == "ES256"

    def test_es384_constant(self):
        assert ES384 == "ES384"

    def test_ps256_constant(self):
        assert PS256 == "PS256"

    def test_ps384_constant(self):
        assert PS384 == "PS384"

    def test_ps512_constant(self):
        assert PS512 == "PS512"

    def test_eddsa_constant(self):
        assert EDDSA == "EdDSA"


class TestHMACAlgorithms:
    """Tests for HMAC algorithms (HS256, HS384, HS512)."""

    def test_hs256(self):
        secret = secret_key()
        token = CipherToken(secret, HS256, 3600, 7200)
        access = token.access()
        decoded = token.decode(access)
        assert decoded["token"] == "access"

    def test_hs384(self):
        secret = secret_key()
        token = CipherToken(secret, HS384, 3600, 7200)
        access = token.access()
        decoded = token.decode(access)
        assert decoded["token"] == "access"

    def test_hs512(self):
        secret = secret_key()
        token = CipherToken(secret, HS512, 3600, 7200)
        access = token.access()
        decoded = token.decode(access)
        assert decoded["token"] == "access"


class TestRSAAlgorithms:
    """Tests for RSA algorithms (RS256, RS384, RS512)."""

    def test_rsa256_with_valid_key(self):
        private_key, _ = generate_rsa_keypair()
        token = CipherToken(private_key, RS256, 3600, 7200)
        access = token.access()
        assert is_jwt_format(access)

    def test_rsa384_with_valid_key(self):
        private_key, _ = generate_rsa_keypair()
        token = CipherToken(private_key, RS384, 3600, 7200)
        access = token.access()
        assert is_jwt_format(access)

    def test_rsa512_with_valid_key(self):
        private_key, _ = generate_rsa_keypair()
        token = CipherToken(private_key, RS512, 3600, 7200)
        access = token.access()
        assert is_jwt_format(access)


class TestInvalidKeyFormats:
    """Tests for algorithms that require specific key formats."""

    def test_rsa_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, RS256, 3600, 7200).access()

    def test_ec256_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, ES256, 3600, 7200).access()

    def test_ec384_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, ES384, 3600, 7200).access()

    def test_pss256_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, PS256, 3600, 7200).access()

    def test_pss384_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, PS384, 3600, 7200).access()

    def test_pss512_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, PS512, 3600, 7200).access()

    def test_eddsa_requires_valid_key(self):
        secret = secret_key()
        with pytest.raises(ValueError, match="InvalidKeyFormat"):
            CipherToken(secret, EDDSA, 3600, 7200).access()