import pytest

from toolkit.calculator import calculate, to_rpn, tokenize, validate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
    ToolkitError,
)


@pytest.mark.parametrize("expr, expected", [
    ("2+3*4", 14),
    ("10 / 4", 2.5),
    ("-2 * -3", 6),
    ("1+-2", -1),
    ("(2+3)*4", 20),
    ("10-4-3", 3),
    ("8/4/2", 1),
    ("1.5+1.5", 3),
    ("-(1+2)", -3),
    ("  7  ", 7),
    ("1,5+1.5", 3),
    ("7//2", 3),
    ("-7//2", -4),
    ("7//-2", -4),
    ("7%3", 1),
    ("-7%3", 2),
    ("7%-3", -2),
    ("2+7%4*2", 8),
])
def test_calc_ok(expr, expected):
    assert calculate(expr) == pytest.approx(expected)


def test_rpn_form():
    assert to_rpn(validate(tokenize("2+3*4"))) == ["2", "3", "4", "*", "+"]
    assert to_rpn(validate(tokenize("-2*-3"))) == ["2", "u-", "3", "u-", "*"]


@pytest.mark.parametrize("expr", ["", "   ", "2*/3", "2+a", "1/0", "2+", "(1+2", "1+2)",
                                  "1 2", "1..2", "()", "*3"])
def test_calc_errors(expr):
    with pytest.raises(ToolkitError):
        calculate(expr)


@pytest.mark.parametrize("expr, exc", [
    ("", EmptyExpressionError),
    ("2+a", InvalidCharacterError),
    ("2*/3", ConsecutiveOperatorsError),
    ("2+", MissingOperandError),
    ("1/0", DivisionByZeroError),
])
def test_calc_error_types(expr, exc):
    with pytest.raises(exc):
        calculate(expr)


@pytest.mark.parametrize("expr", ["1//0", "1%0", "1///2", "5%"])
def test_new_ops_errors(expr):
    with pytest.raises(ToolkitError):
        calculate(expr)
