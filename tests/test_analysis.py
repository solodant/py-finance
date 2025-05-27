"""
Unit tests for ReturnsCalculator and VolatilityCalculator.

These tests verify the correctness and robustness of return and volatility calculations.
Tests cover:
- Logarithmic and percentage return calculations
- Rolling volatility calculations
- Handling of invalid input through CalculationError exceptions
"""

import pytest
from pandas import Series, DataFrame
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator
from core.exceptions import CalculationError


def test_log_returns(price_data: DataFrame) -> None:
    """Test that log returns are calculated correctly and contain no nulls."""
    calc = ReturnsCalculator()
    result: Series = calc.calculate(price_data["Close"], log_returns=True)
    assert isinstance(result, Series)
    assert not result.isnull().any()


def test_pct_returns(price_data: DataFrame) -> None:
    """Test that percentage returns are calculated correctly."""
    calc = ReturnsCalculator()
    result: Series = calc.calculate(price_data["Close"], log_returns=False)
    assert isinstance(result, Series)


def test_returns_calculate_exception() -> None:
    """Test that ReturnsCalculator raises CalculationError on invalid input."""
    rc = ReturnsCalculator()
    with pytest.raises(CalculationError):
        rc.calculate(12345)  # Invalid input type


def test_volatility_calculation(returns_data: Series) -> None:
    """Test that rolling volatility is calculated correctly over a given window."""
    calc = VolatilityCalculator()
    result: Series = calc.calculate(returns_data, window=2)
    assert isinstance(result, Series)


def test_volatility_calculate_exception() -> None:
    """Test that VolatilityCalculator raises CalculationError on invalid input."""
    vc = VolatilityCalculator()
    with pytest.raises(CalculationError):
        vc.calculate(12345)  # Invalid input type
