import pytest
import pandas as pd
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator
from core.exceptions import CalculationError


def test_log_returns(price_data):
    calc = ReturnsCalculator()
    result = calc.calculate(price_data["Close"], log_returns=True)
    assert isinstance(result, pd.Series)
    assert not result.isnull().any()


def test_pct_returns(price_data):
    calc = ReturnsCalculator()
    result = calc.calculate(price_data["Close"], log_returns=False)
    assert isinstance(result, pd.Series)


def test_returns_calculate_exception():
    rc = ReturnsCalculator()
    with pytest.raises(CalculationError):
        rc.calculate(12345)


def test_volatility_calculation(returns_data):
    calc = VolatilityCalculator()
    result = calc.calculate(returns_data, window=2)
    assert isinstance(result, pd.Series)


def test_volatility_calculate_exception():
    vc = VolatilityCalculator()
    with pytest.raises(CalculationError):
        vc.calculate(12345)
