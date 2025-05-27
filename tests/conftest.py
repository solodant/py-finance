"""
Test fixtures for unit testing various components of the py-finance project.

Provides reusable argument mocks (Args) and sample DataFrame data for testing:
- CLI arguments for different input types (CSV, Excel, tickers, currencies)
- Price and returns data used in analysis module tests
"""

import pytest
import pandas as pd
from pandas import DataFrame, Series
from pathlib import Path


@pytest.fixture
def args_empty() -> object:
    """Fixture returning Args instance with all fields set to None."""

    class Args:
        def __init__(self) -> None:
            self.csv = None
            self.excel = None
            self.tickers = None
            self.currencies = None
            self.period = None

    return Args()


@pytest.fixture
def args_csv(tmp_path: Path) -> object:
    """Fixture returning Args instance with a CSV path and default period."""

    class Args:
        def __init__(self) -> None:
            self.csv = str(tmp_path / "test.csv")
            self.excel = None
            self.tickers = None
            self.currencies = None
            self.period = "1y"

    return Args()


@pytest.fixture
def args_excel(tmp_path: Path) -> object:
    """Fixture returning Args instance with an Excel path and default period."""

    class Args:
        def __init__(self) -> None:
            self.csv = None
            self.excel = str(tmp_path / "test.xlsx")
            self.tickers = None
            self.currencies = None
            self.period = "1y"

    return Args()


@pytest.fixture
def args_ticker() -> object:
    """Fixture returning Args instance with a single ticker and 6-month period."""

    class Args:
        def __init__(self) -> None:
            self.csv = None
            self.excel = None
            self.tickers = ["AAPL"]
            self.currencies = None
            self.period = "6mo"

    return Args()


@pytest.fixture
def args_currency() -> object:
    """Fixture returning Args instance with a single currency pair and 6-month period."""

    class Args:
        def __init__(self) -> None:
            self.csv = None
            self.excel = None
            self.tickers = None
            self.currencies = ["USDRUB"]
            self.period = "6mo"

    return Args()


@pytest.fixture
def price_data() -> DataFrame:
    """Fixture returning a sample price DataFrame with 'Close' values."""
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "Close": [100, 102, 101, 105, 107],
    }
    return pd.DataFrame(data).set_index("Date")


@pytest.fixture
def returns_data(price_data: DataFrame) -> Series:
    """Fixture returning a Series of calculated returns from price_data."""
    from analysis.returns import ReturnsCalculator

    return ReturnsCalculator().calculate(price_data["Close"])


@pytest.fixture
def dummy_df() -> DataFrame:
    """Fixture returning a dummy DataFrame with 'Open' and 'Close' columns and date index."""
    df = pd.DataFrame(
        {
            "Open": [1.0, 2.0],
            "Close": [1.5, 2.5],
            "Date": pd.date_range("2023-01-01", periods=2),
        }
    ).set_index("Date")
    return df
