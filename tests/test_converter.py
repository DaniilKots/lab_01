import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidNumberError,
    UnknownUnitError,
)


def test_length_mass():
    assert convert(1000, "mm", "m") == pytest.approx(1)
    assert convert("1.5", "kg", "g") == pytest.approx(1500)


def test_temperature():
    assert convert(0, "c", "f") == pytest.approx(32)
    assert convert(-273.15, "c", "k") == pytest.approx(0, abs=1e-9)


def test_case_insensitive():
    assert convert(1, "KM", "M") == pytest.approx(1000)


@pytest.mark.parametrize("args, exc", [
    ((-300, "c", "k"), BelowAbsoluteZeroError),
    ((-1, "k", "c"), BelowAbsoluteZeroError),
    ((1, "kg", "m"), IncompatibleUnitsError),
    ((1, "xx", "m"), UnknownUnitError),
    (("abc", "m", "km"), InvalidNumberError),
    (("nan", "m", "km"), InvalidNumberError),
])
def test_convert_errors(args, exc):
    with pytest.raises(exc):
        convert(*args)


def test_comma():
    assert convert("1,5", "kg", "g") == pytest.approx(1500)
