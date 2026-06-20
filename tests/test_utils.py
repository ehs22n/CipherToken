import pytest
from ciphertoken.utils import DEFAULT_SECRET_SIZE, MIN_SECRET_SIZE, TOKEN_ACCESS, TOKEN_REFRESH


class TestUtilsConstants:
    """Tests for utils module constants."""

    def test_token_access_constant(self):
        assert TOKEN_ACCESS == "access"

    def test_token_refresh_constant(self):
        assert TOKEN_REFRESH == "refresh"

    def test_default_secret_size(self):
        assert DEFAULT_SECRET_SIZE == 32

    def test_min_secret_size(self):
        assert MIN_SECRET_SIZE == 16