import pytest
from ciphertoken.time import now, seconds, minutes, hours, days, weeks


class TestTimeHelpers:
    """Tests for time helper functions."""

    def test_now(self):
        current = now()
        assert isinstance(current, int)
        assert current > 0

    def test_seconds(self):
        assert seconds(10) == 10
        assert seconds(0) == 0

    def test_minutes(self):
        assert minutes(1) == 60
        assert minutes(2) == 120
        assert minutes(0) == 0

    def test_hours(self):
        assert hours(1) == 3600
        assert hours(2) == 7200

    def test_days(self):
        assert days(1) == 86400
        assert days(2) == 172800

    def test_weeks(self):
        assert weeks(1) == 604800
        assert weeks(2) == 1209600